from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

from core.domain.account import Account
from core.domain.document import Document
from core.domain.entry_side import EntrySide
from core.domain.accounting_entry import AccountingEntry
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
        if self.amount <= Decimal('0'):
            raise ValueError("Payment must be positive")

        debit = AccountingEntry.create(
            document_id=self.id,
            organization_id=self.organization_id,
            account=self.expense_account,
            side=EntrySide.DEBIT,
            amount=self.amount,
            budgeting_code=self.budgeting_code,
            flow_code=self.flow_code,
            target_code=self.target_code
        )

        credit = AccountingEntry.create(
            document_id=self.id,
            organization_id=self.organization_id,
            account=self.cash_account,
            side=EntrySide.CREDIT,
            amount=self.amount,
            budgeting_code=self.budgeting_code,
            flow_code=self.flow_code,
            target_code=self.target_code
        )

        return PostingResult(entries=[debit, credit])