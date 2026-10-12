def make_counter():
    count=0
    def counter():
        nonlocal count
        count+=1
        return count
    return counter
counting=make_counter()
for i in range(10):
    print(counting())