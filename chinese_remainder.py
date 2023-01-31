
# китайская теория об остатков
def chinese_remainder(n, a):           
    sum = 0
    prod = 1
    for i in n:
        prod *= i
    for n_i, a_i in zip(n, a):
        p = prod // n_i
        sum += a_i * mul_inv(p, n_i) * p
    return sum % prod

 # расширенный алгоритм Евклида
def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1: 
        return 1
    while a > 1:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0: 
        x1 += b0
    return x1