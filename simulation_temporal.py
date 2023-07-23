from matplotlib import pyplot as plt
import numpy as np
import networkx as nx
import copy

class simulation():
    
    epidemic_states = np.array(['S', 'I'])
    activity_states = np.array(['A', 'N'])
    
    def power_dist(self, r, xmin, gamma):
        return xmin * (1-r) ** (-1/(gamma-1))
    
    def get_mean_theoretical_degree(self):
        return 2*self.m*self.eta*np.mean(self.activity)
    
    def get_mean_degree(self):
        return np.mean(np.array([d for n, d in self.g.degree()]))

    def get_R0(self):
        return self.lambd*self.get_mean_degree()/self.mu
    
    def get_R0_theoretical(self):
        return self.lambd*self.get_mean_theoretical_degree()/self.mu   
    
    def get_epidemic_threshold(self):
        return 2*np.mean(self.activity_rate)/(np.mean(self.activity_rate) + np.sqrt(np.mean(np.square(self.activity_rate))))
    
    def __init__(self, N, m, epsilon, lambd, mu, gamma, eta, p0):
        
        self.N = N
        self.m = m
        self.eta = eta
        
        self.lambd = lambd
        self.mu = mu
        self.nodes_list = np.arange(N)
        
        self.activity = self.power_dist(np.random.uniform(size = N), epsilon, gamma)
        self.activity_rate = np.minimum(self.activity * eta, np.ones_like(self.activity))
        #self.activity_rate = self.activity * eta
        
        self.epidemic_state = np.random.choice(self.epidemic_states, N, p=[1- p0, p0])
        self.check_topology()
        
    def check_topology(self):
        
        self.g = nx.empty_graph(self.N, nx.Graph)
        
        self.activity_state = np.full(self.N, 'N')
        
        probs = np.random.rand(self.N)
        
        self.activity_state[probs <= self.activity_rate] = "A"
        
        active_nodes = self.nodes_list[self.activity_state == "A"]

        for active_node in active_nodes:
            
            nodes_to_connect = np.random.choice(self.nodes_list, self.m, replace=False)
            
            while(np.isin(active_node, nodes_to_connect, assume_unique=True)):
                nodes_to_connect = np.random.choice(self.nodes_list, self.m, replace=False)
        
            for node_to_conect in nodes_to_connect:
                self.g.add_edge(active_node, node_to_conect)

        # print(np.array(self.g.edges())[0][0])
        # print(np.array(self.g.edges())[0][1])
        # print(self.g[np.array(self.g.edges())[0][0]])
        # print(self.g[np.array(self.g.edges())[0][1]])
        # print(self.g.edges())
    
    def get_inf_number(self):
        return np.sum(self.epidemic_state == "I")/self.N
    
    def get_susc_number(self):
        return np.sum(self.epidemic_state == "S")/self.N
    
    def check_epidemic(self, node):
        
        if self.epidemic_state[node] == 'S':
            
            neighbours = np.array(self.g[node])
            
            if neighbours.shape[0] > 0:
                    
                    i_neighbours = neighbours[self.epidemic_state[neighbours] == 'I']
                    
                    i_count = i_neighbours.shape[0]
                    
                    if i_count > 0:
                        
                        infection_prob = np.random.rand(i_count)
                        
                        if all(i_p >= self.lambd for i_p in infection_prob):
                            pass
                        else:
                            self.new_epidemic_state[node] = 'I'
                            
        elif self.epidemic_state[node] == 'I':
            
            recovery_prob = np.random.rand()
            
            if recovery_prob <= self.mu:
                self.new_epidemic_state[node] = 'S'
    
    def do_one_step(self):
        
        self.check_topology()
        
        self.new_epidemic_state = copy.deepcopy(self.epidemic_state)
        
        for node in self.nodes_list:
            self.check_epidemic(node)
            
        self.epidemic_state = self.new_epidemic_state
        

        
        