# -*- coding: utf-8 -*-

import random
import time
import tkinter as tk
from initialb import states    
from initialb import judge
from initialb import refine

UNIT = 40   # pixels
ENV_H = 3  # grid height
ENV_W = 3  # grid width
learning_rate=0.5
EPSILON=0.3

window=tk.Tk()
window.title('tic-tac-toe')
window.geometry('{0}x{1}'.format(ENV_H * UNIT, ENV_H * UNIT))
global canvas
canvas=tk.Canvas(window,bg='white',height=ENV_H * UNIT,width=ENV_H * UNIT)
for c in range(0, ENV_W * UNIT, UNIT):
    x0, y0, x1, y1 = c, 0, c, ENV_H * UNIT
    canvas.create_line(x0, y0, x1, y1)
for r in range(0, ENV_H * UNIT, UNIT):
    x0, y0, x1, y1 = 0, r, ENV_H * UNIT, r
    canvas.create_line(x0, y0, x1, y1)

#chess position
key_dict={'1':(20,20),'2':(60,20),'3':(100,20),
          '4':(20,60),'5':(60,60),'6':(100,60),
          '7':(20,100),'8':(60,100),'9':(100,100)}
# record chessboard's state(how many chess on it, and their position)
#global pos_rec
global chess_state_i
#pos_rec=[]
# V(s) : dict
global value_table
key_list=list(set(refine(states(9))))

value_table={} 
for k in key_list:
    if(judge(k)==0):
        value_table[k]=0
    elif(judge(k)==1):
        value_table[k]=1
    else:
        value_table[k]=0.5


countO=0    # the num of a random agent win
countX=0    # the num of a RL agent win
countdraw=0 # the num of a draw 
#'O' random
def random_choose_action():
    empty1=[x for x in list(range(1,10)) if x not in pos_rec]
    if(len(empty1)==0):
        return
    action=random.sample(empty1,1)[0]  #action[0] 
    
    return action

def choose_action(current_state):  #current_state is similar to  'iiiiOXOii'
    #agent 'X'  
    if random.uniform()<EPSILON:
        empty1=[x for x in list(range(1,10)) if x not in pos_rec]
        if(len(empty1)==0):
            return
        action=random.sample(empty1,1)[0]  #action[0] 
    else:
        current_length=len([x for x in current_state if x!='i'])  #
        # Filter current_ Length + 1 and add it to the new dictionary ready
        ready={}
        for k in value_table.keys():
            if(len([j for j in k if j!='i' ])==(current_length+1)):
                ready[k]=value_table[k]
        #Filter out k that corresponds to the non-i value in current_state and add it to the new dictionary result
        result={}
        num1=[]      #num1  in current_state  non-i's id
        for i in range(9):
            if(current_state[i]!='i'):
                num1.append(i)
        
        for q in ready.keys(): #for k in ready.keys():
            for h in num1:
                if(q[h]==current_state[h]):
                    if(h==(num1[len(num1)-1])):
                        result[q]=value_table[q]
                else:
                    break
        #select the maximum  key of the result, and select an action 'X'   max(result,key=result.get)
        aim_key=max(result,key=result.get)
        count=0
        for m in aim_key:
            if count not in num1:
                if (m!='i'):
                    action=count+1  
                    break
                else:
                    count+=1
            else:
                count+=1
    return action

def update_table(current_state,next_state):
   
    if(judge(current_state)):
        value_table[current_state]+=learning_rate*(value_table[next_state]-value_table[current_state]) 
  
def reset():
    canvas.delete('all')
    
    for c in range(0, ENV_W * UNIT, UNIT):
        x0, y0, x1, y1 = c, 0, c, ENV_H * UNIT
        canvas.create_line(x0, y0, x1, y1)
    for r in range(0, ENV_H * UNIT, UNIT):
        x0, y0, x1, y1 = 0, r, ENV_H * UNIT, r
        canvas.create_line(x0, y0, x1, y1)
    #time.sleep(0.3)
    canvas.pack()
    window.update()   
# 'O'
def random_step(action,chess_state_i,pos_rec):
    pos_rec.append(action)
    temp_state=chess_state_i
    chess_state_i=''
    for k in range(0,9):
        if k!=action-1:
            chess_state_i+=temp_state[k]
        else:
            chess_state_i+='O'
    #time.sleep(0.2)
    canvas.create_text(key_dict[str(action)],text='O',font="time 25 bold")         
    canvas.pack()
    window.update()
    return chess_state_i,pos_rec        
# 'X'       
def agent_step(action,chess_state_i):

    pos_rec.append(action)
    temp_state=chess_state_i
    chess_state_i=''
    for k in range(0,9):
        if k!=action-1:
            chess_state_i+=temp_state[k]
        else:
            chess_state_i+='X'
    #print('agent after, '+chess_state_i)
    canvas.create_text(key_dict[str(action)],text='X',font="time 25 bold")
    #time.sleep(0.2)
    canvas.pack()
    window.update()
    return chess_state_i

for episode in range(1,10001):
    global pos_rec
    pos_rec=[] 
    chess_state_i='iiiiiiiii'
    terminal=0
    while(terminal!=1):
        #random first
        if((len(pos_rec)!=9)&(judge(chess_state_i)!=1)):
            chess_state_i,pos_rec=random_step(random_choose_action(),chess_state_i,pos_rec)
            current_state=chess_state_i
            
        #agent 
        if((len(pos_rec)!=9)&(judge(current_state)!=0)):     #if not lose
            chess_state_i=agent_step(choose_action(current_state),current_state)
            next_state=chess_state_i

        elif(judge(chess_state_i)==0):           # if lose
            terminal=1
            print('episode %d, random win '%(episode))
            countO+=1
        elif((len(pos_rec)==9)&(judge(chess_state_i)==0.5)):    # if draw
            print('episode %d, draw '%(episode))
            terminal=1
            countdraw+=1
            
        if((len(pos_rec)!=9)&(judge(chess_state_i)==1)):  #if win
            terminal=1
            print('episode %d, agent win '%(episode))
            countX+=1
        update_table(current_state,next_state)
    pos_rec=[]
    chess_state_i='iiiiiiiii'
    reset()
    print('---------------------------------------------------------------------')
print('---------------------------------------------------------------------')
print('random win, ',countO)
print('agent win, ',countX)
print('draw , ',countdraw)
print('---------------------------------------------------------------------')

print(value_table)
window.update()
window.mainloop()

