from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import UUID, uuid4

@dataclass(frozen=True)
class Transaction:
    id: UUID
    organization_id: UUID
    amount: Decimal
    timestamp: datetime
    description: str

    @staticmethod
    def create(
        organization_id: UUID,
        amount: Decimal,
        description: str
    ) -> "Transaction":
        
        if amount == Decimal('0'):
            raise ValueError("Zero transaction")
        
        if not description.strip():
            raise ValueError("Transaction description is required")

        return Transaction(
            id=uuid4(),
            organization_id=organization_id,
            amount=amount,
            timestamp=datetime.now(),
            description=description.strip()
        )
        
