from datetime import datetime, timezone

from app.database.database import SessionLocal
from app.database.models import AgentSessionModel


class PostgresSessionStore:

    def save_session(
        self,
        session_id: str,
        service_session_id: str,
    ):
        with SessionLocal() as db:

            existing = db.get(
                AgentSessionModel,
                session_id
            )

            if existing:
                existing.service_session_id = service_session_id
                existing.updated_at = datetime.now(timezone.utc)

            else:
                db.add(
                    AgentSessionModel(
                        session_id=session_id,
                        service_session_id=service_session_id,
                    )
                )

            db.commit()

    def get_service_session_id(
        self,
        session_id: str,
    ):
        with SessionLocal() as db:

            record = db.get(
                AgentSessionModel,
                session_id
            )

            if record is None:
                return None

            return record.service_session_id