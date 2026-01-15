from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

from core.domain.basic_classes import Account, Document, JournalEntry
from core.domain.posting import Postable, PostingResult

# платёжное поручение - зкр
@dataclass(frozen=True, kw_only=True)
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