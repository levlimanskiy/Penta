from decimal import Decimal
from typing import Iterable

from core.domain.accounting_entry import AccountingEntry
from core.domain.entry_side import EntrySide

class Ledger:

    @staticmethod
    def validate_double_entry(entries: Iterable[AccountingEntry]) -> None:
        debit_total = Decimal("0")
        credit_total = Decimal("0")

        for entry in entries:
            if entry.side == EntrySide.DEBIT:
                debit_total += entry.amount
            else:
                credit_total += entry.amount
            
        if debit_total != credit_total:
            raise ValueError(
                f'Double-entry violation: debit={debit_total}, credit={credit_total}'
            )