from dataclasses import dataclass
from typing import List

from core.domain.journal_entry import JournalEntry

@dataclass(frozen=True)
class PostingResult:
    entries: List[JournalEntry]
    