import random

def get_random_number(a, b):
    return random.randint(a, b)

sum=0
a,b,c,d=map(int, input().split())

for i in range(1000):
    x=get_random_number(a, b)
    y=get_random_number(c, d)
    if x>y:
        sum+=1
print(sum/1000) 
