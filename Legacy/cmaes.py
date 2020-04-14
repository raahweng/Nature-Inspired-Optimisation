import numpy as np
import random, math
import matplotlib as mpl
import matplotlib.pyplot as plt

#NOTES
#Orthogonal matrix doesn't change lengths (eg rotation, reflection, NOT strech, shear etc), also transpose = inverse
#Eigenvectors of a Covariance Matrix are the directions in which the data varies the most, thus eigenvalues are standard deviation

#TODO:
#C should be positive definite and therefore there shouldn't be any negative numbers
#z, zmean, pc, C have negatives in them rn

N = 3                                  #Number of dimenstions
xmean = np.random.uniform(0,1, (N,1))   #Initial random means (uniformly distributed)
sigma = 0.5                             #Step size (actually the standard deviation)
lmda = 4 + math.floor(3*math.log(N))    #Number of offspring (optimal?)
mu = math.floor(lmda/2)                 #Number of parents (optimal?)
weights = np.full(mu, math.log(mu + 1/2)-np.log(np.arange(1, mu + 1)))    #Weights for calculating weighted mean
weights = weights / np.sum(weights)     #Normalise weights so they sum to 1
mueff = sum(weights) ** 2 / sum(weights ** 2)   #Variance-effective size of mu
counteval = 0
chiN= N**0.5 * (1- (1/(4*N)) + (1/(21*N**2)))   #Expectation of ||N(0,I)|| (Approximate)
cc = (4+mueff/N) / (N+4 + 2*mueff/N)    #Time constant for cumulation of C
cs = (mueff+2)/(N+mueff+5)              #Time constant for cumulation for sigma control
pc = np.zeros((N,1))                      #Evolution path for C
ps = np.zeros((N,1))                      #Evolution path for Sigma
c1 = 2/N**2                            #Rank-One update stuff
cmu = min([mueff/N**2,1-c1])           #Rank-One update stuff
damps =  1 + 2*max([0, math.sqrt((mueff-1)/(N+1))-1]) + cs   #damps sigma
eigenval = 0
B = np.identity(N)                      #Eigenvectors of C with length 1; defines coordinate system
D = np.identity(N)                      #Diagonal matrix of the square roots of the eigenvalues of C; defines scaling
C = B * D * np.transpose(B * D)         #Covariance matrix
y = np.zeros((N,lmda))
x = np.zeros((N,lmda))                  #Population; columns = individual
z = np.zeros((N,lmda))
times = np.zeros(lmda)

def matmul3(a,b,c):
    return np.matmul(a, np.matmul(b, c))

# def fitness(vector):
#     vector = np.transpose(vector)
#     time = 0
#     v1 = 0
#     for i in range(N-1):
#         dy = abs(vector[i+1]-vector[i])   #Height of one line segment
#         try:
#             time += (2 * math.sqrt((20/N) ** 2 + dy ** 2))/(v1+math.sqrt(v1 ** 2+2*9.8*dy))   #Time taken for one line segment
#         except ZeroDivisionError:
#             time += math.inf
#         v1 = math.sqrt(v1 ** 2+2*9.8*dy)    #Final velocity set to the initial velocity of next segment
#     return time

def fitness(x):
    #sphere function; minima at 0,0...
    return sum(x ** 2)

def check_symmetric(a, rtol=1e-05, atol=1e-08):
    return np.allclose(a, a.T, rtol=rtol, atol=atol)

def is_pos_def(x):
    try:
        if np.all(np.linalg.eigvals(x) > 0):
            print("Positive Definite")
        else:
            print("Not Positive Definite")
    except np.linalg.LinAlgError:
        print("Not Positive Definite")
    

while True:
    #Sampling
    for i in range(lmda):
        z[:,i] = np.random.multivariate_normal(np.zeros(N), np.identity(N))  #Random normally-distributed vector: individual 
        x[:,i] = np.transpose(xmean + sigma * matmul3(B,D,z[:,i][:, np.newaxis]))   #Mutate individual using xmean
        counteval += 1    
        #y[:,i] = np.random.multivariate_normal(np.zeros(N), C)                      #Sampled from Normal Distribution, Mean 0 and Covariance C
        #x[:,i] = np.random.multivariate_normal(np.full(N, xmean), (sigma ** 2) * C)   #Sampled from Normal Distribution, Mean xmean and Covariance = (Variance*C)
            
        times[i] = fitness(x[:,i])   #Fitness evaluation
    sort = np.argsort(times)
    times.sort()    
    #times = list(reversed(times[sort[::-1]]))    #Sort by Fitness

    xmean = np.matmul(x[:, sort[::-1]][:, 0:mu], weights).reshape(N,1)      #Sample top candidates as parents, update xmean as weighted mean of x
    zmean = np.matmul(z[:, sort[::-1]][:, 0:mu], weights).reshape(N,1) 

    ps = (1-cs)*ps + math.sqrt(cs*(2-cs)*mueff) * np.matmul(B, zmean).reshape(N,1)   #Cumulative Step Length Adaptation: changes evolution path corresponding to "success" so far
    if (np.linalg.norm(ps) / (math.sqrt(1-(1-cs) ** (2*counteval/lmda)))) < chiN * (1.4+2/(N+1)):  #Heaviside Function: stalls update of pc if  if ||pc|| is large / helps when step size is too small
        hsig = np.linalg.norm(ps) / (math.sqrt(1-(1-cs) ** (2*counteval/lmda)) /chiN)    #  /chiN ??
    else:
        hsig = 0
    sigma *= np.exp((cs/damps)*(np.linalg.norm(ps)/chiN - 1))   #Update Step size (Sigma)
    
    pc = (1-cc)*pc + hsig * math.sqrt(cc*(2-cc)*mueff) * matmul3(B,D,zmean.reshape(N,1))   #Conjugate evolution path update

    C = (1-c1-cmu) * C + c1 * (np.matmul(pc,np.transpose(pc)) + (1-hsig) * cc*(2-cc) * C) + cmu * matmul3(matmul3(B, D, z[:,sort[0:mu]]), np.diag(weights), np.transpose(matmul3(B, D, z[:,sort[0:mu]])))     #Adapt Covariance Matrix C

    if counteval - eigenval >  lmda/(c1+cmu)/N/10:
        eigenval = counteval
        C = np.triu(C) + np.transpose(np.triu(C,1))   #Make C symmetrical
        try:
            B, D = np.linalg.eig(C)
        except:
            print(C)
            quit()
        B = np.diag(B)
        D = np.diag(np.sqrt(np.diag(D)))
    print()



##    dxlist = []
##    for i in range(pointnum):
##          dxlist.append(i*10/pointnum*2)
##    plt.plot(dxlist, mutant)
##    plt.show()

