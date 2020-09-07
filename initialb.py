# -*- coding: utf-8 -*-
"""
Created on Sun Nov 18 16:06:45 2018

@author: Zhou
"""

def judge(current_state): #判断是否为终态
    # lose
    if ((current_state[0]==current_state[1]==current_state[2]=='O')|
            (current_state[3]==current_state[4]==current_state[5]=='O')|
            (current_state[6]==current_state[7]==current_state[8]=='O')|
            (current_state[0]==current_state[3]==current_state[6]=='O')|
            (current_state[1]==current_state[4]==current_state[7]=='O')|
            (current_state[2]==current_state[5]==current_state[8]=='O')|
            (current_state[0]==current_state[4]==current_state[8]=='O')|
            (current_state[2]==current_state[4]==current_state[6]=='O')):
        observe=0
    # win
    elif ((current_state[0]==current_state[1]==current_state[2]=='X')|
        (current_state[3]==current_state[4]==current_state[5]=='X')|
        (current_state[6]==current_state[7]==current_state[8]=='X')|
        (current_state[0]==current_state[3]==current_state[6]=='X')|
        (current_state[1]==current_state[4]==current_state[7]=='X')|
        (current_state[2]==current_state[5]==current_state[8]=='X')|
        (current_state[0]==current_state[4]==current_state[8]=='X')|
        (current_state[2]==current_state[4]==current_state[6]=='X')):
        observe=1
    # draw or 
    else:
        observe=0.5
    return observe

def states(k):
    if k==1:
        s=['O','X','i']
        return s
    else:
        s_=[]
        s=states(k-1)
    for num in range(len(s)):
        for k in ['O','X','i']:
            temp=s[num]
            temp+=k
            s_.append(temp)
    return s_

def refine(sumlist):
    sumlist=list(set(sumlist))
    print('before, ',sumlist)
    print(len(sumlist))
    for i in range(len(sumlist)-1, -1, -1):
        countO=0
        countX=0
        for k in sumlist[i]:
            if(k=='O'):
                countO+=1
            if(k=='X'):
                countX+=1
        if(countO!=countX):
            if(countX+1!=countO):
                sumlist.pop(i)
    return sumlist