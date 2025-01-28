from abc import ABC, abstractmethod

from fin_app.domain.entities import AccountDomain


class Mapper(ABC):
    @classmethod
    @abstractmethod
    def to_entity(cls, data):
        pass


class AccountMapper(Mapper):
    @classmethod
    def to_entity(cls, data):
        return AccountDomain(
            id=data.id,
            name=data.name,
            type=data.type,
            balance=data.balance,
            created_at=data.created_at,
        )
