from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Enum, func

from middle_earth_trading_platform.database.DBSession import Base


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, index=True)
    race = Column(String, index=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "race": self.race,
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at)
        }


class Inventory(Base):
    __tablename__ = 'inventory'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    weapon_name = Column(String, unique=True, index=True)
    quantity = Column(Integer, index=True)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "weapon_name": self.weapon_name,
            "quantity": str(self.quantity)
        }


class Offers(Base):
    __tablename__ = 'offers'
    offer_id = Column(Integer, primary_key=True, autoincrement=True)
    sender_id = Column(Integer, ForeignKey('user.id'))
    receiver_id = Column(Integer, ForeignKey('user.id'))
    sender_items = Column(JSON)
    receiver_items = Column(JSON)
    status = Column(Enum('pending', 'accepted', 'rejected', name='offer_status'))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    def to_dict(self):
        return {
            "offer_id": self.offer_id,
            "sender_id": self.sender_id,
            "receiver_id": self.receiver_id,
            "sender_items": self.sender_items,
            "receiver_items": self.receiver_items,
            "status": self.status,
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at),
        }
