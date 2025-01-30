import uuid
from abc import ABC
from typing import List

from fin_app.domain.entities import TransferDomain
from fin_app.presentation.api.adapters.serializers.transaction_serializer import (
    TransactTransferSerializer,
)


class TransactionServiceInterface(ABC):

    def get_all(self) -> list[TransferDomain]:
        pass

    def get_by_account_id(self, id: uuid.UUID) -> List[TransferDomain]:
        pass

    def create(self, data: TransactTransferSerializer):
        pass

    def cancel_by_transfer_id(self, id: uuid.UUID):
        pass
