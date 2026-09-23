from numberutils import find_max, find_min


def test_find_min():
    assert find_min([3, 1, 2]) == 1


def test_find_max():
    assert find_max([3, 1, 2]) == 3
