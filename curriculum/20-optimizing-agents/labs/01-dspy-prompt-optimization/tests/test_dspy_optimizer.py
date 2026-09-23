import pytest

pytest.importorskip("dspy")


def test_scripted_lm_answers_known_questions(dspy_optimizer, knowledge_base):
    lm = dspy_optimizer.configure_scripted_lm(knowledge_base)
    program = dspy_optimizer.build_program()

    result = program(question="What is the capital of France?")

    assert result.answer == "Paris"
    assert len(lm.calls) == 1  # dspy.JSONAdapter avoids ChatAdapter's fallback retry


def test_exact_match_metric_is_case_insensitive(dspy_optimizer):
    import dspy

    example = dspy.Example(question="q", answer="Paris")
    correct = dspy.Prediction(answer="paris")
    wrong = dspy.Prediction(answer="Tokyo")

    assert dspy_optimizer.exact_match_metric(example, correct) is True
    assert dspy_optimizer.exact_match_metric(example, wrong) is False


def test_build_trainset_creates_examples_with_question_as_input(dspy_optimizer, knowledge_base):
    trainset = dspy_optimizer.build_trainset(knowledge_base)

    assert len(trainset) == len(knowledge_base)
    assert {example.question for example in trainset} == set(knowledge_base.keys())
    assert set(trainset[0].inputs().keys()) == {"question"}


def test_optimize_program_bootstraps_real_demonstrations(dspy_optimizer, knowledge_base):
    dspy_optimizer.configure_scripted_lm(knowledge_base)
    program = dspy_optimizer.build_program()
    trainset = dspy_optimizer.build_trainset(knowledge_base)

    optimized = dspy_optimizer.optimize_program(program, trainset)

    # Proof optimization genuinely happened, not just that .compile() ran:
    # real bootstrapped few-shot demos, selected because they passed the metric.
    assert len(optimized.demos) >= 1
    for demo in optimized.demos:
        assert demo.answer == knowledge_base[demo.question]


def test_optimized_program_still_answers_correctly(dspy_optimizer, knowledge_base):
    dspy_optimizer.configure_scripted_lm(knowledge_base)
    program = dspy_optimizer.build_program()
    trainset = dspy_optimizer.build_trainset(knowledge_base)
    optimized = dspy_optimizer.optimize_program(program, trainset)

    result = optimized(question="What is the capital of France?")

    assert result.answer == "Paris"
