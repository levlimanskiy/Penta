
from decimal import Decimal
from datetime import datetime

from core.domain.basic_classes import Organization, Account, JournalEntry, Document
from core.domain.ledger import Ledger
from core.domain.docs_types import PaymentOrder

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
Ledger.validate(posting.entries)
print("Ledger validation passed")
print('Payment order posted automatically:')
for e in posting.entries:
    print(e)