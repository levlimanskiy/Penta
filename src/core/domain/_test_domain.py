
from decimal import Decimal
from datetime import datetime

from core.domain.organization import Organization
from core.domain.transaction import Transaction
from core.domain.account import Account
from core.domain.accounting_entry import AccountingEntry
from core.domain.document import Document
from core.domain.entry_side import EntrySide
from core.domain.ledger import Ledger
from core.domain.doc_types.payment_order import PaymentOrder

org = Organization.create("УД П РФ")

cash_account = Account(
    code="5 201 11-1",
    name="Денежные средства учреждения"
)

expense_account = Account(
    code="5 401 20-272",
    name="Расходы на приобретение оборудования"
)


po = PaymentOrder(
    number='666666',
    organization_id=org.id,
    amount=Decimal('150000.00'),
    expense_account=expense_account,
    cash_account=cash_account,
    budgeting_code="0000 00000000 243",
    flow_code="225",
    target_code="02-01"
)

posting = po.post()
Ledger.validate_double_entry(posting.entries)
print("Ledger validation passed")
print('Payment order posted automatically:')
for e in posting.entries:
    print(e)