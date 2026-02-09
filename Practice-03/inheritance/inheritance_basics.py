class Animal:
    def speak(self):
        print("Animal makes a sound")

class Dog(Animal):
    pass

d = Dog()
d.speak()



class Animal:
    def eat(self):
        print("Animal eats")

class Cat(Animal):
    def meow(self):
        print("Meow")

c = Cat()
c.eat()
c.meow()



class Person:
    species = "Human"

class Student(Person):
    pass

s = Student()
print(s.species)




class Vehicle:
    def __init__(self, brand):
        self.brand = brand

class Car(Vehicle):
    pass

c = Car("Toyota")
print(c.brand)



class Person:
    def greet(self):
        print("Hello")

class Teacher(Person):
    def teach(self):
        print("Teaching...")

t = Teacher()
t.greet()
t.teach()
