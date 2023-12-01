def maxSubsetSum(arr):
    n=len(arr)
    d=[[0 for i in range(n+1)] for j in range(2)]
    opt_d0=[]
    opt_d1=[]
    for i in range(1, n+1):
        d[0][i]=max(d[0][i-1], d[1][i-1])
        append=False #default append to know whether we added or not an element previous
        #to a[i-1] to opt_d0, if we did, then we do not want to include it
        if d[1][i-1]>d[0][i] and i>1:
            opt_d0.append(arr[i-2])
            append=True
        d[1][i]=max(0, arr[i-1])+d[0][i-1]
        if append is True:
            opt_d1.append(opt_d0[:-1])
        if arr[i-1]>0:
            opt_d1.append(arr[i-1])
    max_sum=max(d[0][-1], d[1][-1])
    if max_sum==d[0][-1]:
        max_subset=opt_d0
    elif max_sum==d[1][-1]:
        max_subset=opt_d1
    return max_sum, max_subset


'''
diff=d[0][i]-max(d[0][i-1], d[1][i-1])
if diff!=0:
    opt_d0.append(diff)
'''