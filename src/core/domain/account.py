from dataclasses import dataclass

@dataclass(frozen=True)
class Account:
    code: str
    name: str

    def __post_init__(self):
        if not self.code.strip():
            raise ValueError("Account code cannot be empty")