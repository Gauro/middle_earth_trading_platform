from DBSession import SessionLocal
from Schemas import User, Inventory


def get_user_details(user_id: int):
    session = SessionLocal()
    user = session.query(User).filter(User.id == user_id).first()
    session.close()
    return user


def get_inventory_using_user_id(user_id: int):
    session = SessionLocal()
    inventory_details = session.query(Inventory).filter(Inventory.user_id == user_id).all()
    return inventory_details
