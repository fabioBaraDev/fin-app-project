import enum
import uuid
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


class AccountCategoryDomain(enum.Enum):
    A = "A"
    B = "B"
    C = "C"


@dataclass
class AccountDomain:
    name: str
    type: AccountCategoryDomain
    id: uuid.UUID = uuid.uuid4()
    balance: Decimal = 0
    created_at: str = datetime.now()
