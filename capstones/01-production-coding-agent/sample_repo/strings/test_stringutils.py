from stringutils import reverse, shout


def test_shout():
    assert shout("hello") == "HELLO"


def test_reverse():
    assert reverse("hello") == "olleh"
