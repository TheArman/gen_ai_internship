from abc import ABC, abstractmethod


class Vehicle(ABC):

    def __init__(self, model, color):
        self._model = model
        self._color = color

    @abstractmethod
    def move(self):
        Ellipsis

    @abstractmethod
    def stop(self):
        Ellipsis

    @property
    def model(self):
        return self._model

    @property
    def color(self):
        return self._color


class Car(Vehicle):

    def move(self):
        print("Car is moving...")

    def stop(self):
        print("Car stopped...")


class Bicycle(Vehicle):

    def move(self):
        print("Bicycle is moving...")

    def stop(self):
        print("Bicycle stopped...")


class Motorcycle(Vehicle):

    def move(self):
        print("Motorcycle is moving...")

    def stop(self):
        print("Motorcycle stopped...")