from dataclasses import dataclass
from abc import ABC, abstractmethod
from core.domain.basic_classes import JournalEntry
from typing import List

@dataclass(frozen=True)
class PostingResult:
    entries: List[JournalEntry]

class Postable(ABC):

    @abstractmethod
    def post(self) -> PostingResult:
        """Generate accounting entries according to legal rules."""
        pass

    