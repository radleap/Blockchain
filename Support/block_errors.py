#------------------------
def myFunc(int_in):
    return int_in/5
print("function only output", myFunc(100))

#------------------------
# class myClass:
#     oneval = 17
#
# C = myClass()
# print(C.oneval)

#------------------------
# class myClass:
#     oneval = 17
#     def div(self, int_in): #need self to invoke
#         return(int_in/self.oneval)
# C = myClass()
# C.oneval = 5 #reseting the instance variable from 17 to 5
# print(C.div(150))

# -----------------------
class myClass:
    oneval = 17 #class attribute accessed with myClass_instance.oneval
    def __init__(self, inval): #constructor immediately set the value of inval
        self.oneval = inval
    def div(self, input): #need self to invoke
        return(input/self.oneval)

# C = myClass(4) # set inval to 4
# B = myClass(10) # set inval to 10
# print(C.div(34)) #
# print(B.div(34))
# -------------------------- inheritance
# class newClass(myClass): #uses functionality of myClass
#     name = 'Ben'

# N = newClass(12)
# print(N.name)
# print(N.div(36))

# -------------------------- inheritance with error catching

# class myClass:
#     oneval = 17 #class attribute accessed with myClass_instance.oneval
#     def __init__(self, inval): #constructor immediately set the value of inval
#         self.oneval = inval
#     def div(self, input): #need self to invoke
#         try:
#             return(input/self.oneval)
#         except:
#             print("Must pass integer to div")
#             return(0)
class myClass:
    oneval = 17 #class attribute accessed with myClass_instance.oneval
    def __init__(self, inval): #constructor immediately set the value of inval
        self.oneval = inval
    def div(self, input): #need self to invoke
        try:
            return(input/self.oneval)
        except TypeError:
            print("Must pass integer to div")
            return(0)
        except:
            print("Unknown error in Div")

class newClass(myClass): #uses functionality of myClass
    name = 'Ben'
    def __repr__(self): #gets invoken when try to print "representation"
        #name = 'Ben' #local data not need self
        return(self.name + ": onval is equal to " + str(self.oneval))

N = newClass(12)
print(N.name)
print(N.div(36))
print(N.div('afsga'))
