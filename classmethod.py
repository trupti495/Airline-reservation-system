# methods declared inside class only acess using dot opeartor
# three way 1 class 2 instance 3 static

# class methods need @classmethods and cls as the argument
# A class method is a method that belongs to the class rather than a specific object. It 
# uses the @classmethod decorator and takes cls (class) as its first parameter.
# They can be called using the class name or an object.

class student:
    c_name="abc"

    # class method
    @classmethod
    def change_c(cls):
        return "class method"
    
    @classmethod
    def change_c1(cls,new_name):
        cls.c_name=new_name
        return  f"Value updated {cls.c_name}"
    
# call has 2 way
# 1way using class name    
print(student.change_c())    

# 2way using object
s1=student()
print(s1.change_c1("linkcode"))
