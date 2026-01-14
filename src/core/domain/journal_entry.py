from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID, uuid4

from core.domain.account import Account

@dataclass(frozen=True)
class JournalEntry:
    id: UUID
    document_id: UUID
    organization_id: UUID

    debit_account: Account
    credit_account: Account
    amount: Decimal

    budgeting_code: str
    flow_code: str
    target_code: str

    @staticmethod
    def create(
        document_id: UUID,
        organization_id: UUID,
        debit_account: Account,
        credit_account: Account,
        amount: Decimal,
        budgeting_code: str,
        flow_code: str,
        target_code: str
    ) -> "JournalEntry":
        
        if debit_account == credit_account:
            raise ValueError('Debit and credit accounts must differ')
        
        if amount == Decimal("0"):
            raise ValueError("Amount must be nonzero")

        for name, value in {
            "budgeting_code": budgeting_code,
            "flow_code": flow_code,
            "target_code": target_code
        }.items():
            if not value.strip():
                raise ValueError(f"{name} is required")
        
        return JournalEntry(
            id=uuid4(),
            document_id=document_id,
            organization_id=organization_id,
            debit_account=debit_account,
            credit_account=credit_account,
            amount=amount,
            budgeting_code=budgeting_code.strip(),
            flow_code=flow_code.strip(),
            target_code=target_code.strip(),
        )