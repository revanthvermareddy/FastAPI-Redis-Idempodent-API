import stripe

from app.settings import stripe_settings


stripe.api_key = stripe_settings.secret_key


class StripeService:
    
    @staticmethod
    def create_session(data: dict):
        return stripe.checkout.Session.create(
            line_items=[
                {
                    'price': data['priceId'],
                    'quantity': 1,
                },
            ],
            payment_method_types=stripe_settings.payment_method_types.split(','),
            mode=stripe_settings.mode,
            success_url=stripe_settings.success_url,
            cancel_url=stripe_settings.cancel_url,
        )