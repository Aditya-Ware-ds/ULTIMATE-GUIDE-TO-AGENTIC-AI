# Threat model / red-team report -- Secure enterprise agent

Following Module 18 lesson 03's four-step red-team process exactly: pick a
realistic scenario, prove the exploit with a failing test, patch it, prove
the same test now shows it blocked. Every threat below maps to a specific,
currently-passing test in `tests/`.

## Red-team scenario 1: approval alone is not a sufficient safeguard

**Realistic scenario, grounded in this agent's actual tools**: an
enterprise assistant with a `send_announcement` tool is asked (by a
legitimate user, or by a user whose request was itself shaped by content
the agent read elsewhere -- Module 18 lesson 01's indirect-injection
vector) to send an announcement to a channel that sounds plausible but
isn't actually an approved internal channel (e.g. `external-leak-channel`,
or a channel name crafted to look internal but isn't on the real
allowlist). A busy human approver, reviewing many approval requests, might
not scrutinize the channel name carefully and approve it.

**Step 1 -- the scenario**: as above -- a plausible, specific attack on
*this* agent's actual capability (not a generic "try to jailbreak it").

**Step 2 -- prove the exploit** (if the tool had no allowlist, or if the
allowlist were only checked at the agent/approval layer instead of inside
the tool itself): a test scripting the model requesting
`send_announcement(channel="external-leak-channel", ...)`, followed by
`resume_after_approval(..., approved=True)`, would show the announcement
actually recorded in `_SENT_ANNOUNCEMENTS` -- the exploit succeeding
because approval alone was trusted as sufficient.

**Step 3 -- the patch**: `send_announcement` (in `mcp_server.py`) checks
`channel` against `ANNOUNCEMENT_CHANNEL_ALLOWLIST` **inside the tool
itself**, raising `ToolError` regardless of whether the calling agent
already obtained human approval. The approval gate and the allowlist are
independent, composed layers (Module 18 lesson 02's "combining with Module
09's approval gates" point) -- neither one alone is treated as sufficient.

**Step 4 -- prove the fix**: `test_redteam_approved_but_non_allowlisted_channel_is_still_blocked`
scripts exactly the scenario above -- the model requests the
non-allowlisted channel, a human approves it (`approved=True`) -- and
asserts `_SENT_ANNOUNCEMENTS == []`. The test currently passes: the
tool-level boundary holds even when the human-approval layer would have
let it through.

## Threat 2: a swallowed error message hiding why an action was blocked

**Scenario**: if the MCP server's tool raised a plain exception instead of
`ToolError`, the calling agent (and ultimately the user) would see only a
generic "Error executing tool send_announcement" -- with no indication
*why* the send failed, making it harder for a legitimate user to correct a
genuine typo versus recognizing a blocked malicious attempt.

**Defense**: `mcp_server.py` raises `mcp.server.mcpserver.exceptions.ToolError`
specifically (verified, see `ARCHITECTURE.md`, to be the mechanism that
actually propagates a specific message to the client) for both the
unknown-record and the non-allowlisted-channel cases.

**Proof**: `test_dispatch_surfaces_the_real_error_message_for_an_unknown_record`.

## Threat 3: dispatching a consequential action before approval

**Scenario**: a bug in the agent loop calls `dispatch` for
`send_announcement` immediately, before checkpointing and pausing for
human review -- defeating the entire purpose of the approval gate.

**Defense**: `_continue_loop` checks `tool_call.name in REQUIRES_APPROVAL`
**before** ever calling `dispatch` -- a `REQUIRES_APPROVAL` tool always
saves a checkpoint and returns `"paused"` first.

**Proof**: `test_run_agent_with_approval_pauses_before_sending_an_announcement`
explicitly checks `_SENT_ANNOUNCEMENTS == []` at the paused state, not just
that the returned status says `"paused"`.

## Threat 4: a checkpoint that doesn't actually survive a restart

**Scenario**: if the checkpoint format or the resume logic accidentally
depended on some in-memory state (a global variable, an object held only
in the original process), a real production restart between approval
request and human response would silently lose the pending action, or
resume incorrectly.

**Defense**: `resume_after_approval` only reads from `load_checkpoint`'s
return value (parsed from the JSON file on disk) and the freshly-passed-in
`mcp_client` -- nothing about resume depends on any state from the
original `run_agent_with_approval` call's process.

**Proof**: `test_kill_and_resume_reloads_the_checkpoint_from_a_fresh_process`
-- resume is tested against genuinely fresh module instances and a fresh
MCP server, not the same objects the pause used.

## What this threat model does not cover

This agent's tools don't currently retrieve untrusted external content
(unlike Module 18's own lab's `read_document`) -- `lookup_record` reads
from a small trusted internal dict. A production version connecting
`lookup_record` to a real, externally-editable data source (a wiki, a
ticket system) would need Module 18's full indirect-injection analysis
applied to that specific data source, the same way this threat model
applies Module 18's allowlist pattern to `send_announcement`.
