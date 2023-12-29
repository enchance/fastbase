from abc import ABC, abstractmethod


class IUser(ABC):
    async def has(self, data: str) -> bool:
        ...