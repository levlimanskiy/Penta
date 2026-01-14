from abc import ABC, abstractmethod
from core.domain.posting_result import PostingResult

class Postable(ABC):

    @abstractmethod
    def post(self) -> PostingResult:
        """Generate accounting entries according to legal rules."""
        pass