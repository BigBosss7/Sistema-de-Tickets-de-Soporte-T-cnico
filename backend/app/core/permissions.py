from fastapi import Depends, HTTPException 

from app.models.user import User
from app.core.security import get_current_user 

def require_supervisor(
    current_user: User = Depends(get_current_user)
):

    if current_user.role != "SUPERVISOR":
        raise HTTPException(
            status_code=403,
            detail="Supervisor access required"
        )

    return current_user


def require_technician(
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "TECHNICIAN":
        raise HTTPException(
            status_code=403,
            detail="Technician access required"
        )

    return current_user

def require_technician_or_supervisor(
    current_user: User = Depends(get_current_user)
):
    if current_user.role not in [
        "TECHNICIAN",
        "SUPERVISOR"
    ]:
      raise HTTPException(
           status_code=403,
           detail="Technician or supervisor acces required"
      )

    return current_user 