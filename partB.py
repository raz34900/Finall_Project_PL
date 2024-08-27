
############################################
# Question 1: Fibonacci Sequence Generator #
############################################

# Implement a Fibonacci sequence generator using a single lambda expression that
# returns a list of the first n Fibonacci numbers. The function should take n as an input.

from functools import reduce


def fibGen(n):
    return (lambda fib: [fib(i) for i in range(n)])(lambda fib: fib if fib<=1 else fibGen(n-1)[fib-1]+fibGen(n-1)[fib-2])

# explanation:
# (lambda fib: [fib(i) for i in range(n)]) - this lambda function creates a list of the first n fibonacci numbers
# (lambda fib: fib if fib<=1 - this lambda function returns 0 if fib is 0 and 1 if fib is 1
# fibGen(n-1)[fib-1] - this is the i-1 fibonacci number from the list of the first n-1 fibonacci numbers
# fibGen(n-1)[fib-2] - this is the i-2 fibonacci number from the list of the first n-1 fibonacci numbers



############################################
# Question 2: concatenation                #
############################################

# Write the shortest Python program, that accepts a list of strings and return a
# single string that is a concatenation of all strings with a space between them. Do not
# use the "join" function. Use lambda expressions. 

def concat(lst):
    return (lambda lst: (lambda concat: concat(lst)) (lambda lst: lst[0] if len(lst)==1 else lst[0] + " " + concat(lst[1:])))(lst)

# explanation:
# (lambda lst: (lambda concat: concat(lst)) - this lambda function returns the result of the lambda function concat
# (lambda lst: lst[0] if len(lst)==1 else lst[0] + " " + concat(lst[1:])) - this lambda function returns the concatenation 
# of the first element of the list and the result of the lambda function concat with the rest of the list


############################################
# Question 3: sum of squares               #
############################################

# Write a Python function that takes a list of lists of numbers and return a new list
# containing the cumulative sum of squares of even numbers in each sublist. Use at
# least 5 nested lambda expressions in your solution. 

def sumOfSquares(lst):
    return list(map(
        lambda sublist: sum(
            map(lambda x: (lambda y: y ** 2)(x), 
                filter(lambda x: (lambda z: z % 2 == 0)(x), 
                    map(lambda x: (lambda y: y)(x), sublist)
                )
            )
        ),
        map(lambda x: (lambda y: y)(x), lst)
    ))

# map applies a lambda to each sublist in list_of_lists.
# Each sublist is first processed by an identity lambda (lambda y: y)(x) which simply returns the sublist itself—this is a technique to add extra lambdas artificially.
# The filter function has a nested lambda (lambda z: z % 2 == 0)(x) which checks if numbers are even.
# The filtered numbers are then processed by another map, where each even number is passed through another identity lambda before being squared by a nested lambda (lambda y: y ** 2)(x).
# Another identity lambda (lambda y: y)(x) wraps the entire list_of_lists in the outer map.


############################################
# Question 4: cumulative operation         #
############################################

# Write a higher-order function that takes a binary operation (as a lambda function)
# and returns a new function that applies this operation cumulatively to a sequence.
# Use this to implement both factorial and exponentiation functions.

def cumulative_operation(operation):
    """ Returns a new function that applies a binary operation cumulatively to a sequence. """
    def apply_operation(sequence):
        result = sequence[0]
        for element in sequence[1:]:
            result = operation(result, element)
        return result
    return apply_operation
    

def exponent(base, power):
    return cumulative_operation(lambda x, y: x * y)([base] * power)


############################################
# Question 5:  rewrite into single line    #
############################################

# Rewrite the following program in one line by using nested filter, map and reduce functions:
def original():
    nums = [1,2,3,4,5,6]
    evens = []
    for num in nums:
        if num % 2 == 0:
            evens.append(num)
        
    squared = []
    for even in evens:
        squared.append(even**2)

    sum_squared = 0

    for x in squared:
        sum_squared += x
    print(sum_squared)

def single_line(nums):
    return reduce(lambda x, y: x + y, map(lambda x: x**2, filter(lambda x: x % 2 == 0, nums)))


############################################
#            Main and tests                #
############################################

def main():
    
    #### Q1 ####
    #n = 1
    #print(fibGen(n))



    #### Q2 ####
    # print(concat(["Hello", "world"]))  # Output: "Hello world"
    # print(concat(["Never", "trust", "Raz", ",", "she", "lies"]))  # Output: "Never trust Raz , she lies"



    #### Q3 ####
    # lst1 = []
    # print(sumOfSquares(lst1)) # Expected output: []
    # lst2 = [[2, 4, 6]]
    # print(sumOfSquares(lst2))# Expected output: [56]
    # lst3 = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]
    # print(sumOfSquares(lst3))# Output will be [20, 100, 244]
    # lst4 = [[1, 3, 5], [2, 4, 6], [7, 8, 9]]
    # print(sumOfSquares(lst4))# Output will be [0, 56, 64]


    #### Q4 ####    
    # factorial = cumulative_operation(lambda x, y: x * y)
    # factorial_result = factorial(range(1, 6))
    # print("Factorial of 5:", factorial_result) # Expected output: 120

    # exponent_result = exponent(3, 4)
    # print("3 raised to the power of 4:", exponent_result) # Expected output: 81

    #### Q5 ####
    nums = [1, 2, 3, 4, 5, 6]
    result = single_line(nums)
    print(result)  # Output: 56
    original()

    # Test case 2
    nums = [2, 4, 6, 8, 10]
    result = single_line(nums)
    print(result)  # Output: 220

    # Test case 3
    nums = [1, 3, 5, 7, 9]
    result = single_line(nums)
    print(result)  # Output: 0
    
if __name__ == "__main__":
    main()


