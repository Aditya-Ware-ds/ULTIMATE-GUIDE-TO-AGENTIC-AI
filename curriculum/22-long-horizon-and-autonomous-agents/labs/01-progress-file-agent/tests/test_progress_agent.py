TASK_NAMES = ["Research topic A", "Draft section 1", "Draft section 2"]


def test_load_progress_returns_none_when_no_file_exists(progress_agent, progress_path):
    assert progress_agent.load_progress(progress_path) is None


def test_save_then_load_progress_round_trips(progress_agent, progress_path):
    tasks = [{"name": "t1", "status": "pending", "result": None}]

    progress_agent.save_progress(progress_path, tasks)

    assert progress_agent.load_progress(progress_path) == tasks


async def test_run_long_horizon_agent_completes_all_tasks_in_one_run(
    progress_agent, client, progress_path
):
    for _ in TASK_NAMES:
        client.provider.add_text("done")

    result = await progress_agent.run_long_horizon_agent(client, progress_path, TASK_NAMES)

    assert all(task["status"] == "done" for task in result["tasks"])
    assert client.provider.call_count == len(TASK_NAMES)


async def test_kill_and_resume_does_not_repeat_completed_tasks(
    progress_agent, client, progress_path
):
    # Simulate a crash after the first task: call the single-task function
    # directly rather than letting a full run complete in one call (the
    # same kill-and-resume test pattern as Module 07's lab).
    client.provider.add_text("Result for task 1")
    tasks = [{"name": name, "status": "pending", "result": None} for name in TASK_NAMES]
    progress_agent.save_progress(progress_path, tasks)
    tasks = await progress_agent.run_one_task_and_persist(client, progress_path, tasks, 0)

    assert tasks[0]["status"] == "done"
    assert tasks[1]["status"] == "pending"
    assert client.provider.call_count == 1

    # "Restart": a fresh call to run_long_horizon_agent must resume from
    # task 2, never re-running the already-completed task 1.
    client.provider.add_text("Result for task 2")
    client.provider.add_text("Result for task 3")
    # No response scripted for task 1 -- if it were wrongly re-run, the mock
    # provider would raise AssertionError for running out of script before
    # ever reaching the real assertions below.

    result = await progress_agent.run_long_horizon_agent(client, progress_path, TASK_NAMES)

    assert all(task["status"] == "done" for task in result["tasks"])
    assert result["tasks"][0]["result"] == "Result for task 1"
    assert result["tasks"][1]["result"] == "Result for task 2"
    assert result["tasks"][2]["result"] == "Result for task 3"
    assert client.provider.call_count == 3  # 1 from before the "crash" + 2 after resume


async def test_run_long_horizon_agent_initializes_a_fresh_progress_file(
    progress_agent, client, progress_path
):
    for _ in TASK_NAMES:
        client.provider.add_text("done")

    await progress_agent.run_long_horizon_agent(client, progress_path, TASK_NAMES)

    persisted = progress_agent.load_progress(progress_path)
    assert [task["name"] for task in persisted] == TASK_NAMES
