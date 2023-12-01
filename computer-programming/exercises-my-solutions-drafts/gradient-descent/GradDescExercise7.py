from GradDescExercise5 import grad_desc
from flattened_to_3_d_index import flattened_to_3_d_index
import numpy as np
import matplotlib.pyplot as plt


def s(x, a, b, c):
    return a + b * np.sin(c * x)


# True values of parameters, just for reference:
a_true, b_true, c_true = 0.5, 1.2, 3.5
z_true = np.array([a_true, b_true, c_true])

# Values of x and corresponding values of y in line with the true model, for
# reference, we plot it to compare our findings to the model from which our
# data originated.
x_fine = np.linspace(-5, 5, 1000)
y_fine = s(x_fine, a_true, b_true, c_true)
plt.clf()
plt.title("Actual model, observations, learnt models with best and wortst initial guess")
#"Actual model (blue curve), observations (orange dots), model predicted for the best initial guess of parameters (red curve), model predicted for the worst initial guess of parameters (orange curve) (in the defined range)"
plt.plot(x_fine, y_fine, '-', label="true")

# x_train and y_train are the observed values from which we want to derive the model
# they are given; we want to consider many possible combinations of gueses for
# parameters a, b and c

# Here we artificially generate x_train and y_train and treat them as observed data.
x_train = np.linspace(-5, 5, 60)
np.random.seed(4627323)
y_train = s(x_train, a_true, b_true, c_true) + \
    0.1 * np.random.randn(len(x_train))
plt.plot(x_train, y_train, "o", label="observed_data")


def loss(z, x_data, y_data):  # inputs are z_guess, x_train and y_train
    # y_guess; value of the function predicted by the model with guessed parameters
    y_pred = s(x_data, z[0], z[1], z[2])
    # and y_data is empirical values we collected
    # we want to guess a, b, c, so we want to solve 3-D problem
    return np.mean((y_data - y_pred)**2)


n_guesses = 10
# for this to be able to broadcast with?
# Ensure that at least one between b and c is always non-negative because otherwise
# there could be two distinct ways to find the model since -sin(-x)=sin(x)
a_guesses = np.linspace(-5, 5, n_guesses)
b_guesses = np.linspace(-5, 5, n_guesses)
c_guesses = np.linspace(0, 10, n_guesses)
minimums = np.zeros((n_guesses, n_guesses, n_guesses))
argmins = np.zeros((n_guesses, n_guesses, n_guesses, 3))


for i in range(len(a_guesses)):
    a = a_guesses[i]
    for j in range(len(b_guesses)):
        b = b_guesses[j]
        for k in range(len(c_guesses)):
            c = c_guesses[k]
            # we input argument np.array([a, b, c]) as initial guess
            # zz is array of length 3, initially we consider initial guess, then
            # as the algorithm updates initial guess we consider consecutive guesses
            # for zz argument
            res = grad_desc(lambda zz: loss(
                zz, x_train, y_train), np.array([a, b, c]))
            minimums[i, j, k] = res.val_fin
            argmins[i, j, k, :] = res.x_fin

#not in all cases did the algorithm converge but in this simulations we gathered
#final results for all runs and then it can be more striking to see
max_ = np.max(minimums)
argmax_flattened_ind = np.argmax(minimums)
argmax_ind = flattened_to_3_d_index(
    argmax_flattened_ind, (n_guesses, n_guesses, n_guesses))
argmax_ = argmins[argmax_ind]
min_ = np.min(minimums)
argmin_flattened_ind = np.argmin(minimums)
argmin_ind = flattened_to_3_d_index(
    argmin_flattened_ind, (n_guesses, n_guesses, n_guesses))
argmin_ = argmins[argmin_ind]
print(
    f"The minimum value of loss (benchmark is 0!) to which the grad_desc algorithm converged is {min_} which happened for the initial guess {argmin_}.")
print(
    f"The maximum value of loss to which the grad_desc algorithm converged is {max_} which happened for the initial guess {argmax_}.")

#Consider the true model and how well it fits the empirical data:
loss_true_model=loss(np.array([a_true, b_true, c_true]), x_train, y_train)
print("Here we do not have the case of overfitting since loss given the data and the true model is 0.012 and for the best model we have found the loss is greater, 0.024.")


a_argmin, b_argmin, c_argmin = argmin_
y_estimate_best_case = s(x_fine, a_argmin, b_argmin,
                         c_argmin)  # best initial guess
plt.plot(x_fine, y_estimate_best_case, '-',
         color="red", label="best_case_estimate")

a_argmax, b_argmax, c_argmax = argmax_
y_estimate_worst_case = s(x_fine, a_argmax, b_argmax,
                          c_argmax)  # worst initial guess
plt.plot(x_fine, y_estimate_worst_case, '-',
         color="orange", label="worst_case_estimate")


plt.legend()


#Above we considered 10 evenly spaced values of initial guesses for a, b and c
#within the specified ranges and we took into account all possible combinations
#of those values, so 10**3 possible initial guesses. Now we change the approach:
#we will specify the ranges for a, b and c and we will run 100 trials and upon
#each iteration we will randomly generate the vector for the initial guess by
#randomly generating a, b and c from specified ranges.

n_guesses=100
#in the previous example, we appended all possible minimums, regardless whether the
#algo converged, here we are more careful, so we also create a list, not array
#as we do not know its size

#we can keep all values and corresponding parameters in lists
#but we can also keep just one, like best_loss_value
best_loss_value=np.inf
best_loss_parameters=np.zeros(3)
best_initial_guess=np.zeros(3)
minimums2=[]
argmins2=[]
for guess in range(n_guesses):
    a2=np.random.uniform(-1, 1)
    b2=np.random.uniform(-0.5, 1.5)
    c2=np.random.uniform(2, 5)
    res2=grad_desc(lambda zz: loss(zz, x_train, y_train), np.array([a2, b2, c2]), epsilon=1e-1)
    if res2.converged==True: #!!! for convergence we need to adapt alpha, beta, epsilon...
        minimums2.append(res2.val_fin)
        #best_init_guess=np.array([a2, b2, c2]) no!! this gets updated even if the value is greater
        argmins2.append(res2.x_fin)
    #alternatively, we can just keep the best_loss, it should be the same as
    #np.min(minimums2) at the end
    if res2.converged==True and res2.val_fin<best_loss_value:
        best_loss_value=res2.val_fin
        best_initial_guess[:]=np.array([a2, b2, c2]) #we fill the entries, not assignment! mutable
        best_loss_parameters[:]=res2.x_fin
#!!! Best_initial_guess for parameters (so that from them, as a starting point
#after all iterations of the optimization algorithm, the minimum loss is reachable) 
#is different from the parameters correspodning to the best_loss_value.
#These parameters are reached at the end of all iterations of grad_desc/minimum
#from a given starting parameters.
#By choosing n_guesses different combinations of starting parameters (n_guesses
#distinct initial guesses) and examining the final minimum and corresponding
#minimizer to which our initial guess evolves, we show that the final outcome
#strongly depends on the initial guess for nasty functions like s.
minimums2=np.array(minimums2)
argmins2=np.array(argmins2)      
#we extract the worst case with initial guess array([0.5279513 , 0.1246411 , 2.21377666])
#while the algo still converged so that we can see that depending on the initial
#guess, we converge to different values
max2_ = np.max(minimums2)
argmax_ind2 = np.argmax(minimums2)
argmax2_ = argmins2[argmax_ind2]
min2_ = np.min(minimums2) #the best loss value
argmin_ind2 = np.argmin(minimums2)
argmin2_ = argmins2[argmin_ind2] #parameters corresponding to the best initial guess
n_convergences=len(minimums2)
n_non_convergences=n_guesses-n_convergences
assert min2_==best_loss_value and (argmin2_==best_loss_parameters).all()

print(f"The optimal value for the loss found is {min2_} and the corresponding parameters are {argmin2_}, while the corresponding initial guess is {best_initial_guess}!")
print(f"To check that a method without storing all values is equivalent: obtained loss is {best_loss_value}, paramters that minimze loss are {best_loss_parameters} and the initial guess that allows to arrive at (converge to) this outcome is {best_initial_guess}!")



#here absolute minimum is 0 so we can just take the minimum of the values of
#loss to determine the closest value to official outcome




'''
a_guesses, b_guesses, c_guesses=np.meshgrid(a_guesses, b_guesses, c_guesses)

loss_ = loss(np.stack((a_guesses, b_guesses, c_guesses)), x_train, y_train)
'''

'''
z=np.zeros(3)
for a in a_guesses:
    z[0]=a
    for b in b_guesses:
        
        for c in c_guesses:
            res=grad_desc(loss, z0)
'''


from scipy.optimize import minimize

minimums_grad_desc=[]
minimums_minimize=[]
best_loss_grad_desc=np.inf
best_loss_minimize=np.inf
best_initial_guess_grad_desc=np.zeros(3)
best_initial_guess_minimize=np.zeros(3)
for guess in range(n_guesses):
    a3=np.random.uniform(-1, 1)
    b3=np.random.uniform(-0.5, 1.5)
    c3=np.random.uniform(2, 5)
    res_grad_desc=grad_desc(lambda zz: loss(zz, x_train, y_train), np.array([a3, b3, c3]), epsilon=0.1)
    res_minimize=minimize(lambda zz: loss(zz, x_train, y_train), np.array([a3, b3, c3]))
    if res_grad_desc.converged or not res_grad_desc.converged: 
        minimum_grad_desc=res_grad_desc.val_fin
        minimums_grad_desc.append(minimum_grad_desc)
        if minimum_grad_desc<best_loss_grad_desc:
            best_initial_guess_grad_desc[:]=np.array([a3, b3, c3])
            best_loss_grad_desc=minimum_grad_desc
    if res_minimize.success:
        minimum_minimize=res_minimize.fun
        minimums_minimize.append(minimum_minimize)
        if minimum_minimize<best_loss_minimize: #only then, not upon each convergence
            best_initial_guess_minimize[:]=np.array([a3, b3, c3])
            best_loss_minimize=minimum_minimize #update
            
plt.figure()     
plt.hist([minimums_grad_desc, minimums_minimize])
#(np.array(minimums_grad_desc)>=np.array(minimums_minimize)).sum() is 98
#so in most cases minimize allows for a better result

print(f"Number of times the algorithm converged for minimize: {len(minimums_minimize)} and for grad_desc: {len(minimums_grad_desc)}")