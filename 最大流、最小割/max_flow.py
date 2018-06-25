# -*- coding: utf-8 -*-
"""
Created on Sun Jun 24 01:01:11 2018

@author: Administrator
"""

import networkx as nx
import matplotlib.pyplot as plt
from random import randint
import numpy as np

#随机生成一个有向无环图
def random_dag(v_num=10, e_num=20,direction=True,rand_weight=False,max_weight=10):
    G = nx.Graph()
    if direction:
        G=G.to_directed()
    G.add_nodes_from(range(v_num))
    for i in range(e_num):
        f = randint(0,v_num-2)
        t = randint(f+1,v_num-1)
        G.add_edge(f,t, capacity=randint(1,max_weight) if rand_weight else 1) 
        #nx的最大流算法需要边有一个名叫capacity的域，否则一条边的容量将被作为无穷大
    return G

def Graph_info(G):
    info = {}
    info['node']=list(G.node)
    info['edges'] = []
    for i,j in G.edges:
        info['edges'].append((i,j,G[i][j]['capacity']))
    return info

def Graph_from_info(info,direction=True):
    G = nx.DiGraph() if direction else nx.Graph()
    G.add_nodes_from(info['node'])
    for i,j,w in info['edges']:
        G.add_edge(i,j,capacity=w)
    return G
    

info = {'edges': [(0, 1, 1),
  (0, 5, 1),
  (1, 8, 1),
  (1, 7, 1),
  (1, 4, 1),
  (2, 5, 1),
  (3, 4, 1),
  (3, 9, 1),
  (3, 7, 1),
  (4, 6, 1),
  (4, 7, 1),
  (4, 8, 1),
  (5, 8, 1),
  (6, 7, 1),
  (7, 9, 1),
  (7, 8, 1),
  (8, 9, 1)],
 'node': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]}
v_num = 10
e_num = 30
G = random_dag(v_num,e_num,direction=True,rand_weight=True)

G = Graph_from_info(info)
nx.draw_circular(G,with_labels=True,with_width=True)
plt.show()
print(Graph_info(G))
print(nx.maximum_flow(G,_s=0,_t=v_num-1))

from queue import Queue
INF = 10000 #无穷大

def BFS(G,s,d,pre,capacity):
    visited = [False]*G.number_of_nodes()
    queue = Queue() #广度优先搜索需要用队列完成.每次运行广度优先搜索前必须先清空队列，否则之前的元素会遗留在队列里
           
    flow = [0]*G.number_of_nodes()
    flow[s] = INF
    visited[s] = True
    queue.put(s)
    while not queue.empty():
        v = queue.get()
        #for son in G.successors(v): #这种写法是错误的，因为这样只能找到原来就存在的边，无法找到后来添加进来的边（实际并没有者的添加边，而是增加了一个反向的capacity）,于是无法形成退流
        for son in range(G.number_of_nodes()):
            if not visited[son] and capacity[v][son]>0: #如果一开始就没有边，则capacity为0
                flow[son]=min(capacity[v][son],flow[v])
                visited[son]=True
                pre[son] = v
                queue.put(son)
                if son == d:
                    return flow[son]
    return 0
        

def max_flow_EK(G,s,d):
    max_flow = 0
    capacity = np.zeros([G.number_of_nodes(),G.number_of_nodes()],dtype=np.int32)
    for f,t in G.edges:
        capacity[f][t] = G[f][t]['capacity']
    
    while True:
        pre = [-INF]*G.number_of_nodes()
        flow = BFS(G,s,d,pre,capacity)
        max_flow += flow
        if flow==0: #python没有do while语法。这种方法等价于 do while
            break
        t = G.number_of_nodes()-1    
        while True:
            f = pre[t]
            if f<0 :
                break
            capacity[f][t] -= flow
            capacity[t][f] += flow
            t = f
    
    #每条边上的flow:
    flow_result = {}
    for v in range(G.number_of_nodes()):
        flow_result[v] = {}
        for son in G.successors(v):
            flow_result[v][son] = capacity[son][v]
    return max_flow,flow_result

m = max_flow_EK(G,0,v_num-1)
print(m)


v_num=100
e_num=150
error = []
for i in range(1000):
    G = random_dag(v_num,e_num,rand_weight=True,max_weight=100)
    if nx.maximum_flow(G,_s=0,_t=v_num-1)[0]!=max_flow_EK(G,0,v_num-1)[0]:
        error.append(G)
if not error:
    print('success')
else:
    print(error)
