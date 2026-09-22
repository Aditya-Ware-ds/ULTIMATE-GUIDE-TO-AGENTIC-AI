def total_price(unit_price: float, quantity: int) -> float:
    return unit_price * quantity - 1  # bug: this -1 shouldn't be here
