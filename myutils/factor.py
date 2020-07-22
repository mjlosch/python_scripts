def factor(n):
    """Compute prime factors of n
    
    Usage: factor(n)
    """
    import numpy
    #
    # 0. extract factors of 2
    #
    factors = []
    while n/2 == n/2.:
        n = n/2
        factors.append(2)
    #
    # 1. Create an array of trial values
    #
    a = numpy.ceil(numpy.sqrt(n))
    lim = min(n,10 ** 6)
    a = numpy.arange(a, a + lim)
    b2 = a ** 2 - n
    #
    # 2. Check whether b is a square
    #
    fractions = numpy.modf(numpy.sqrt(b2))[0]
    #
    # 3. Find 0 fractions
    #
    indices = numpy.where(fractions == 0)
    #
    # 4. Find the first occurence of a 0 fraction
    #
    a = numpy.ravel(numpy.take(a, indices))[0]
    a = int(a)
    b = numpy.sqrt(a ** 2 - n)
    b = int(b)
    c = a + b
    d = a - b
    #
    if c == 1 or d == 1:
        return factors
    factors.append(c)
    factors.append(d)
    print(c, d)
    factor(c)
    factor(d)

    return factors

def factors(n):    
    from functools import reduce
    return set(reduce(list.__add__, 
                      ([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0)))
