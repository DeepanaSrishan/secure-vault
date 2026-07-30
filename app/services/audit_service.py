from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog


def create_log(
    user_id: int,
    action: str,
    db: Session
):

    log = AuditLog(
        user_id=user_id,
        action=action
    )

    db.add(log)
    db.commit()

    return log