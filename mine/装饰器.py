def call_counter(function):
    count = 0

    def inner():
        function()
        nonlocal count
        count += 1
        return count

    return inner

@call_counter
def my_function():
    print("Function called")

for i in range(5):
    print(my_function())