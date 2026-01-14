from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

from core.domain.account import Account
from core.domain.document import Document
from core.domain.journal_entry import JournalEntry
from core.domain.postable import Postable
from core.domain.posting_result import PostingResult

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