from functools import reduce

# 1.) Implement a Fibonacci sequence generator using a single lambda expression that
# returns a list of the first n Fibonacci numbers. The function should take n as an input.

fibGen = lambda n: (lambda fib: [fib(i) for i in range(n)])(lambda fib: fib if fib <= 1 else fibGen(n - 1)[fib - 1] + fibGen(n - 1)[fib - 2])
print(fibGen(6))  # Output: [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

# explanation:
# (lambda fib: [fib(i) for i in range(n)]) - this lambda function creates a list of the first n fibonacci numbers
# (lambda fib: fib if fib<=1 - this lambda function returns 0 if fib is 0 and 1 if fib is 1
# fibGen(n-1)[fib-1] - this is the i-1 fibonacci number from the list of the first n-1 fibonacci numbers
# fibGen(n-1)[fib-2] - this is the i-2 fibonacci number from the list of the first n-1 fibonacci numbers

# 2.) Write the shortest Python program, that accepts a list of strings and return a
# single string that is a concatenation of all strings with a space between them. Do not
# use the "join" function. Use lambda expressions.

lst = ['Vlad', 'Raz', 'Roi']
concat = lambda lst: '' if not lst else lst[0] + ' ' + concat(lst[1:])
print(concat(lst)) # Output: Vlad Raz Roi

# 3.) Write a Python function that takes a list of lists of numbers and return a new list
# containing the cumulative sum of squares of even numbers in each sublist. Use at
# least 5 nested lambda expressions in your solution

def cumulative_sum_of_squares(lst):
    return list(map(lambda sublist:
                    sum(map(lambda x:
                            (lambda y: y ** 2)(x),
                            filter(lambda z: z % 2 == 0, sublist))),lst))

numbers = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
print(cumulative_sum_of_squares(numbers))  # Output: [4, 52, 64]

# 4.) Write a higher-order function that takes a binary operation (as a lambda function)
# and returns a new function that applies this operation cumulatively to a sequence.
# Use this to implement both factorial and exponentiation functions.

def cumulative_operation(operation):
    return lambda seq: seq[0] if len(seq) == 1 else operation(seq[0], cumulative_operation(operation)(seq[1:]))
factorial = lambda n: cumulative_operation(lambda x, y: x * y)(range(1, n + 1))
exponentiation = lambda base, exp: cumulative_operation(lambda x, y: x * y)([base] * exp)
print(factorial(5))        # 120 (5!)
print(exponentiation(2, 4))  # 16 (4^2)

# 5.) Rewrite the following program in one line by using nested filter, map and reduce functions
#nums = [1,2,3,4,5,6]
#evens = []
#for num in nums:
#    if num % 2 == 0:
#    evens.append(num)
#squared = []
#for even in evens:
#    squared.append(even**2)
#sum_squared = 0
#for x in squared:
#    sum_squared += x
#print(sum_squared)

print(reduce(lambda x, y: x + y, map(lambda x: x ** 2, filter(lambda x: x % 2 == 0, [1, 2, 3, 4, 5, 6]))))  # Output: 56

# 6.) Write one-line function that accepts as an input a list of lists containing strings
# and returns a new list containing the number of palindrome strings in each sublist.
# Use nested filter / map / reduce functions.

print(list(map(lambda x: len(list(filter(lambda y: y == y[::-1], x))), [['madam', 'hello', 'world'], ['level', 'radar']])))# Output: [1, 2]

# 7.) Explain the term "lazy evaluation" in the context of the following program:

# def generate_values():
# print('Generating values...')
# yield 1 \\\\\\\\\\\\\\YIELD - Delays the evaluation of an expression until its value is actually needed
# yield 2
# yield 3

# def square(x):
# print(f'Squaring {x}')
# return x * x

# print('Eager evaluation:')
# values = list(generate_values()) \\\\\\\\\\\\\\LIST OF YIELD VALUES
# squared_values = [square(x) for x in values] \\\\\\\\\\\\\\SQUARE OF YIELD VALUES
# print(squared_values) \\\\\\\\\\\\\\PRINT SQUARE OF YIELD VALUES
# print('\nLazy evaluation:') \\\\\\\\\\\\\\PRINT LAZY EVALUATION
# squared_values = [square(x) for x in generate_values()] \\\\\\\\\\\\\\SQUARE OF YIELD VALUES
# print(squared_values) \\\\\\\\\\\\\\PRINT SQUARE OF YIELD VALUES

# Lazy evaluation is a strategy that delays the evaluation of an expression until its value is actually needed. In the context of the program above,
# the eager evaluation approach first generates all values using the generate_values() function and then squares each value using the square() function. This means that all values are generated and squared before being printed.

# 8.)  Write a one-line Python function that takes a list of integers and returns a new list
# containing only the prime numbers, sorted in descending order. Use lambda
# expressions and list comprehensions.

print(sorted(list(filter(lambda x: all(x % i != 0 for i in range(2, int(x ** 0.5) + 1)), [2, 3, 4, 5, 6, 7, 8, 9])), reverse=True))  # Output: [7, 5, 3, 2]


