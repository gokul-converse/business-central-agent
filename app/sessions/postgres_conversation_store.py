from datetime import datetime, timezone

from sqlalchemy import select

from app.database.database import SessionLocal
from app.database.models import ConversationMessageModel


class PostgresConversationStore:
    def save_message(
        self,
        session_id: str,
        role: str,
        content: str,
    ):
        with SessionLocal() as db:
            message = ConversationMessageModel(
                session_id=session_id,
                role=role,
                content=content,
                created_at=datetime.now(timezone.utc),
            )

            db.add(message)
            db.commit()

    def get_messages(
    self,
    session_id: str,
    limit: int = 10,
):
        with SessionLocal() as db:
            statement = (
                select(ConversationMessageModel)
                .where(
                    ConversationMessageModel.session_id == session_id
                )
                .order_by(
                    ConversationMessageModel.created_at.desc(),
                    ConversationMessageModel.id.desc(),
                )
                .limit(limit)
            )

            records = db.execute(statement).scalars().all()

            # Newest messages were fetched first.
            # Reverse them for chronological order.
            records.reverse()

            return [
                {
                    "role": record.role,
                    "content": record.content,
                }
                for record in records
            ]