from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4

@dataclass(frozen=True)
class Document:
    id: UUID
    number: str
    date: datetime
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