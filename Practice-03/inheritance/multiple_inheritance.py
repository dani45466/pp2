class Fly:
    def fly(self):
        print("Flying")

class Swim:
    def swim(self):
        print("Swimming")

class Duck(Fly, Swim):
    pass

d = Duck()
d.fly()
d.swim()




class Printer:
    def action(self):
        print("Printing")

class Scanner:
    def action(self):
        print("Scanning")

class Device(Printer, Scanner):
    def action(self):
        print("Printing and scanning")


d = Device()
d.action()



