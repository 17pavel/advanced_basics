#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functools import  wraps

def disable():
    '''
    Disable a decorator by re-assigning the decorator's name
    to this function. For example, to turn off memoization:

    >>> memo = disable

    '''
    ...


def decorator(func):
    '''
    Decorate a decorator so that it inherits the docstrings
    and stuff from the function it's decorating.
    '''
    @wraps(func)
    def wrapper(*args,  **kwargs):
        print(func.__name__)
        return func(*args,  **kwargs)
    return wrapper


def countcalls(func):
    '''Decorator that counts calls made to the function decorated.'''
    @wraps(func)
    def wrapper(*args,  **kwargs):
        wrapper.count += 1
        print(f'func called: {wrapper.count}')
        return func(*args, **kwargs)
    wrapper.count =0    
    
    return wrapper


def memo(func):
    '''
    Memoize a function so that it caches all return values for
    faster future lookups.
    '''
    cache = {}
    @wraps(func)
    def wrapper(*args, **kwargs):
        key = str(args) + str(kwargs)
        if key not in cache:
            cache[key] = func(*args, **kwargs)
            print(cache, key, sep=' | ' )
        return cache[key]    
    return wrapper


def n_ary(func):
    '''
    Given binary function f(x, y), return an n_ary function such
    that f(x, y, z) = f(x, f(y,z)), etc. Also allow f(x) = x.
    '''
    @wraps(func)
    def wrapper(*args, **kwargs):
        ...
    return wrapper


def trace(func):
    '''Trace calls made to function decorated.

    @trace("____")
    def fib(n):
        ....

    >>> fib(3)
     --> fib(3)
    ____ --> fib(2)
    ________ --> fib(1)
    ________ <-- fib(1) == 1
    ________ --> fib(0)
    ________ <-- fib(0) == 1
    ____ <-- fib(2) == 2
    ____ --> fib(1)
    ____ <-- fib(1) == 1
     <-- fib(3) == 3

    '''
    @wraps(func)
    def wraper(*args, **kwargs):
        ...
    return wraper


@memo
@countcalls
#@n_ary
def foo(a, b):
    return a + b


@countcalls
@memo
#@n_ary
def bar(a, b):
    return a * b


@countcalls
#@trace("####")
@memo
def fib(n):
    """Some doc"""
    return 1 if n <= 1 else fib(n-1) + fib(n-2)


def main():
    print (foo(4, 3))
#    print (foo(4, 3, 2))
    print (foo(4, 3))
    print ("foo was called", foo.count, "times")

    print (bar(4, 3))
#    print (bar(4, 3, 2))
#    print (bar(4, 3, 2, 1))
    print ("bar was called", bar.count, "times")

    print (fib.__doc__)
    fib(10)
    print (fib.count, 'calls made')


if __name__ == '__main__':
    main()
