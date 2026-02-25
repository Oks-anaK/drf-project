import stripe

from config import settings
from forex_python.converter import CurrencyRates

stripe.api_key = settings.STRIPE_API_KEY

def convert_rub_to_dollars(amount):
    """Конвертирует рубли в доллары."""

    c = CurrencyRates()
    rate = c.get_rate('RUB', 'USD')
    return int(amount * rate)


def create_stripe_product(name):
    """Создает продукт в страйпе."""

    return stripe.Product.create(name=name)



def create_stripe_price(amount, product_id):
    """Создает цену в страйпе."""

    return stripe.Price.create(
        currency="usd",
        unit_amount=amount * 100,
        product=product_id,
    )


def create_stripe_session(price):
    """Создает сессию на оплату в страйпе."""

    session = stripe.checkout.Session.create(
        success_url="https://127.0.0.1:8000/",
        line_items=[{"price": price.id, "quantity": 1}],
        mode="payment",
    )
    return session.id, session.url
