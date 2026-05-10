from sqlalchemy import Column, Integer, String, Float, DateTime
from app.db.base import Base


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)

    airline = Column(String, nullable=False)

    from_airport = Column(String, nullable=False)

    to_airport = Column(String, nullable=False)

    departure_date = Column(String)

    return_date = Column(String)

    price = Column(Float)

    seat_class = Column(String)

    image = Column(String)

    description = Column(String)