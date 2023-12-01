import numpy as np
import matplotlib.pyplot as plt

#%% EXERCISE 2

#left to do: create graph of numbers against frequencies + align figures, stack them
#horizontal and vertical: https://matplotlib.org/stable/gallery/subplots_axes_and_figures/subplots_demo.html

def unbiased_random(n_): #we could ofc use n but we do not want to use the same
#notation for external and internal variables
    while True:
        e1 = np.random.randint(n)
        e2 = np.random.randint(n)
        if e1 > e2:
           e1, e2 = e2, e1
        if (e2 != e1 and e2 != e1+1 and (e2+1) % n != e1): 
            break
    return (e1, e2)

    
def unbiased_random(n_):
    while True:
        e1 = np.random.randint(n)
        e2 = np.random.randint(n)  
        if e1>e2:
            e1, e2=e2, e1
        if e1!=e2:
            break
    return (e1, e2)

def biased_random(n_):
    e1 = np.random.randint(n-1)
    e2 = np.random.randint(e1+1, n)
    return (e1, e2)

#Shared for both distributions:
n=10
numbers=np.array([i for i in range(n)])
sample_size=10**5

#Sampling 2 random incides in an unbiased way.
frequencies1=np.zeros(n)
frequencies2=np.zeros(n)
for attempt in range(sample_size):
    random_numbers=unbiased_random(n)
    e1, e2=random_numbers #unpacking a tuple
    frequencies1[e1]+=1
    frequencies2[e2]+=1
#plt.figure()
#plt.title("!")
#plt.plot(numbers, frequencies1)
#plt.figure()
#plt.title("?")
#plt.plot(numbers, frequencies2)

#Sampling 2 random incides in a biased way.
frequencies12=np.zeros(n)
frequencies22=np.zeros(n)
for attempt in range(sample_size):
    random_numbers2=biased_random(n)
    e12, e22=random_numbers2 #unpacking a tuple
    frequencies12[e12]+=1
    frequencies22[e22]+=1
#plt.clf()
#plt.hist(frequencies12, bins=n-1)
#plt.hist(frequencies22, bins=n-1)



#Histogram just needs raw data values, input is data, not some frequencies, can have array with 10**5 numbers, corresponding
#to the size of the sample as an input

plt.figure()
plt.title("Distribution of the first index for unbiased random number generation")
#Sampling index 1 from unbiased distribution (output of unbiased_random is a tuple so we need to extract specific element):
plt.hist(np.array([unbiased_random(n)[0] for i in range(10**5)]), bins=n-1)
plt.figure()
plt.title("Distribution of the second index for unbiased random number generation")
#Sampling index 2 from unbiased distribution:
plt.hist(np.array([unbiased_random(n)[1] for i in range(10**5)]), bins=n-1, color="red")
plt.figure()
plt.title("Distribution of the first index for biased random number generation")
plt.hist(np.array([biased_random(n)[0] for i in range(10**5)]), bins=n-1, color="orange")
plt.figure()
plt.title("Distribution of the second index for biased random number generation")
plt.hist(np.array([biased_random(n)[1] for i in range(10**5)]), bins=n-1, color="pink")
#for unbiased_random, we use bins=n as there are n different values that the generated numbers can take,
#while for biased, first index can take n-1 values (it cannot take the last value which is reserved for the second index)
#and second index cannot take what the first index took, so it will for example never take 0
#distribution of the second numbers is right-skewed as it always takes values to the right of first index, which has uniform distribution
plt.figure()
plt.hist2d([unbiased_random(n)[0] for i in range(10**5)], [unbiased_random(n)[1] for i in range(10**5)], bins=(n-1, n-1))
plt.figure()
plt.hist2d([biased_random(n)[0] for i in range(10**5)], [biased_random(n)[1] for i in range(10**5)], bins=(n-1, n-1))

