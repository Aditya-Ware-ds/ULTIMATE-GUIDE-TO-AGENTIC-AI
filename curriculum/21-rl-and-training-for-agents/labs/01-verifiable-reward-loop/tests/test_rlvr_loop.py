import math


def test_verify_math_answer_correct_candidate(rlvr_loop):
    assert rlvr_loop.verify_math_answer("2 + 2", 4) == 1.0


def test_verify_math_answer_incorrect_candidate(rlvr_loop):
    assert rlvr_loop.verify_math_answer("2 + 3", 4) == 0.0


def test_verify_math_answer_never_raises_on_malformed_candidate(rlvr_loop):
    # A reward-hacking-adjacent malformed candidate: syntactically invalid
    # code should score 0.0, never crash the reward computation.
    assert rlvr_loop.verify_math_answer("this is not python", 4) == 0.0


def test_verify_math_answer_never_raises_on_non_integer_output(rlvr_loop):
    assert rlvr_loop.verify_math_answer('"not a number"', 4) == 0.0


def test_group_relative_advantages_matches_the_grpo_formula(rlvr_loop):
    advantages = rlvr_loop.group_relative_advantages([1.0, 0.0, 1.0, 0.0])

    assert advantages == [1.0, -1.0, 1.0, -1.0]


def test_group_relative_advantages_handles_zero_std(rlvr_loop):
    advantages = rlvr_loop.group_relative_advantages([1.0, 1.0, 1.0])

    assert advantages == [0.0, 0.0, 0.0]


def test_group_relative_advantages_correct_candidates_score_higher(rlvr_loop):
    advantages = rlvr_loop.group_relative_advantages([1.0, 0.5, 0.0])

    assert advantages[0] > advantages[1] > advantages[2]
    # Advantages should be centered (mean approximately zero).
    assert math.isclose(sum(advantages), 0.0, abs_tol=1e-9)


def test_best_candidate_picks_the_highest_advantage(rlvr_loop):
    result = rlvr_loop.best_candidate(["a", "b", "c"], [-1.0, 2.0, 0.5])

    assert result == "b"


def test_run_verifiable_reward_loop_end_to_end(rlvr_loop):
    candidates = ["2 + 2", "2 * 2", "5", "0"]

    result = rlvr_loop.run_verifiable_reward_loop(candidates, target=4)

    assert result["rewards"] == [1.0, 1.0, 0.0, 0.0]
    assert result["best"] in ("2 + 2", "2 * 2")  # both correct, tie is fine
    assert len(result["advantages"]) == 4
    assert result["advantages"][0] > result["advantages"][2]  # correct beats incorrect
