from abc import ABC
from app.core.base_repository import BaseRepository

class BaseService(ABC):
    def __init__(self, repo: BaseRepository):
        self.repo = repo