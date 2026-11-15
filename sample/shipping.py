"""Small controlled target: shipping fee in dollars for a nonnegative subtotal."""


def shipping_fee(subtotal):
    return 0 if subtotal >= 50 else 5
