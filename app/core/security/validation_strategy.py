from abc import ABC, abstractmethod

class ValidationStrategy(ABC):
    @abstractmethod
    async def validate(self, data: str) -> bool:
        pass