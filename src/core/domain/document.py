from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4

@dataclass(frozen=True, kw_only=True)
class Document:
    id: UUID = field(default_factory=uuid4)
    number: str
    date: datetime = field(default_factory=datetime.utcnow)
    organization_id: UUID

    @staticmethod
    def create(number: str, organization_id: UUID) -> "Document":
        if not number.strip():
            raise ValueError("Document number is required")
        
        return Document(
            id=uuid4(),
            number=number.strip(),
            date=datetime.now(),
            organization_id=organization_id
        )