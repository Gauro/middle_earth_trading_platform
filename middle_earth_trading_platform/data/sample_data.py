# data/sample_data.py
from datetime import datetime

from middle_earth_trading_platform.database.DBSession import SessionLocal
from middle_earth_trading_platform.database.Schemas import User, Inventory, Offers


def create_dummy_data():
    session = SessionLocal()

    users = [
        User(username="Gandalf", race="wizard", created_at=datetime.now(), updated_at=datetime.now()),
        User(username="Legolas", race="elf", created_at=datetime.now(), updated_at=datetime.now()),
        User(username="Galandriel", race="elf", created_at=datetime.now(), updated_at=datetime.now()),
        User(username="Thorin", race="dwarf", created_at=datetime.now(), updated_at=datetime.now()),
        User(username="Bofur", race="dwarf", created_at=datetime.now(), updated_at=datetime.now()),
        User(username="Bifur", race="dwarf", created_at=datetime.now(), updated_at=datetime.now()),
        User(username="Saruman", race="wizard", created_at=datetime.now(), updated_at=datetime.now()),
        User(username="Elrond", race="dwarf", created_at=datetime.now(), updated_at=datetime.now()),
        User(username="Frodo", race="hobbit", created_at=datetime.now(), updated_at=datetime.now())
    ]

    session.add_all(users)
    session.commit()

    user_ids = [user.id for user in users]
    # Create dummy inventory items
    inventory_items = [
        Inventory(user_id=user_ids[0], weapon_name="staff", quantity=5),
        Inventory(user_id=user_ids[0], weapon_name="axe", quantity=5),
        Inventory(user_id=user_ids[0], weapon_name="bow", quantity=5),
        Inventory(user_id=user_ids[1], weapon_name="bow", quantity=5),
        Inventory(user_id=user_ids[1], weapon_name="axe", quantity=5),
        Inventory(user_id=user_ids[1], weapon_name="sword", quantity=5),
        Inventory(user_id=user_ids[2], weapon_name="staff", quantity=10)
    ]
    session.add_all(inventory_items)
    session.commit()

    offer = Offers(sender_id=user_ids[0], receiver_id=user_ids[1], sender_items={"staff": 2},
                   receiver_items={"sword": 2}, status='pending', created_at=datetime.now(),
                   updated_at=datetime.now())
    session.add(offer)
    session.commit()
    session.close()


create_dummy_data()
