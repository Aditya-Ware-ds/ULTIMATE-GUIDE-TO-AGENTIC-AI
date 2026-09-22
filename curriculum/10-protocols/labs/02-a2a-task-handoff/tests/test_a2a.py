import pytest


def test_task_starts_submitted(a2a):
    task = a2a.Task(id="t1")

    assert task.state == a2a.TaskState.SUBMITTED
    assert task.history == []


def test_start_work_without_input_goes_to_working(a2a):
    task = a2a.Task(id="t1")

    task = a2a.start_work(task, needs_input=False)

    assert task.state == a2a.TaskState.WORKING
    assert task.history == ["submitted -> working"]


def test_start_work_with_input_goes_to_input_required(a2a):
    task = a2a.Task(id="t1")

    task = a2a.start_work(task, needs_input=True)

    assert task.state == a2a.TaskState.INPUT_REQUIRED


def test_start_work_raises_if_not_submitted(a2a):
    task = a2a.Task(id="t1", state=a2a.TaskState.WORKING)

    with pytest.raises(ValueError):
        a2a.start_work(task, needs_input=False)


def test_provide_input_transitions_to_working(a2a):
    task = a2a.Task(id="t1", state=a2a.TaskState.INPUT_REQUIRED)

    task = a2a.provide_input(task)

    assert task.state == a2a.TaskState.WORKING


def test_provide_input_raises_if_not_awaiting_input(a2a):
    task = a2a.Task(id="t1", state=a2a.TaskState.WORKING)

    with pytest.raises(ValueError):
        a2a.provide_input(task)


def test_complete_sets_result_and_state(a2a):
    task = a2a.Task(id="t1", state=a2a.TaskState.WORKING)

    task = a2a.complete(task, "done!")

    assert task.state == a2a.TaskState.COMPLETED
    assert task.result == "done!"


def test_complete_raises_if_not_working(a2a):
    task = a2a.Task(id="t1")

    with pytest.raises(ValueError):
        a2a.complete(task, "done!")


def test_fail_sets_result_and_state(a2a):
    task = a2a.Task(id="t1", state=a2a.TaskState.WORKING)

    task = a2a.fail(task, "something broke")

    assert task.state == a2a.TaskState.FAILED
    assert task.result == "something broke"


def test_is_terminal(a2a):
    assert a2a.is_terminal(a2a.Task(id="t1", state=a2a.TaskState.COMPLETED))
    assert a2a.is_terminal(a2a.Task(id="t1", state=a2a.TaskState.FAILED))
    assert a2a.is_terminal(a2a.Task(id="t1", state=a2a.TaskState.CANCELED))
    assert not a2a.is_terminal(a2a.Task(id="t1", state=a2a.TaskState.WORKING))
    assert not a2a.is_terminal(a2a.Task(id="t1", state=a2a.TaskState.SUBMITTED))


def test_delegate_task_full_flow_with_clarification(a2a):
    task = a2a.delegate_task("t1", "do something vague", needs_clarification_check=lambda r: True)
    assert task.state == a2a.TaskState.INPUT_REQUIRED

    task = a2a.provide_input(task)
    assert task.state == a2a.TaskState.WORKING

    task = a2a.complete(task, "clarified and done")
    assert task.state == a2a.TaskState.COMPLETED
    assert task.history == [
        "submitted -> input-required",
        "input-required -> working",
        "working -> completed",
    ]


def test_delegate_task_full_flow_without_clarification(a2a):
    task = a2a.delegate_task("t2", "a clear request", needs_clarification_check=lambda r: False)
    assert task.state == a2a.TaskState.WORKING

    task = a2a.complete(task, "done directly")
    assert task.state == a2a.TaskState.COMPLETED
