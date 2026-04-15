
#! Divisor cannot be zero
def divide (dividend, divisor):
    if divisor == 0:
        raise ZeroDivisionError("Divisor cannot be zero")
    
    return dividend/divisor

# result = divide(10, 0)

# print(result)

grades = []

try:
    average = divide(sum(grades), len(grades))
except ZeroDivisionError as e:
    print("There are no grades yet in your list", e)
else: 
    print("The average grade is ", average)
finally:
    print("End of Calculation")

# except TypeError: 


students = [
    {"name": "Bob", "grades": [80, 85]},
    {"name": "Rolf", "grades": []},
    {"name": "Jen", "grades": [90, 95]}
]

print("====================== Students Grades ==========================")

for student in students:
    try:
        average = divide(sum(student["grades"]), len(student["grades"]))
    except ZeroDivisionError as e:
        print("[ERROR] There are no grades yet in your list", e)
    else: 
        print("The average grade is ", average)
    finally:
        print("End of Calculation for student ", student["name"])     