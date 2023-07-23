from abc import ABC, abstractmethod


class FileBased(ABC):

    @abstractmethod
    def store(self):
        Ellipsis


class Database(ABC):

    @abstractmethod
    def store(self):
        Ellipsis