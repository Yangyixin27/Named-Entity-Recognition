import numpy as np

def run_viterbi(emission_scores, trans_scores, start_scores, end_scores):

    L = start_scores.shape[0]
    N = emission_scores.shape[0]

    trellis = np.zeros(shape=(N,L))  # default to 0s

    Backpointers = np.zeros(shape=(N-1,L))

    #print type(start_scores)

    trellis[0] =start_scores+emission_scores[0]

    y = [0]*N
    for i in range(1, N):
        for j in range(L):
            wp = emission_scores[i][j]
            max = float('-inf')
            r = 0
            for k in range(L):
                x =wp + trellis[i - 1][k] + trans_scores[k][j]
                if (x > max):
                    max = x
                    r = k
            trellis[i][j] = max
            Backpointers[i-1][j] = r

    m = float('-inf')
    p = 0
    for j in range(L):
        x = trellis[-1][j] + end_scores[j]
        if (x > m):
            m = x
            p = j

    y[N-1]=int(p)
    #print p
    for i in range(N-2,-1,-1):
        #print p
        p=int(Backpointers[i][p])
        y[i]=int(p)

    return (m, y)

