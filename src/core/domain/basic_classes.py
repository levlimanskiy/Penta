from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4
from decimal import Decimal
from enum import Enum

"""Понятие документа """        
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

"""Организации, реквизиты организаций"""
# тип организаций (важно для бюджетной бухгалтерии)
class OrganizationType(Enum):
    TREASURY = '01'
    BUDGET_INSTITUTION = '02'
    STATE_ENTERPRISE = '03'
    OTHER_NONFINANCIAL_ENTERPRISE = '04'
    OTHER_FINANCIAL_ENTERPRISE = '05'
    NONCOMMERCIAL_IP = '06'
    PHYS = '07'
    INTERNATIONAL_ENTERPRISES = '08'
    NONRESIDENTS = '09'

# сам класс организации
@dataclass(frozen=True)
class Organization:
    id: UUID
    name: str
    inn: str
    kpp: str
    org_type: OrganizationType

    @staticmethod
    def create(name: str, 
               inn: str,
               kpp: str,
               org_type: OrganizationType
               ) -> "Organization":
        # checks
        if not (name.strip() or inn.strip()):
            raise ValueError("Organization name cannot be empty")
        if not inn.isdigit() or len(inn) not in (10, 12):
            raise ValueError("Invalid INN")
        if not kpp.isdigit() or len(kpp) != 9:
            raise ValueError("Invalid KPP")
        
        return Organization(
            id=uuid4(),
            name=name.strip(),
            inn=inn,
            kpp=kpp,
            org_type=org_type
        )

# реквизиты организации: коммерческий банк
@dataclass(frozen=True)
class BankAccount:
    id: UUID
    organization_id: UUID
    account_number: str
    bank_name: str
    bik: str
    corr_account: str | None
    payment_text: str | None

    @staticmethod
    def create(
        organization_id: UUID,
        account_number: str,
        bank_name: str,
        bik: str,
        corr_account: str | None = None,
        payment_text: str | None = None
    ) -> "BankAccount":
        
         if not account_number.strip():
            raise ValueError("Account number required")

         if not bik.isdigit() or len(bik) != 9:
            raise ValueError("Invalid BIK")
         
         return BankAccount(
             
             id=uuid4(),
             organization_id=organization_id,
             account_number=account_number,
             bank_name=bank_name,
             bik=bik,
             corr_account=corr_account,
             payment_text=payment_text
        )

# реквизиты организации: бюджет
@dataclass(frozen=True)
class TreasuryAccount:
    id: UUID
    organization_id: UUID
    account_number: str
    bank_name: str
    bik: str
    kbk: str
    oktmo: str
    personal_account: str
    treasury_account: str | None
    payment_text: str | None

    @staticmethod
    def create(
        organization_id: UUID,
        account_number: str,
        bank_name: str,
        bik: str,
        kbk: str,
        oktmo: str,
        personal_account: str,
        treasury_account: str | None = None,
        payment_text: str | None = None
    ) -> "TreasuryAccount":
         
         if not personal_account.strip():
            raise ValueError("Personal account (лицевой счёт) required")
         if not kbk.isdigit() or len(kbk) != 20:
            raise ValueError("Invalid KBK")
         if not oktmo.isdigit() or len(oktmo) not in (8, 11):
            raise ValueError("Invalid OKTMO")
         if not account_number.strip():
            raise ValueError("Account number required")
         if not bik.isdigit() or len(bik) != 9:
            raise ValueError("Invalid BIK")
         
         return TreasuryAccount(
             id=uuid4(),
             organization_id=organization_id,
             account_number=account_number,
             bank_name=bank_name,
             bik=bik,
             kbk=kbk,
             oktmo=oktmo,
             personal_account=personal_account,
             treasury_account=treasury_account,
             payment_text=payment_text
        )


"""Бухгалтерские данные"""
# бухгалтерский счёт
@dataclass(frozen=True)
class Account:
    code: str
    name: str

    def __post_init__(self):
        if not self.code.strip():
            raise ValueError("Account code cannot be empty")

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

