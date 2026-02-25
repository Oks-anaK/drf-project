import stripe

from config import settings

stripe.api_key = settings.STRIPE_API_KEY


def create_stripe_product(name):
    """Создает продукт в страйпе."""

    return stripe.Product.create(name=name)


def create_stripe_price(amount, product_id):
    """Создает цену в страйпе."""

    return stripe.Price.create(
        currency="rub",
        unit_amount=int(amount * 100),
        product=product_id,
    )


def create_stripe_session(price):
    """Создает сессию на оплату в страйпе."""

    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",
        line_items=[{"price": price.id, "quantity": 1}],
        mode="payment",
    )
    return session.id, session.url
