#!/usr/bin/env python
# -*- encoding: utf-8
"""
Some experiments in finding prime factors, inspired by reading
https://golem.ph.utexas.edu/category/2019/07/the_riemann_hypothesis_says_50.html

A chance to play with itertools.
"""

import collections
import itertools


def prime_factors(n):
    """Generate the prime factors of n."""
    def n_is_divisible_by(i):
        return n % i == 0

    i = 2
    while i * i <= n:
        if n_is_divisible_by(i):
            n //= i
            yield i
        else:
            i += 1

    if n > 1:
        yield n


def prod(iterable):
    """Multiply all the numbers in iterable together."""
    result = 1
    for i in iterable:
        result *= i
    return result


def divisors(n):
    """Generate the divisors of n."""
    pf = prime_factors(n)

    # The fundamental theorem of arithmetic states that any integer has
    # a prime factorisation which is unique, up to ordering.
    #
    # So we can decompose any number into a product of the form
    #
    #       n = p_1^k_1 * p_2^k_2 * ... p_i^k_i
    #
    # e.g.
    #
    #       2160 = 2^4 * 3^3 * 5
    #
    # First, get a list of prime factors with their multiplicity,
    # e.g. 2160 = 2^4 * 3^3 * 5, so this gives [(2, 4), (3, 3), (5, 1)]
    factors_with_multiplicity = collections.Counter(pf)

    # Now, get a list of powers of each prime factor that appear in
    # a divisor of n.
    #
    # For example, any divisor of 2160 must have one of the following
    # in its prime factorisation
    #
    #       2^0 = 1, 2^1 = 2, 2^2 = 4, 2^3 = 8, 2^4 = 16
    #
    # so the list of factors becomes:
    #
    #       [
    #           [(2, 0), (2, 1), (2, 2), (2, 3), (2, 4)],
    #           [(3, 0), (3, 1), (3, 2), (3, 3)],
    #           [(5, 0), (5, 1)],
    #       ]
    #
    powers = [
        tuple(factor ** i for i in range(count + 1))
        for factor, count in factors_with_multiplicity.items()
    ]

    # And now consider each combination of them in turn using itertools:
    for prime_power_set in itertools.product(*powers):
        yield prod(prime_power_set)


for n in (27, 293, 1416, 4716):
    print(n, list(divisors(n)))
