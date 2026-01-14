from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID, uuid4

from core.domain.account import Account

@dataclass(frozen=True)
class AccountingEntry:
    id: UUID
    document_id: UUID
    organization_id: UUID

    account: Account
    amount: Decimal
    budgeting_code: str
    flow_code: str
    target_code: str

    @staticmethod
    def create(
        document_id: UUID,
        organization_id: UUID,
        account: Account,
        amount: Decimal,
        budgeting_code: str,
        flow_code: str,
        target_code: str
    ) -> "AccountingEntry":
        
        if amount == Decimal("0"):
            raise ValueError

        for name, value in {
            "budgeting_code": budgeting_code,
            "flow_code": flow_code,
            "target_code": target_code
        }.items():
            if not value.strip():
                raise ValueError(f"{name} is required")
        
        return AccountingEntry(
            id=uuid4(),
            document_id=document_id,
            organization_id=organization_id,
            account=account,
            amount=amount,
            budgeting_code=budgeting_code.strip(),
            flow_code=flow_code.strip(),
            target_code=target_code.strip(),
        )