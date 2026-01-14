from dataclasses import dataclass
from uuid import UUID, uuid4


@dataclass(frozen=True)
class Organization:
    id: UUID
    name: str
    parent_id: UUID | None = None

    @staticmethod
    def create(name: str, parent_id: UUID | None = None) -> "Organization":
        if not name.strip():
            raise ValueError("Organization name cannot be empty")
        
        return Organization(
            id=uuid4(),
            name=name.strip(),
            parent_id=parent_id
        )
        