
def smallest_num(a,b,c):
    num1=a
    num2=b
    num3=c
    smallest = 0
    if num1 <= num2 and num1 <= num3:
        smallest = num1
    if num2 <= num1 and num2 <= num3:
        smallest = num2
    if num3 <= num1 and num3 <= num2:
        smallest = num3
    print(f"{smallest} is the smallest of three numbers.")
    return smallest
