from dataclasses import dataclass
from typing import List

from core.domain.accounting_entry import AccountingEntry

@dataclass(frozen=True)
class PostingResult:
    entries: List[AccountingEntry]
    