def det(val):
    return (val<=2)

def binsearch(sorted_arr,func):
    left = -1
    right = len(sorted_arr)
    while right - left >1:
        mid = (left+right)//2
        if func(sorted_arr[mid]):
            left = mid
        else:
            right = mid 
    return left
    
print(binsearch([1,1,1,1,1],det))