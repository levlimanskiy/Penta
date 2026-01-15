from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4
from decimal import Decimal

# бухгалтерский счёт
@dataclass(frozen=True)
class Account:
    code: str
    name: str

    def __post_init__(self):
        if not self.code.strip():
            raise ValueError("Account code cannot be empty")
        
# родительский класс документов
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

# организации
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

# проводка
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

