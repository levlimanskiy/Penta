
from decimal import Decimal
from datetime import datetime

from core.domain.basic_classes import * 
from core.domain.ledger import Ledger
from core.domain.docs_types import *


org_us = Organization.create(
    name="ФГБУ УЭЗВОВ УД П РФ",
    inn='7710036332',
    kpp='771001001',
    org_type=OrganizationType.BUDGET_INSTITUTION
)

our_acc = TreasuryAccount.create(
    organization_id=org_us.id,
    account_number='40102810545370000003',
    bank_name='ОКЦ №1 ГУ Банка России по ЦФО',
    bik='004525988',
    kbk='00000000000000000243',
    oktmo='12345678',
    personal_account='2173X28800',
    treasury_account='0321466430000000017300',
    payment_text='УФК по г.Москве'
)

org_counter = Organization.create(
    name="ФГУП ППП УД П РФ",
    inn='7710142570',
    kpp='771001001',
    org_type=OrganizationType.STATE_ENTERPRISE
)

org_acc = BankAccount.create(
    organization_id=org_counter.id,
    account_number='405028104000000000311',
    bank_name='ПАО ПСБ',
    bik='044525555',
    corr_account='301018104000000555',
    payment_text='ФГУП ППП'
)

contract = ContractPayable.create(
    number='Д1630-УПП/25',
    date=datetime.fromisoformat("2025-12-19"),
    organization_id=org_counter.id,
    payment_account=org_acc,
    valid_until=datetime.fromisoformat('2025-12-31'),
    subject='Поставка товара',
    subdiv='Дирекция Дом Правительства',
    executor='Карсанов Е.П.',
    treasury_account_id=our_acc
)

completion = CompletionDocument.create(
    number="Акт-1/26",
    contract_id=contract.id,
    amount=Decimal('10000.00'),
    description="Выполнение работ по поставке",
    document_type="Акт выполненных работ",
    acceptance_date=datetime(2026, 1, 15),
    organization_id=org_us.id,
)

print(contract)
print(completion)