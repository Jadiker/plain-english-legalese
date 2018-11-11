import pickle

class MyObj:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c
        
me = MyObj("hi", "medium", "goodbye")

# with open("hello", "wb+") as f:
#     pickle.dump(me, f)

with open("hello", "rb") as f:
    new_me = pickle.load(f)
    print(new_me.a)
    print(new_me.b)
    print(new_me.c)
    
# 
# f = open("hello", "rb+")
# # use file
# f.close()
# # file closed
# 
# 
# with open("hello", "rb+") as f:
#     # use file
# # file closed
    
