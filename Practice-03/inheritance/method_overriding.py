class Animal:
    def sound(self):
        print("Animal sound")

class Dog(Animal):
    def sound(self):
        print("Dog barks")

a = Animal()
d = Dog()

a.sound()
d.sound()




# overriding with different behavior
class Vehicle:
    def move(self):
        print("Vehicle moves")

class Car(Vehicle):
    def move(self):
        print("Car drives")

v = Vehicle()
c = Car()

v.move()
c.move()




class Shape:
    def draw(self):
        print("Drawing shape")

class Circle(Shape):
    def draw(self):
        print("Drawing circle")

c = Circle()
c.draw()



class Animal:
    def speak(self):
        print("Animal speaks")

    def introduce(self):
        self.speak()

class Cat(Animal):
    def speak(self):
        print("Meow")

c = Cat()
c.introduce()
