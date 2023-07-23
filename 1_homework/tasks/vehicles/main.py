from vehicles import Car, Bicycle, Motorcycle


car = Car("BMW", "red")
car.move()
car.stop()
print(f"{car.model} {car.color}")
print("\n")

bicycle = Bicycle("7Star", "blue")
bicycle.move()
bicycle.stop()
print(f"{bicycle.model} {bicycle.color}")
print("\n")

motorcycle = Motorcycle("Mersedes", "black")
motorcycle.move()
motorcycle.stop()
print(f"{motorcycle.model} {motorcycle.color}")