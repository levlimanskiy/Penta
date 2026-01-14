from enum import Enum

class EntrySide(str, Enum):
    DEBIT = 'debit'
    CREDIT = 'credit'
    