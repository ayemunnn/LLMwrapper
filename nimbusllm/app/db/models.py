from datetime import datetime
from sqlalchemy import String, Integer, Float, DateTime, Text, func
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base

class LLMRequestLog(Base):
    __tablename__ = "llm_request_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    request_id: Mapped[str] = mapped_column(String(32), unique=True, index=True)

    provider: Mapped[str] = mapped_column(String(32), index=True)
    model: Mapped[str] = mapped_column(String(128), index=True)

    prompt: Mapped[str] = mapped_column(Text)          # store last user msg or full prompt
    response_text: Mapped[str] = mapped_column(Text)   # store generated text

    input_tokens: Mapped[int] = mapped_column(Integer, default=0)
    output_tokens: Mapped[int] = mapped_column(Integer, default=0)

    latency_ms: Mapped[int] = mapped_column(Integer, default=0)
    status: Mapped[str] = mapped_column(String(16), default="success")  # success/fail
    error: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
