from fastapi import APIRouter
from loguru import logger
from pydantic import BaseModel

from app.services.idempotent_service import idempotent_api


router = APIRouter()


class PaymentInfo(BaseModel):
    sender_id: str
    receiver_id: str
    amount: float
    description: str


@router.post('/pay')
def pay(request: PaymentInfo):
    # Get the JSON payload from the request
    payment_info = request.model_dump_json()

    logger.info(f'Payment request received: {payment_info}')
    response = idempotent_api.make_request(payment_info)
    logger.info(f'Payment response: {response}')
    return response

