from dataclasses import dataclass, field
from decimal import Decimal
from uuid import UUID, uuid4
from datetime import datetime
from typing import Optional

from core.domain.basic_classes import *
from core.domain.posting import *
# главный тип - договор с поставщиком
@dataclass(frozen=True)
class ContractPayable(Document):
    organization_id: UUID    
    payment_account: BankAccount | TreasuryAccount       
    valid_until: datetime           # срок действия
    subject: str                    # предмет договора
    subdiv: str                     # подразделение
    executor: str                   # исполнитель
    treasury_account_id: TreasuryAccount       # наш счёт


    @staticmethod
    def create(
        number: str,
        date: datetime,
        organization_id: UUID,
        payment_account: BankAccount | TreasuryAccount, 
        valid_until: datetime,
        subject: str,
        subdiv: str,
        executor: str,
        treasury_account_id: TreasuryAccount,
    ) -> "ContractPayable":
        doc = Document.create(number, organization_id)
        if not number.strip():
            raise ValueError("Contract number is required")

        if valid_until < date:
            raise ValueError("Contract validity date cannot be earlier than contract date")

        if not subject.strip():
            raise ValueError("Contract subject is required")

        if not executor.strip():
            raise ValueError("Executor is required")

        return ContractPayable(
            id=doc.id,
            number=doc.number.strip(),
            date=date,
            organization_id=organization_id,
            payment_account=payment_account,
            valid_until=valid_until,
            subject=subject.strip(),
            subdiv=subdiv.strip(),
            executor=executor.strip(),
            treasury_account_id=treasury_account_id,
        )

# закрывающий документ
@dataclass(frozen=True)
class CompletionDocument(Document):
    contract_id: UUID
    amount: Decimal
    description: str
    document_type: str
    acceptance_date: datetime

    @staticmethod
    def create(
        number: str,
        contract_id: UUID,
        amount: Decimal,
        description: str,
        document_type: str,
        acceptance_date: datetime,
        organization_id: UUID
    ) -> "CompletionDocument":
        
        doc = Document.create(number, organization_id)

        if not document_type.strip():
            raise ValueError("Document type required")
        if acceptance_date > datetime.now():
            raise ValueError("Acceptance date cannot be in the future")

        return CompletionDocument(
            id=doc.id, 
            number=doc.number,
            date=datetime.now(),
            organization_id=organization_id,
            contract_id=contract_id,
            amount=amount.quantize(Decimal('0.01')),
            description=description.strip(),
            document_type=document_type.strip(),
            acceptance_date=acceptance_date,
        )

# платёжное поручение (расход) - зкр
@dataclass(frozen=True)
class PaymentOrder(Document, Postable):
    amount: Decimal
    expense_account: Account
    cash_account: Account
    budgeting_code: str
    flow_code: str
    target_code: str

    def post(self) -> PostingResult:
        if self.amount == Decimal('0'):
            raise ValueError("Payment must be nonnegative")

        entry = JournalEntry.create(
            document_id=self.id,
            organization_id=self.organization_id,
            debit_account=self.expense_account,
            credit_account=self.cash_account,
            amount=self.amount,
            budgeting_code=self.budgeting_code,
            flow_code=self.flow_code,
            target_code=self.target_code
        )
        return PostingResult(entries=[entry])