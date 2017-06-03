def bsearch(find, arr, low, high):
    while low <= high:
        mid = (low + high) >> 1
        if arr[mid] == find:
            return mid, True
        elif arr[mid] > find:
            high = mid - 1
        else:
            low = mid + 1
    return low, False


def BaezaYates_intersect_helper(A, B, left1, right1, left2, right2, result):
    if left1 > right1 or left2 > right2:
        return
    if right1-left1 > right2-left2:
        left1, left2 = left2, left1
        right1, right2 = right2, right1
        A, B = B, A
    mid = (left1 + right1) >> 1
    index,found = bsearch(A[mid], B, left2, right2)
    if found:
        result.append(A[mid])
        BaezaYates_intersect_helper(A, B, left1, mid-1, left2, index-1, result)
        BaezaYates_intersect_helper(A, B, mid+1, right1, index+1, right2, result)
    else:
        if A[mid] > B[right2]:
            BaezaYates_intersect_helper(A, B, left1, mid-1, left2, right2, result)
        elif A[mid] < B[left2]:
            BaezaYates_intersect_helper(A, B, mid+1, right1, left2, right2, result)
        else:
            BaezaYates_intersect_helper(A, B, left1, mid-1, left2, index-1, result)
            BaezaYates_intersect_helper(A, B, mid+1, right1, index, right2, result)


def BaezaYates_intersect(A, B):
    result = []
    BaezaYates_intersect_helper(A, B, 0, len(A)-1, 0, len(B)-1, result)
    result.sort()
    return result