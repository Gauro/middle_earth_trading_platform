# routes/user_routes.py
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from middle_earth_trading_platform.database.DBSession import SessionLocal
from middle_earth_trading_platform.database.Schemas import User, Inventory, Offers
from middle_earth_trading_platform.models.IO_Models import RespondToOffer

router = APIRouter()


@router.get("/get_all_user_details")
async def get_all_user_details():
    """
    Retrieve details of all users.

    Retrieves and returns the details of all users stored in the database.

    Returns:
    - List[Dict]: A list of dictionaries representing the details of all users.

    Raises:
    - HTTPException: Returns a 400 error if an exception occurs during processing.
    """
    try:

        session = SessionLocal()
        users = session.query(User).all()
        users = [user.to_dict() for user in users]
        session.close()
        return JSONResponse(status_code=200, content=users)

    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})


@router.get("/get_all_user_inventory")
async def get_all_user_inventory():
    """
    Retrieve inventory details of all users.

    Retrieves and returns the inventory details of all users stored in the database,
    including the username and a list of inventory items associated with each user.

    Returns:
    - Dict[int, Dict[str, Union[str, List[Dict]]]]: A dictionary mapping user IDs to dictionaries
      containing the username and inventory details for each user.

    Raises:
    - HTTPException: Returns a 400 error if an exception occurs during processing.
    """
    try:

        session = SessionLocal()
        users_inventory = {}
        users = session.query(User).all()
        for user in users:
            inventory_details = session.query(Inventory).filter(Inventory.user_id == user.id).all()
            inventory_details = [i.to_dict() for i in inventory_details]
            users_inventory[user.id] = {"username": user.username, "inventory": inventory_details}
        session.close()

        return JSONResponse(status_code=200, content=users_inventory)

    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})


@router.get("/users/{user_id}")
async def get_user(user_id: int):
    """
    Retrieve details of a specific user.

    Retrieves and returns the details of a user specified by the provided user ID.

    Parameters:
    - user_id (int): The unique identifier of the user.

    Returns:
    - Dict[str, Union[int, str]]: A dictionary representing the details of the user,
      including the user's ID and username.

    Raises:
    - HTTPException: Returns a 404 error if the user with the specified ID is not found.
    - HTTPException: Returns a 400 error if an exception occurs during processing.
    """
    try:
        session = SessionLocal()
        user = session.query(User).filter(User.id == user_id).first()
        session.close()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        # return user
        return JSONResponse(status_code=200, content=user.to_dict())

    except HTTPException as http_exc:
        return JSONResponse(status_code=http_exc.status_code, content={"error": http_exc.detail})
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})


@router.get("/users/{user_id}/user_inventory")
async def get_user_inventory(user_id: int):
    """
    Retrieve inventory details of a specific user.

    Retrieves and returns the inventory details of the user specified by the provided user ID.

    Parameters:
    - user_id (int): The unique identifier of the user.

    Returns:
    - List[Dict[str, Union[int, str]]]: A list of dictionaries representing the inventory details
      associated with the specified user, including the weapon name and quantity.

    Raises:
    - HTTPException: Returns a 404 error if either the user or the inventory details are not found.
    - HTTPException: Returns a 400 error if an exception occurs during processing.
    """
    try:
        session = SessionLocal()
        inventory_details = session.query(Inventory).filter(Inventory.user_id == user_id).all()
        if not inventory_details:
            user = session.query(User).filter(User.id == user_id).first()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            else:
                raise HTTPException(status_code=404, detail="Inventory details not found for the user")
        inventory_details = [i.to_dict() for i in inventory_details]
        return JSONResponse(status_code=200, content=inventory_details)

    except HTTPException as http_exc:
        return JSONResponse(status_code=http_exc.status_code, content={"error": http_exc.detail})
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})


@router.get("/users/{user_id}/get_offers")
async def get_user_offers(user_id: int):
    """

    Retrieves and returns a list of offers received by the user with the specified ID.

    Parameters:
    - user_id (int): The ID of the user for whom to retrieve offers.

    Returns:
    - JSONResponse: A JSON response containing a list of offers received by the user.
                    Each offer is represented as a dictionary.

    Raises:
    - HTTPException: Returns a 404 error if the user with the specified ID is not found.
                     Returns a 400 error for other exceptions encountered during processing.
    """
    try:

        session = SessionLocal()
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        offers = session.query(Offers).filter(Offers.receiver_id == user_id).all()
        offers = [offer.to_dict() for offer in offers]

        return JSONResponse(status_code=200, content=offers)

    except HTTPException as http_exc:
        return JSONResponse(status_code=http_exc.status_code, content={"error": http_exc.detail})

    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})


@router.post("/users/respond_to_offer")
async def respond_to_offer(request: RespondToOffer):
    """
    Respond to an offer with acceptance or rejection.

    This endpoint allows a user to respond to a specific offer with either acceptance or rejection.
    The response will update the status of the offer accordingly and may trigger inventory updates
    for both the sender and receiver of the offer.

    Parameters:
    - user_id (int): The ID of the user responding to the offer.
    - offer_id (int): The ID of the offer being responded to.
    - response (str): The response to the offer, which must be either 'accept' or 'reject'.

    Returns:
    - JSONResponse: A JSON response indicating the success or failure of the operation.

    Raises:
    - HTTPException: Returns a 401 error if the User is unauthorized to perform this action.
    - HTTPException: Returns a 404 error if the User or the offer is not found.
    - HTTPException: Returns a 400 error if the response is not 'accept' or 'reject', or if any
      other exception occurs during processing.
    """
    try:

        session = SessionLocal()
        sender = session.query(User).filter(User.id == request.user_id).first()
        if not sender:
            raise HTTPException(status_code=404, detail="User not found")

        offer = session.query(Offers).filter(Offers.offer_id == request.offer_id).first()
        if not offer:
            raise HTTPException(status_code=404, detail="Offer not found")

        if offer.receiver_id != request.user_id:
            raise HTTPException(status_code=401, detail="User not authorized to perform this action")

        if offer.status != 'pending':
            raise HTTPException(status_code=401, detail="User not authorized to perform this action")

        if request.response.lower() not in ['accept', 'reject']:
            raise HTTPException(status_code=400, detail="Invalid response. Must be 'accept' or 'reject'")

        if request.response.lower() == 'accept':
            # Update offer status
            offer.status = "accepted"

            # Update inventories for both sender and receiver
            # 1. receiver items
            for item, offer_qty in offer.receiver_items.items():
                # add to senders inventory
                sender_inventory = session.query(Inventory).filter(
                    (Inventory.user_id == offer.sender_id) & (Inventory.weapon_name == item)).first()
                if sender_inventory:
                    sender_inventory.quantity = sender_inventory.quantity + offer_qty
                else:
                    new_inventory = Inventory(user_id=offer.sender_id, weapon_name=item, quantity=offer_qty)
                    session.add(new_inventory)

                # remove from receiver's inventory
                receiver_inventory = session.query(Inventory).filter(
                    (Inventory.user_id == offer.receiver_id) & (Inventory.weapon_name == item)).first()
                if receiver_inventory:
                    receiver_inventory.quantity = receiver_inventory.quantity - offer_qty
                else:
                    raise HTTPException(status_code=400, detail=f"Receiver does not have {item} to barter. "
                                                                f"Please submit renewed offer.")

            # 2. sender items
            for item, offer_qty in offer.sender_items.items():
                # add to senders inventory
                sender_inventory = session.query(Inventory).filter(
                    (Inventory.user_id == offer.sender_id) & (Inventory.weapon_name == item)).first()
                if sender_inventory:
                    sender_inventory.quantity = sender_inventory.quantity - offer_qty
                else:
                    raise HTTPException(status_code=400, detail=f"Sender does not have {item} to barter. "
                                                                f"Please submit renewed offer.")

                # remove from receiver's inventory
                receiver_inventory = session.query(Inventory).filter(
                    (Inventory.user_id == offer.receiver_id) & (Inventory.weapon_name == item)).first()
                if receiver_inventory:
                    receiver_inventory.quantity = receiver_inventory.quantity + offer_qty
                else:
                    new_inventory = Inventory(user_id=offer.receiver_id, weapon_name=item, quantity=offer_qty)
                    session.add(new_inventory)

            session.commit()
            session.close()

            return JSONResponse(status_code=200, content={"data": "Offer accepted successfully"})
        else:
            # Update offer status
            offer.status = "rejected"
            session.commit()
            session.close()
            return JSONResponse(status_code=200, content={"data": "Offer rejected successfully"})

    except HTTPException as http_exc:
        return JSONResponse(status_code=http_exc.status_code, content={"error": http_exc.detail})

    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})
