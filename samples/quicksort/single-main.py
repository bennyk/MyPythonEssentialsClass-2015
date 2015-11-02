
import random

def qsort(items, depth=0):
    """
    Recursive quick-sort algorithm.
    """
    indent = '  ' * depth
    prefix = "{}".format(indent)
    print(prefix, "sorting {}".format(items))

    if len(items) <= 1:
        return [ items[0] ]

    pivot = items[0]
    less = []
    pivotList = []
    more = []
    for x in items:
        if x < pivot:
            less.append(x)
        elif x > pivot:
            more.append(x)
        else:
            pivotList.append(x)

    print(prefix, "less", less)
    print(prefix, "pivot", pivotList)
    print(prefix, "more", more)

    # sometime we have a worst case pivot

    sortedLess = []
    if len(less) > 0:
        sortedLess = qsort(less, depth=depth + 1)

    sortedMore = []
    if len(more) > 0:
        sortedMore = qsort(more, depth=depth + 1)

    print(prefix, "sorted:", sortedLess, pivotList, sortedMore)

    return sortedLess + pivotList + sortedMore


def qsort2(items):
    """
    Quick-sort using list comprehension
    """
    if len(items) == 0:
        return []

    if len(items) == 1:
        return [ items[0] ]

    pivot = items[0]
    return qsort2([x for x in items if x < pivot])\
           + [pivot]\
           + qsort2([x for x in items if x > pivot])

def qsort3(items):
    """
    Non recursive version of quick-sort.
    - in our non-recursive version, our strategy is similar except now we need to track the location of pivots till
    all of the pivots have been discovered.
    """

    # create an initial unit of work. Each unit work is marked by a starting index and its sub-partition so that
    # we know when we add up the starting index to compute the final location of the pivot in the final sorted list.
    work = (0, items)

    # we will be using works to track remaining partitions needed to be quick-sorted
    works = [work]

    # create a result list to store all of our pivots sorted thru qsort in our final sorted list
    result = [-1] * len(items)

    # keep working on partition till no remaining partitions left.
    while len(works) > 0:

        # remove a unit of partition to work on in this iteration
        startIndex, part = works.pop()


        # standard quick-sorting start here...

        pivot = part[0]
        lessPart = []
        morePart = []
        for x in part:
            if x < pivot:
                lessPart.append(x)
            elif x > pivot:
                morePart.append(x)
            else:
                # ignoring pivot
                pass

        if len(lessPart) > 0:
            # create a unit of work for the lesser partition.
            works.append((startIndex, lessPart))

        if len(morePart) > 0:
            # create a unit of work for the greater partition.
            works.append((startIndex + len(lessPart) + 1, morePart))

        # A pivot's location is final in standard quick-sort algorithm. Hence we put it back to the result.
        result[ startIndex + len(lessPart) ] = pivot

    return result


sample = random.sample(range(100), 10)
print("->", sample)

print("sorted list:", qsort3(sample))
