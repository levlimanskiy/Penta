from decimal import Decimal
from typing import Iterable

from core.domain.journal_entry import JournalEntry

class Ledger:

    @staticmethod
    def validate(entries: Iterable[JournalEntry]) -> None:
       if not entries:
           raise ValueError("Ledger cannot be empty")