def parent(i):
    return (i - 1) // 2

def left(i):
    return 2 * i + 1

def right(i):
    return 2 * i + 2

def heapify(A, i):
    l = left(i)
    r = right(i)
    smallest = i
    if l < len(A) and A[l] < A[i]:
        smallest = l
    if r < len(A) and A[r] < A[smallest]:
        smallest = r
    if smallest != i:
        A[i], A[smallest] = A[smallest], A[i]
        heapify(A, smallest)

def extractMin(A):
    if len(A) < 1:
        return None  
    min_val = A[0]  
    A[0] = A[len(A) - 1]  
    A.pop()  
    heapify(A, 0)  
    return min_val

def insert(A, e):
    A.append(e)
    i = len(A) - 1
    while i > 0 and A[parent(i)] > A[i]:
        A[i], A[parent(i)] = A[parent(i)], A[i]
        i = parent(i)

def createEmptyPQ():
    return []

