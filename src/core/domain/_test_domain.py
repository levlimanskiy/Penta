from decimal import Decimal
from core.domain.organization import Organization
from core.domain.transaction import Transaction

org = Organization.create("УД П РФ")

tx = Transaction.create(
    organization_id=org.id,
    amount=Decimal("15000.00"),
    description="Закупка оборудования"
)

print(org)
print(tx)