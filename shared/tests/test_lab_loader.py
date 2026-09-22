import pytest

from shared.testing.lab_loader import load_lab_module


@pytest.fixture
def fake_lab(tmp_path):
    for target, value in (("starter", "starter_value"), ("solution", "solution_value")):
        target_dir = tmp_path / target
        target_dir.mkdir()
        (target_dir / "thing.py").write_text(f'VALUE = "{value}"\n')
    return tmp_path


def test_defaults_to_solution(monkeypatch, fake_lab):
    monkeypatch.delenv("LAB_TARGET", raising=False)

    module = load_lab_module(fake_lab, "thing")

    assert module.VALUE == "solution_value"


def test_loads_starter_when_env_set(monkeypatch, fake_lab):
    monkeypatch.setenv("LAB_TARGET", "starter")

    module = load_lab_module(fake_lab, "thing")

    assert module.VALUE == "starter_value"


def test_invalid_target_raises(monkeypatch, fake_lab):
    monkeypatch.setenv("LAB_TARGET", "not-a-real-target")

    with pytest.raises(ValueError):
        load_lab_module(fake_lab, "thing")


def test_missing_file_raises(monkeypatch, fake_lab):
    monkeypatch.delenv("LAB_TARGET", raising=False)

    with pytest.raises(FileNotFoundError):
        load_lab_module(fake_lab, "does_not_exist")
