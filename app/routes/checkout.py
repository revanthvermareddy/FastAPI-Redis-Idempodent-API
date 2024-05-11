from fastapi import APIRouter
from pydantic import BaseModel

from app.services.stripe import StripeService

router = APIRouter()

class StripeCheckoutRequest(BaseModel):
    priceId: str

@router.post("/create-checkout-session")
def create_checkout_session(stripe_checkout_request: StripeCheckoutRequest):
    stripe_checkout_request_dict = stripe_checkout_request.dict()
    checkout_session = StripeService.create_session(stripe_checkout_request_dict)
    return {"sessionId": checkout_session["id"]}