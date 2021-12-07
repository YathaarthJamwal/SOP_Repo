# HELPER FUNCTIONS------------------------------------------------------------------

def binomialCoefficient(n, k):
    if (n == 0 or (n < k)):
        return 0
    # since C(n, k) = C(n, n - k)
    if(k > n - k):
        k = n - k
    # initialize result
    res = 1
    # Calculate value of
    # [n * (n-1) *---* (n-k + 1)] / [k * (k-1) *----* 1]
    for i in range(k):
        res = res * (n - i)
        res = res // (i + 1)
    return res

def listReverse(list,start,end):
    while(start<end):
        temp = list[start]
        list[start] = list[end] #Swapping
        list[end]=temp
        start+=1
        end-=1
    # print(list)

# ------------------------------------------------------------------------------------

# IMPLEMENTATION OF ALGORITHMS--------------------------------------------------------

def generate_POB_number(n, r, value):
    """
    Generate POB-number corresponding to a a given POB-value
    """

    j = n
    temp = value
    b = [0 for i in range(n)]
    for k in range(r, 0, -1):
        
        while True:
            j = j-1
            p = binomialCoefficient(j, k)
            print("k=",k," j=",j," p=",p," temp=",temp)
            if temp >= p:
                temp = temp-p
                b[j] = 1
            else:
                b[j] = 0
            if (b[j] == 1 or j <= 0):
                print("in here")
                break

        if (j <= 0):
            print("in hereeeee")
            break
    
    if j > 0:
        print("j=",j)
        for k in range(j-1, -1, -1):
            print("j=",k)
            b[k] = 0

    b.reverse()
    return b

def generate_all_POB(n, r):
    """
    Generates all the POB Numbers sequentially.
    """

    pob_dict = {}
    b = []
    for i in range(0,r,1):
        b.append(1)
    for i in range(r,n,1):
        b.append(0)
    # print(first_pob)

    done = 0
    count = 0
    while True:
        print("POB Value: ", count)
        count = count + 1
        b.reverse()
        print("POB String: ",b)
        pob_dict[count-1] = b.copy()
        b.reverse()
        noOfZeros = 0
        i = 0
        j = 1
        while (j < n) and (b[j] == 1 or b[i] == 0):
            # print("i=",i," j=",j," inside", "b[j]=",b[j]," b[i]=",b[i])
            if b[i] == 0:
                noOfZeros = noOfZeros + 1
            if j == n-1:
                done = 1
            i = j
            j = j+1
        
        if (done == 1):
            break

        b[j] = 1
        j = i - noOfZeros
        while i >= j:
            # print("i=",i," j=",j)
            b[i] = 0
            i = i-1

        while i >= 0:
            # print("i=",i," j=",j)
            b[i] = 1
            i = i-1

        # print("i=",i," j=",j)
        if (done == 1):
            break

    return pob_dict

def generate_next_POB_number(B):
    """
    Generates the next POB-number
    """

    ans = B.copy()
    if len(B) < 2:
        print("Not possible")
        return -1

    ans.reverse()
    j = -1
    for i in range(1,len(ans),1):
        if ans[i] == 0 and ans[i-1] == 1:
            j = max(j,i)
    
    if (j == -1):
        print("B contains no substring as 01 i.e., B is the maximum representable number")
        return -1
    
    ans[j] = 1
    ans[j-1] = 0
    listReverse(ans, 0, j-2)
    ans.reverse()
    return ans

def generate_prev_POB_number(B):
    """
    Generates the previous POB-number
    """

    ans = B.copy()
    if len(B) < 2:
        print("Not possible")
        return -1

    ans.reverse()
    j = -1
    for i in range(1,len(ans),1):
        if ans[i] == 1 and ans[i-1] == 0:
            j = max(j,i)
    
    if (j == -1):
        print("B contains no substring as 01 i.e., B is the maximum representable number")
        return -1
    
    ans[j] = 0
    ans[j-1] = 1
    listReverse(ans, 0, j-2)
    ans.reverse()
    return ans

# --------------------------------------------------------------------------------------------


# TEST THE ABOVE FUNCTIONS BELOW--------------------------------------------------------------

res = generate_POB_number(9, 4, 0)
print(res)

res = generate_all_POB(9,4)
print(res)

res = generate_next_POB_number([0,0,0,0,0,1,1,1,1])
print(res)

res = generate_next_POB_number([0,1,1,1,1,0,0,0,0])
print(res)

# --------------------------------------------------------------------------------------------


