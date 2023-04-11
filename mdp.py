import math
import sys
import random

# Data Basis
txt_name = sys.argv[1]
num_noT_state,num_T_state,num_round,frequency,hyper_M,num_total_state = 0,0,0,0,0,0
T_state = {}
transition = {}

# Input
with open(txt_name) as f:
    info=f.readline().rstrip("\n").rstrip().split(" ")
    info = [int(i) for i in info]
    num_noT_state,num_T_state,num_round,frequency,hyper_M=info
    num_total_state = num_noT_state+num_T_state
    info = f.readline().rstrip("\n").rstrip().split(" ")
    info = [int(i) for i in info]
    i = 0
    while i<num_T_state*2:
        T_state[info[i]]=info[i+1]
        i+=2
    while(True):
        info=f.readline()
        if not info:
            break
        info=info.rstrip("\n").rstrip().split(" ") 
        i=1
        probs=[0.0]*num_total_state
        while i<len(info):
            probs[int(info[i])]= float(info[i+1])
            i+=2
        transition[info[0]]=probs 

#MDP Data Basis
count = dict.fromkeys(transition.keys(),0)
total = dict.fromkeys(transition.keys(),0)
curr_state = 0
curr_action = []
states=[]
non_T_states=[]
for i in range(num_total_state):
    states.append(i)
    if i not in T_state.keys():
        non_T_states.append(i)

# Choosing the Action
def chooseAction(state):
    n = 0
    c = 0
    for key in transition.keys():
        if int(key.split(":").pop(0)) == state:
            n+=1
            if count[key] == 0:
                return int(key.split(":").pop(1))
            else:
                c+=count[key]
    avg = [0.0]*n
    for i in range(0,n):
        avg[i] = (total[str(state)+":"+str(i)] *1.0 )/ count[str(state)+":"+str(i)]
    bottom = math.inf
    top = 0
    for key in T_state.keys():
        if T_state[key] > top:
            top = T_state[key]
        if T_state[key] < bottom:
            bottom = T_state[key]
    savg = [0.0]*n
    for i in range(0,n):
        savg[i] = 0.25 +0.75*(avg[i]-bottom)/(top-bottom)
    up = [0.0]*n
    norm = 0.0
    for i in range(0,n):
        up[i] = pow(savg[i],(c/hyper_M))
    for i in range(0,n):    
        norm += up[i]
    p = [0.0]*n
    for i in range(0,n):
        p[i] = up[i]/norm
    action = []
    for i in range(0,n):
        action.append(i)
    return(int(random.choices(action,weights=p,k=1).pop(0)))

    

# Output
def output(num):
    print("After",num,"rounds")
    print("Count:")
    for key in count.keys():
        print("["+str(key)+"] ="+str(count[key]))
    print("Total:")
    for key in count.keys():
        print("["+str(key)+"] ="+str(total[key]))
    best_action = {}
    for state in non_T_states:
        max = 0.0
        max_key = None
        for key in count.keys():
            if int(key.split(":").pop(0)) == state:
                if count[key] != 0:
                    if (total[key]*1.0)/count[key] > max:
                        max = (total[key]*1.0)/count[key]
                        max_key = key
        if max == 0.0:
            max_key = "U"
        best_action[state] = max_key
    print("Best Action:")
    for key in best_action.keys():
        if best_action[key] == "U":
            print(str(key)+":"+best_action[key])
        else:
            print(best_action[key])

    

# Markov Decision Process
for iter in range(1,num_round+1):
    curr_action=[]
    curr_state=random.choices(non_T_states,k=1).pop(0)
    while curr_state not in T_state.keys():
        action = chooseAction(curr_state)
        if str(curr_state)+":"+str(action) not in curr_action:
            curr_action.append(str(curr_state)+":"+str(action))
        curr_state = int(random.choices(states,weights=transition[str(curr_state)+":"+str(action)],k=1).pop(0))
    reward = T_state[curr_state]
    for key in curr_action:
        count[key] += 1
        total[key] += reward

    # in-loop output
    if frequency != 0:
        if iter%frequency == 0:
            output(iter)

# Conclusion
if num_round%frequency != 0:
    output(num_round)
