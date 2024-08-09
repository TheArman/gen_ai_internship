from abc import ABC, abstractmethod
from interfaces import Database, FileBased


class StorageSystem(ABC):

    @abstractmethod
    def save(self):
        Ellipsis

    @abstractmethod
    def load(self):
        Ellipsis

    @abstractmethod
    def delete(self):
        Ellipsis


class FileBasedStorage(FileBased, StorageSystem):

    def save(self):
        print("Save in FileBased Storage...")

    def load(self):
        print("Load...")

    def delete(self):
        print("Delete from FileBased Storage...")

    def store(self):
        print("Store...")


class DatabaseStorage(Database, StorageSystem):

    def save(self):
        print("Save in Database...")

    def load(self):
        print("Load DB...")

    def delete(self):
        print("Delete from Database...")

    def store(self):
        print("Store(DB)...")