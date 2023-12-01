import numpy as np
import matplotlib.pyplot as plt

#%% "RANDOM WALK ON A SQARE GRID" PROBLEM: ESTIMATING PROBABILITY DISTRIBUTION
#USING A STOCHASTIC PROCESS. METROPOLIS HASTINGS ALGORITHM.
#ONLY APPLICABLE TO GRID PROBLEMS!!
'''
Random walk problem on n x n grid. Evaluating probability distribution using
stochastic process. Finding limiting probability by running the stochastic
process enough number of times. Since acceptance matrix is not arbitrary
and depends on the proposal matrix, we may think that it compensates for the
imbalance caused by the proposal matrix chosen without many constraints.
This way we will get the same probability distribution and this way it is possible
for infinitely many possible stochastic simulations to be run to be able to
sample from the same probability distribution corresponding to the specific problem.
'''

def grid_proposal_random(n_states):
    matrix=np.zeros((n_states, n_states))
    sqrt_n_states=int(np.sqrt(n_states)) #we know that for a square grid, n_states will give an integer while squared
    #we convert it to int in order to avoid future problem with indexing
    #matrix[dest][source] has to be indexed with int, but when we evaluate dest, we use sqrt so we must make sure it is int
    moves=np.array([1, -1, sqrt_n_states, -sqrt_n_states])
    for source in range(n_states):
        #taking care of corner points
        if source==0:
            allowed_dest=(source+1, source+sqrt_n_states)
        elif source==sqrt_n_states-1:
            allowed_dest=(source-1, source+sqrt_n_states)
        elif source==n_states-sqrt_n_states:
            allowed_dest=(source+1, source-sqrt_n_states)
        elif source==n_states-1:
            allowed_dest=(source-1, source-sqrt_n_states)
        elif 0<source<sqrt_n_states-1:
            allowed_dest=(source+1, source-1, source+sqrt_n_states)
        elif n_states-sqrt_n_states<source<n_states-1:
            allowed_dest=(source+1, source-1, source-sqrt_n_states)
        elif source%sqrt_n_states==0: #it is written after corner points in this column and is elif so won't collide
            allowed_dest=(source+1, source-sqrt_n_states, source+sqrt_n_states)
        elif source+1%sqrt_n_states==0:
            allowed_dest=(source-1, source-sqrt_n_states, source+sqrt_n_states)
        else:
            allowed_dest=(source-1, source+1, source-sqrt_n_states, source+sqrt_n_states)
        for dest in allowed_dest:
            matrix[dest][source]=np.random.random() #isn't dest and source already int? 
    #why do we have to convert the type for it to work? because dest is float, it is computed using sqrt which is by default float
    column_sums=np.sum(matrix, axis=0)
    proposal_matrix=matrix/column_sums
    return proposal_matrix
       
#"Regular", "even" proposal matrix corresponding to the transition matrix
#for a totally random walk with no possibility of staying in one place. 
def grid_proposal_pretty(n_states):
    proposal_matrix=np.zeros((n_states, n_states))
    sqrt_n_states=int(np.sqrt(n_states))
    moves=np.array([1, -1, sqrt_n_states, -sqrt_n_states])
    for source in range(n_states):
        #taking care of corner points
        if source==0:
            allowed_dest=(source+1, source+sqrt_n_states)
        elif source==sqrt_n_states-1:
            allowed_dest=(source-1, source+sqrt_n_states)
        elif source==n_states-sqrt_n_states:
            allowed_dest=(source+1, source-sqrt_n_states)
        elif source==n_states-1:
            allowed_dest=(source-1, source-sqrt_n_states)
        elif 0<source<sqrt_n_states-1:
            allowed_dest=(source+1, source-1, source+sqrt_n_states)
        elif n_states-sqrt_n_states<source<n_states-1:
            allowed_dest=(source+1, source-1, source-sqrt_n_states)
        elif source%sqrt_n_states==0: #it is written after corner points in this column and is elif so won't collide
            allowed_dest=(source+1, source-sqrt_n_states, source+sqrt_n_states)
        elif source+1%sqrt_n_states==0:
            allowed_dest=(source-1, source-sqrt_n_states, source+sqrt_n_states)
        else:
            allowed_dest=(source-1, source+1, source-sqrt_n_states, source+sqrt_n_states)
        n_dest=len(allowed_dest)
        for dest in allowed_dest:
            proposal_matrix[dest][source]=1/n_dest #evenly distributed probabilities
            #over destinations, we do not have to devide by column sums!
    return proposal_matrix    

def acceptance_matrix(proposal, probability):
    n=np.size(probability)
    A=np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i!=j and not (proposal[i][j]==0): #proposal[j][i] can be zero no problem
                A[i][j]=min(1, (proposal[j][i]*probability[i])/(proposal[i][j]*probability[j]))
    return A

def propose_move_(source, proposal_matrix):
#INDEXING OF NUMPY ARRAYS IS NOT LIKE INDEXING A LIST!!, [:, source], not [:][source]
    transit_prob=proposal_matrix[:, source] #transition probabilities from a 
#given source are included in the column corresponding to the source so we want 
#to extract that column and pass it as a p argument to random.choice in order 
#to generate a random number from the numpy array given a numerical probability distribution
    n=np.size(transit_prob)
    destinations=np.array([i for i in range(n)])
    dest=np.random.choice(destinations, p=transit_prob) 
#how to fix the problem that probabilities do not sum to 1 when there are rounding issues?
#just normalization? but i already used it
    move=(source, dest)
    return move

def accept_move_(move, acceptance_matrix):
    source, destination=move
    p=acceptance_matrix[destination][source]
    return np.random.binomial(1, p) #returns 1 or 0 (True or False, equivalent)
    
#With "sampling_from_probability_dist(p, n_iter=1000)" we will sample from
#probability distribution p.
#Here we take "grid_proposal_random(n_states)" proposal matrix generator.
def sampling_from_probability_dist(p, n_iter=100000): #function of probability and number of iterations
    n_states=np.size(p)
    sample=np.zeros(n_states) #sample will contain frequencies of states corresponding to its indices
    proposal_m=grid_proposal_random(n_states)
    acceptance_m=acceptance_matrix(proposal_m, p)
    position=np.random.randint(0, n_states) #initializing position, first will be random
    #subsequent position will be more meaningful
    sample[position]+=1
    for i in range(n_iter):
        proposed_move=propose_move_(position, proposal_m)
        if accept_move_(proposed_move, acceptance_m): #or if accept....==True, equivalently
            position=proposed_move[1] #destination will become the current position if the move is accepted
            sample[position]+=1
    p_dist_estimate=sample/np.sum(sample) #estimate of the probability distribution
    return p_dist_estimate
    
#Using a regular matrix, pretty one.
def sampling_from_probability_dist2(p, n_iter=100000): #function of probability and number of iterations
    n_states=np.size(p)
    sample=np.zeros(n_states) #sample will contain frequencies of states corresponding to its indices
    proposal_m=grid_proposal_pretty(n_states)
    acceptance_m=acceptance_matrix(proposal_m, p)
    position=np.random.randint(0, n_states) #initializing position, first will be random
    #subsequent position will be more meaningful
    sample[position]+=1
    for i in range(n_iter):
        proposed_move=propose_move_(position, proposal_m)
        if accept_move_(proposed_move, acceptance_m): #or if accept....==True, equivalently
            position=proposed_move[1] #destination will become the current position if the move is accepted
            sample[position]+=1
    p_dist_estimate=sample/np.sum(sample) #estimate of the probability distribution
    return p_dist_estimate

#Let's take probability distribution be:
random_numbers=np.random.random(10)
random_prob_dist=random_numbers/np.sum(random_numbers)
print(random_prob_dist)
random_prob_dist_estimate=sampling_from_probability_dist(random_prob_dist)
print(random_prob_dist_estimate)
random_prob_dist_estimate2=sampling_from_probability_dist2(random_prob_dist)
print(random_prob_dist_estimate2)


#We can see that the population probability distribution is similar to sample
#probability distribution in the cases of both proposal matrices chosen.



#ACTUAL STOCHASTIC SIMULATIONS THIS TIME USING Q MATRIX:

#%% NOW ESTIMATE PROBABILITY DISTRIBUTION FOR A GRID PROBLEM WITH TRANSITION
#MATRIX DEFINED BY grid_proposal_pretty; basically it's equivalent to proposing
#and accepting everything, with 100% probability of acceptance?

#is it right?
def sampling_3(p, n_iter=100000): 
    n_states=np.size(p)
    sample=np.zeros(n_states) 
    proposal_m=grid_proposal_pretty(n_states)
    position=np.random.randint(0, n_states)
    sample[position]+=1
    for i in range(n_iter):
        proposed_move=propose_move_(position, proposal_m)
        position=proposed_move[1] 
        sample[position]+=1
    p_dist_estimate=sample/np.sum(sample) 
    return p_dist_estimate

#%% NOW ESTIMATE THE PROBABILITY DISTRIBUTION FOR A GRID PROBLEM FOR MATRIX
#Q COMPUTED FROM PROPOSAL AND ACCEPTANCEL CARRY OUT STOCHASTIC SIMULATION

#%% COMPUTE THE LIMITING PROBABILITY

#%% FINISH THIS FILE AND "Sampling from some distribution" also go through it

#%% docs: metropolis hastings i pytania

#%% EXERCISE SHEETS AND ADDITIONAL EXERCISES
















#PROPOSAL MATRIX HAS TO BE PROBLEM-SPECIFIC OBVIOUSLY
#IN EACH PROBLEM THERE IS SOME PROBABILITY DISTRIBUTION, EACH SOLUTION/VALUE 
#IN THE PROBLEM APPEARS WITH CERTAIN PROBABILITY
#TO SAMPLE FROM THIS PROBLEM, WE NEED TO SET UP PROPOSAL AND ACCEPTANCE MATRIX
#ACCORDING TO SOME RULES
#PROPOSAL MATRIX IS NEARLY ARBITRARY, BUT IT HAS TO BE STOCHASTIC MATRIX 
#COLUMNS SUMMING TO 1, ENTRIES CORRESPONDING TO NON-CONNECTED SOURCE AND DESTINATION
#ARE 0 BECAUSE WE CANNOT PROPOSE INVALID (UNFEASIBLE) MOVE AND DIAGONAL ENTRIES ARE 0 AS WE CANNOT PROPOSE NO MOVE
#(IT WILL BE POSSIBLE TO STAY ON THE CURRENT POSITION WITHOUT MOVING, THOUGH,
#THIS SITUATION WILL CORRESPOND TO REFUSING THE MOVE, USING ACCEPT_MOVE FUNCTION)

#WE CREATE A PROPOSAL MATRIX DESCRIBING A PROBLEM, THERE IS SOME DEGREE OF 
#FREEDOM HERE BUT OBVIOUSLY THE MOVED PROPOSED MUST BE FEASIBLE, I.E. PROBABILITIES
#TO GO TO UNCONNECTED DESTINATION FROM A GIVEN SOURCE MUST NECESSARILY BE 0
#SO THE CORRESPPONDING ENTRY IN THE PROPOSAL MATRIX IS 0
#ENTRIES RELATED TO CONNECTED SOURCE AND DESTINATION CAN BE CHOSEN ALMOST
#ARBITRARILY; OF COURSE IN ORDER TO FACILITATE COMPUTATIONS, WE WOULD PREFER
#SOME PRETTY MATRIX, BUT IN FACT WE MAY FILL THE ENTRIES FOR CONNECTED POINTS
#USING A RANDOM NUMBER GENERATOR AND THEN NORMALIZE THE COLUMNS OF THE MATRIX
#BY DIVIDING THEM BY THE COLUMN SUMS
#AND ACCEPTANCE MATRIX DERIVED FROM THIS PROPOSAL IN ORDER TO SAMPLE FROM SOME
#DISTRIBUTION

#WE WILL CONSIDER TWO PROPOSAL MATRIX - PRETTY ONE AND RANDOM ONE FOR THE SAME 
#PROBLEM; WE WILL BUILD ACCEPTANCE MATRICES ACCORDING TO THE RULES
#THEN WE WILL RUN STOCHASTIC PROCESSES FOR BOTH PAIRS OF PROPOSAL AND ACCEPTANCE MATRIX
#USE THE PROBABILITIES ENCODED IN PROPOSAL AND ACCEPTANCE MATRICES WHILE PROPOSING AND ACCEPTING A MOVE
#WE WILL SAMPLE IN BOTH CASES AND COMPARE THE ESTIMATED DISTRIBUTION - IT SHOULD
#BE THE SAME AS IN THE SAME PROBLEM MARGINAL PROBABILITIES SHOULD BE THE SAME
#WE CAN ALSO COMPUTE A TRANSITION MATRIX FOR BOTH CASES

#how to generate a bunch of random numbers which sum up to 1
#create array of random numbers and divide by the sum