from inventory import total_price


def test_total_price():
    assert total_price(2.5, 4) == 10.0


def test_total_price_zero_quantity():
    assert total_price(3.0, 0) == 0.0
