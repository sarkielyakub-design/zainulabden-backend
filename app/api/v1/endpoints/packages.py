from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.package import Package
from app.schemas.package import PackageOut

router = APIRouter()


# =========================
# GET ALL PACKAGES
# =========================
@router.get("", response_model=dict)
def get_packages(
    db: Session = Depends(get_db)
):
    packages = (
        db.query(Package)
        .order_by(Package.created_at.desc())
        .all()
    )

    serialized_packages = [
        PackageOut.model_validate(
            package,
            from_attributes=True
        )
        for package in packages
    ]

    return {
        "success": True,
        "count": len(serialized_packages),
        "data": serialized_packages,
    }

# =========================
# SEARCH PACKAGES
# =========================
@router.get("/search")
def search_packages(
    q: str,
    db: Session = Depends(get_db),
):

    packages = (
        db.query(Package)
        .filter(
            Package.title.ilike(f"%{q}%")
        )
        .all()
    )

    return packages
# =========================
# GET SINGLE PACKAGE
# =========================
@router.get(
    "/{package_id}",
    response_model=PackageOut
)
def get_package(
    package_id: int,
    db: Session = Depends(get_db)
):
    package = (
        db.query(Package)
        .filter(Package.id == package_id)
        .first()
    )

    if not package:
        raise HTTPException(
            status_code=404,
            detail="Package not found",
        )

    return PackageOut.model_validate(
        package,
        from_attributes=True
    )