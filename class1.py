# oops in py
# polymorphism
# abstraction
# inheritance 
# encapsulation 


# class 
class Student:
    def show(self):
        print("Hello, I am a student")

# Create object
s1 = Student()

# Call method
s1.show()

# class using default constructor
class clg:
    c_name="abc"
    def change_name(self):
        self.c_name="xyz"
        print(self.c_name)

s2=clg()
s2.change_name()        

# class using parametrized constructor

class clg1:
    c_name="abc"
    def change_name(self,new_name):
        self.c_name=new_name
        print(self.c_name)

s3=clg1()
s3.change_name("gpa")   