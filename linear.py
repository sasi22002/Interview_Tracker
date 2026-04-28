x = [1,4,6,7,8,33,66,89,222,467,888]


def bubble_sort(arr):
    n = len(arr)
    
    for i in range(n):
        for j in range(n-i-1):
            if arr[j]>arr[j+1]:
                arr[j],arr[j+1] = arr[j+1],arr[j]
                
    return arr


def binary_search(x,n):
    x = bubble_sort(x)
    
    size = len(x)-1
    left = 0
    right = size
    
    while left<=right:
        mid = (left+right) // 2
        if x[mid] == n:
            return n,mid

        if x[mid] <= n:
            left = mid +1
        else:
            right = mid-1
            
        
            
    return 0,0
        
val,index = binary_search([99,3,2,45,75,246,764,32],32)
    
print(f"Number {val} found at index {index}")


def bin_recursive(arr,left,right,n):
    
    if left<=right:
        mid = (left+right )//2
        if arr[mid] == n:
            return mid
        
        if arr[mid]<n:
            return bin_recursive(arr,mid+1,right,n)
        else:
            return bin_recursive(arr,left,mid-1,n)
           
        
        

print(bin_recursive(x,0,len(x)-1,66))
            

val = {0: True, 1: True, 2: True, 3: True, 4: True, 5: True, 6: True, 7: True, 8: True, 9: True, 10: True, 11: True, 12: True, 13: True, 14: True, 15: True, 16: True, 17: True, 18: True, 19: True, 20: True, 21: True, 22: True, 23: True, 24: True, 25: True, 26: True, 27: True, 28: True, 29: True, 30: True, 31: True, 32: True, 33: True, 34: True, 35: True, 36: True, 37: True, 38: True, 39: True, 40: True, 41: True, 42: True, 43: True, 44: True, 45: True, 46: True, 47: True, 48: True, 49: True, 50: True, 
       51: True, 52: True, 53: True, 54: True, 55: True, 56: True, 57: True, 58: True, 59: True, 60: True, 61: True, 62: True, 63: True, 64: True, 65: True, 66: True, 67: True, 68: True, 69: True, 70: True, 
       71: False, 72: False, 73: False, 74: False, 75: False, 76: False, 77: False, 78: False, 79: False, 80: False, 81: False, 82: False, 
       83: False, 84: False, 85: False, 86: False, 87: False, 88: False, 89: False, 90: False, 91: False, 92: False, 93: False, 94: False, 95: False, 96: False, 97: False, 98: False, 99: False, 100: False}

def msys(arr):
    size = len(arr)-1
    
    x = list(arr.keys())
    size = len(x) -1
    
    left = 0
    right = size
    
    while left<=right:
        mid = (left+right) //2
        if arr[mid] == False:
            return mid
        
        if arr[mid]!=False:
            left = mid +1
        else:
            right = mid-1
            
        
            
        
    pass

print(msys(val))
    