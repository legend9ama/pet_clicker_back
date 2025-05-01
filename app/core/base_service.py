from abc import ABC

class BaseService(ABC):
    def __init__(self, repo):
        self.repo = repo