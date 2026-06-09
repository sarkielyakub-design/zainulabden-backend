from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.api.deps import get_db

from app.models.contact import ContactMessage

from app.api.deps import require_admin

from pydantic import BaseModel


router = APIRouter()


# =========================
# SCHEMA
# =========================
class ContactCreate(BaseModel):

    name: str
    email: str
    phone: str
    message: str


# =========================
# SEND MESSAGE
# =========================
@router.post("/send-message")
def send_message(
    data: ContactCreate,
    db: Session = Depends(get_db),
):

    new_message = ContactMessage(
        name=data.name,
        email=data.email,
        phone=data.phone,
        message=data.message,
    )

    db.add(new_message)

    db.commit()

    db.refresh(new_message)

    return {
        "success": True,
        "message": "Message sent successfully"
    }


# =========================
# ADMIN GET MESSAGES
# =========================
@router.get("/admin/messages")
def get_messages(
    db: Session = Depends(get_db),
    admin=Depends(require_admin),
):

    messages = (
        db.query(ContactMessage)
        .order_by(
            ContactMessage.created_at.desc()
        )
        .all()
    )

    return {
        "success": True,
        "total": len(messages),
        "data": messages,
    }