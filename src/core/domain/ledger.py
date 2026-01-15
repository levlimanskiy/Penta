from decimal import Decimal
from typing import Iterable

from core.domain.basic_classes import JournalEntry

class Ledger:

    @staticmethod
    def validate(entries: Iterable[JournalEntry]) -> None:
        if not entries:
           raise ValueError("Ledger cannot be empty")
       
        total_debit = sum(e.amount for e in entries)
        total_credit = sum(e.amount for e in entries)
