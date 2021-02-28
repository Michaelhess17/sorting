#!/bin/python3
'''
Python provides built-in sort/sorted functions that use timsort internally.
You cannot use these built-in functions anywhere in this file.

Every function in this file takes a comparator `cmp` as input which controls how the elements of the list should be compared against each other.
If cmp(a,b) returns -1, then a<b;
if cmp(a,b) returns  1, then a>b;
if cmp(a,b) returns  0, then a==b.
'''

import random

def cmp_standard(a,b):
    '''
    used for sorting from lowest to highest
    '''
    if a<b:
        return -1
    if b<a:
        return 1
    return 0


def cmp_reverse(a,b):
    '''
    used for sorting from highest to lowest
    '''
    if a<b:
        return 1
    if b<a:
        return -1
    return 0


def cmp_last_digit(a,b):
    '''
    used for sorting based on the last digit only
    '''
    return cmp_standard(a%10,b%10)


def _merged(xs, ys, cmp=cmp_standard):
    '''
    Assumes that both xs and ys are sorted,
    and returns a new list containing the elements of both xs and ys.
    Runs in linear time.
    '''
    result = [0] * (len(xs) + len(ys))
    x_ind = y_ind = result_ind = 0
    while result_ind != len(result):
        while (x_ind != len(xs)) & (y_ind != len(ys)):
            comp = cmp(xs[x_ind], ys[y_ind])
            if comp == -1:
                result[result_ind] = xs[x_ind]
                result_ind += 1
                x_ind += 1
            elif comp == 0:
                result[result_ind] = xs[x_ind]
                result[result_ind + 1] = ys[y_ind]
                result_ind += 2
                x_ind += 1
                y_ind += 1
            else:
                result[result_ind] = ys[y_ind]
                result_ind += 1
                y_ind += 1
        if (x_ind == len(xs)) & (y_ind != len(ys)):
            while y_ind != len(ys):
                result[result_ind] = ys[y_ind]
                result_ind += 1
                y_ind += 1
        elif (x_ind != len(xs)) & (y_ind == len(ys)):
           while x_ind != len(xs):
                result[result_ind] = xs[x_ind]
                result_ind += 1
                x_ind += 1
    return result

def merge_sorted(xs, cmp=cmp_standard):
    '''
    Merge sort is the standard O(n log n) sorting algorithm.
    Recall that the merge sort pseudo code is:

        if xs has 1 element
            it is sorted, so return xs
        else
            divide the list into two halves left,right
            sort the left
            sort the right
            merge the two sorted halves

    You should return a sorted version of the input list xs
    '''
    if (len(xs) == 1) or (not xs):
        return xs
    else:
        xs_l = xs[:len(xs) // 2]
        xs_r = xs[len(xs) // 2:]
        xs_l_sorted = merge_sorted(xs_l, cmp)
        xs_r_sorted = merge_sorted(xs_r, cmp)
        return _merged(xs_l_sorted, xs_r_sorted, cmp)

def quick_sorted(xs, cmp=cmp_standard):
    '''
    Quicksort is like mergesort,
    but it uses a different strategy to split the list.
    Instead of splitting the list down the middle,
    a "pivot" value is randomly selected, 
    and the list is split into a "less than" sublist and a "greater than" sublist.

    The pseudocode is:

        if xs has 1 element
            it is sorted, so return xs
        else
            select a pivot value p
            put all the values less than p in a list
            put all the values greater than p in a list
            sort both lists recursively
            return the concatenation of (less than, p, and greater than)

    You should return a sorted version of the input list xs
    '''
    if (len(xs) == 1) or (not xs):
        return xs
    else:
        p = random.choice(xs)
        xs_p = [x for x in xs if x == p]
        xs_less = [x for x in xs if x < p]
        xs_greater_equal = [x for x in xs if x > p]
        xs_less_sorted = quick_sorted(xs_less, cmp)
        xs_ge_sorted = quick_sorted(xs_greater_equal, cmp)
        merge1 = _merged(xs_less_sorted, xs_p, cmp)
        return _merged(merge1, xs_ge_sorted, cmp)

def quick_sort(xs, cmp=cmp_standard, lo=0, hi=None):
    '''
    EXTRA CREDIT:
    The main advantage of quick_sort is that it can be implemented in-place,
    i.e. with O(1) memory requirement.
    Merge sort, on the other hand, has an O(n) memory requirement.

    Follow the pseudocode of the Lomuto partition scheme given on wikipedia
    (https://en.wikipedia.org/wiki/Quicksort#Algorithm)
    to implement quick_sort as an in-place algorithm.
    You should directly modify the input xs variable instead of returning a copy of the list.
    '''
    if hi == None:
        hi = len(xs) - 1
    def partition(xs, lo, hi):
        pivot = xs[hi]
        i = lo
        for j in range(lo, hi):
            if cmp(xs[j], pivot) == -1:
                xs[i], xs[j] = xs[j], xs[i]
                i += 1
        xs[i], xs[hi] = xs[hi], xs[i]
        return i

    if lo < hi:
        p = partition(xs, lo, hi)
        quick_sort(xs, cmp, lo, p - 1)
        quick_sort(xs, cmp, p + 1, hi)
    else:
        return xs
