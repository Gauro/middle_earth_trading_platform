from pydantic import BaseModel


class RespondToOffer(BaseModel):
    user_id: int
    offer_id: int
    response: str


class CreateOffer(BaseModel):
    user_id: int
    receiver_id: int
    sender_items: dict
    receiver_items: dict
