from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.ticket import Ticket
from app.schemas.ticket import (
    TicketCreate,
    TicketUpdate,
)

router = APIRouter()


# DATABASE
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========================
# CREATE TICKET
# =========================
@router.post("/admin")
def create_ticket(
    data: TicketCreate,
    db: Session = Depends(get_db),
):
    ticket = Ticket(**data.dict())

    db.add(ticket)
    db.commit()
    db.refresh(ticket)

    return ticket


# =========================
# GET ALL TICKETS
# =========================
@router.get("/")
def get_tickets(
    db: Session = Depends(get_db),
):
    return db.query(Ticket).all()


# =========================
# SEARCH TICKETS
# =========================
@router.get("/search")
def search_tickets(
    q: str,
    db: Session = Depends(get_db),
):
    tickets = (
        db.query(Ticket)
        .filter(
            Ticket.to_airport.ilike(f"%{q}%")
        )
        .all()
    )

    return tickets


# =========================
# UPDATE TICKET
# =========================
@router.put("/admin/{id}")
def update_ticket(
    id: int,
    data: TicketUpdate,
    db: Session = Depends(get_db),
):
    ticket = (
        db.query(Ticket)
        .filter(Ticket.id == id)
        .first()
    )

    if not ticket:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found",
        )

    for key, value in data.dict(
        exclude_unset=True
    ).items():
        setattr(ticket, key, value)

    db.commit()
    db.refresh(ticket)

    return ticket


# =========================
# DELETE TICKET
# =========================
@router.delete("/admin/{id}")
def delete_ticket(
    id: int,
    db: Session = Depends(get_db),
):
    ticket = (
        db.query(Ticket)
        .filter(Ticket.id == id)
        .first()
    )

    if not ticket:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found",
        )

    db.delete(ticket)
    db.commit()

    return {
        "message": "Ticket deleted"
    }# =========================
# GET SINGLE TICKET
# =========================
@router.get("/{id}")
def get_ticket(
    id: int,
    db: Session = Depends(get_db),
):

    ticket = (
        db.query(Ticket)
        .filter(Ticket.id == id)
        .first()
    )

    if not ticket:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    return ticket