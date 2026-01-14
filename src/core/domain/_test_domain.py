from decimal import Decimal

from core.domain.organization import Organization
from core.domain.transaction import Transaction
from core.domain.account import Account
from core.domain.accounting_entry import AccountingEntry
from core.domain.document import Document

org = Organization.create("УД П РФ")

tx = Transaction.create(
    organization_id=org.id,
    amount=Decimal("15000.00"),
    description="Закупка оборудования"
)

cash_account = Account(
    code="5 201 11-1",
    name="Денежные средства учреждения"
)

expense_account = Account(
    code="5 401 20-272",
    name="Расходы на приобретение оборудования"
)

document = Document.create(
    number = "ПП-001/2026",
    organization_id=org.id
)

entry_debit = AccountingEntry.create(
    document_id = document.id,
    organization_id=org.id,
    account=expense_account,
    amount=Decimal("150000.00"),
    budgeting_code="0000 00000000 243",
    flow_code="225",
    target_code="02-01"
)

entry_credit = AccountingEntry.create(
    document_id=document.id,
    organization_id=org.id,
    account=cash_account,
    amount=Decimal("-150000.00"),
    budgeting_code="0000 00000000 243",
    flow_code="225",
    target_code="02-01"
)

print("ORGANIZATION:")
print(org)
print("\nDOCUMENT:")
print(document)
print("\nENTRIES:")
print(entry_debit)
print(entry_credit)

