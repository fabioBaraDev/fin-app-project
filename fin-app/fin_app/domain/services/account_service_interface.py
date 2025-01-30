from abc import ABC
from typing import List

from fin_app.domain.entities import AccountDomain


class AccountServiceInterface(ABC):

    def get_all(self) -> List[AccountDomain]:
        pass

    def get_by_id(self, id) -> AccountDomain:
        pass

    def create(self, data) -> AccountDomain:
        pass
