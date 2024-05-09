# routes/offer_routes.py
from datetime import datetime

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from middle_earth_trading_platform.database.DBSession import SessionLocal
from middle_earth_trading_platform.database.Schemas import User, Inventory, Offers
from middle_earth_trading_platform.models.IO_Models import CreateOffer

router = APIRouter()


# @router.get("/offers/all_offers")
# async def get_offer():
#     session = SessionLocal()
#     offers = session.query(Offers).all()
#     if not offers:
#         raise HTTPException(status_code=404, detail="Offer not found")
#     offers = [offer.to_dict() for offer in offers]
#     return offers

@router.post("/offers/create_offer")
# async def create_offer(user_id: int, sender_items: dict, receiver_id: int, receiver_items: dict):
async def create_offer(request: CreateOffer):
    """
    Create a new offer between two users.

    Creates a new offer where a user with the specified ID offers items to another user.
    The offer includes sender and receiver IDs along with items offered and requested.

    Parameters:
    - user_id (int): The ID of the user creating the offer.
    - sender_items (dict): A dictionary containing items offered by the sender and their quantities.
    - receiver_id (int): The ID of the user who will receive the offer.
    - receiver_items (dict): A dictionary containing items requested by the receiver and their quantities.

    Returns:
    - JSONResponse: A JSON response indicating the success or failure of the offer creation.

    Raises:
    - HTTPException: Returns a 404 error if the sender or receiver is not found.
                     Returns a 400 error if the sender or receiver lacks the required items or if any other exception occurs during processing.
    """
    try:
        session = SessionLocal()
        sender = session.query(User).filter(User.id == request.user_id).first()
        receiver = session.query(User).filter(User.id == request.receiver_id).first()
        if not sender or not receiver:
            raise HTTPException(status_code=404, detail="Sender or receiver not found")

        # Check if sender has the items to barter
        sender_inventory_details = session.query(Inventory).filter(Inventory.user_id == request.user_id).all()
        for item, quantity in request.sender_items.items():
            sender_inventory_item = list(filter(lambda x: x.weapon_name == item, sender_inventory_details))
            if sender_inventory_item:
                if sender_inventory_item[0].quantity < quantity:
                    raise HTTPException(status_code=400, detail=f"Sender does not have {quantity} {item} to barter")
            else:
                raise HTTPException(status_code=400, detail=f"Sender does not have {item} in inventory!")

        # Check if receiver has the items to barter
        receiver_inventory_details = session.query(Inventory).filter(Inventory.user_id == request.receiver_id).all()
        for item, quantity in request.receiver_items.items():
            receiver_inventory_item = list(filter(lambda x: x.weapon_name == item, receiver_inventory_details))
            if receiver_inventory_item:
                if receiver_inventory_item[0].quantity < quantity:
                    raise HTTPException(status_code=400, detail=f"Receiver does not have {quantity} {item} to barter")
            else:
                raise HTTPException(status_code=400, detail=f"Receiver does not have {item} in inventory!")

        # Create offer
        new_offer = Offers(sender_id=request.user_id,
                           receiver_id=request.receiver_id,
                           sender_items=request.sender_items,
                           receiver_items=request.receiver_items,
                           status='pending',
                           created_at=datetime.now(),
                           updated_at=datetime.now())

        session.add(new_offer)
        session.commit()
        session.close()

        return JSONResponse(status_code=200, content={"data": "success"})

    except HTTPException as http_exc:
        return JSONResponse(status_code=http_exc.status_code, content={"error": http_exc.detail})

    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})


@router.get("/offers/all_offers")
async def get_all_offers(sender_id: int = None, receiver_id: int = None, status: str = None):
    """
    Retrieve a list of offers based on optional filtering criteria.

    Retrieves a list of all offers matching the specified filtering criteria, such as sender ID,
    receiver ID, and status.

    Parameters:
    - sender_id (int, optional): Filter offers by the ID of the sender.
    - receiver_id (int, optional): Filter offers by the ID of the receiver.
    - status (str, optional): Filter offers by their status (e.g., 'pending', 'accepted', 'rejected').

    Returns:
    - List[Dict]: A list of dictionaries representing the matching offers.

    Raises:
    - HTTPException: Returns a 400 error for other exceptions encountered during processing.
    """
    try:
        session = SessionLocal()
        query = session.query(Offers)

        if sender_id is not None:
            query = query.filter(Offers.sender_id == sender_id)
        if receiver_id is not None:
            query = query.filter(Offers.receiver_id == receiver_id)
        if status is not None:
            query = query.filter(Offers.status == status)

        offers = query.all()

        offers = [offer.to_dict() for offer in offers]
        return JSONResponse(status_code=200, content=offers)

    except HTTPException as http_exc:
        return JSONResponse(status_code=http_exc.status_code, content={"error": http_exc.detail})
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})


@router.get("/offers/{offer_id}")
async def get_offer(offer_id: int):
    """
    Retrieve details of a specific offer by its ID.

    Retrieves and returns the details of the offer with the specified ID.

    Parameters:
    - offer_id (int): The ID of the offer to retrieve details for.

    Returns:
    - Offer: The details of the offer with the specified ID.

    Raises:
    - HTTPException: Returns a 404 error if the offer with the specified ID is not found.
                     Returns a 400 error for other exceptions encountered during processing.
    """
    try:
        session = SessionLocal()
        offer = session.query(Offers).filter(Offers.offer_id == offer_id).first()
        if not offer:
            raise HTTPException(status_code=404, detail="Offer not found")
        return offer
    except HTTPException as http_exc:
        return JSONResponse(status_code=http_exc.status_code, content={"error": http_exc.detail})
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})
