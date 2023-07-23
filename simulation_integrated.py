from matplotlib import pyplot as plt
import numpy as np
import networkx as nx
import copy
from scipy.optimize import curve_fit
from collections import Counter
import seaborn as sns

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
        return self.lambd/self.mu
    
    # def get_R0(self):
    #     return self.lambd*self.get_mean_degree()/self.mu
    
    def get_R0_theoretical(self):
        return self.lambd*self.get_mean_theoretical_degree()/self.mu   
    
    def get_epidemic_threshold(self):
        return 2*np.mean(self.activity_rate)/(np.mean(self.activity_rate) + np.sqrt(np.mean(np.square(self.activity_rate))))
    
    def __init__(self, N, m, epsilon, lambd, mu, gamma, eta, p0, integration_steps):
        
        self.N = N
        self.m = m
        self.eta = eta
        self.integration_steps = integration_steps
        
        self.lambd = lambd
        self.mu = mu
        self.nodes_list = np.arange(N)
        
        self.activity = self.power_dist(np.random.uniform(size = N), epsilon, gamma)
        self.activity_rate = np.minimum(self.activity * eta, np.ones_like(self.activity))
        #self.activity_rate = self.activity * eta
        
        self.epidemic_state = np.random.choice(self.epidemic_states, N, p=[1- p0, p0])
        
        self.integrate_network()
    
    def degree_distribution_graph(self, start, stop):
        
        def power_law(x, a, b):
            return a*np.power(x, b)
        
        k1_sorted = sorted(Counter(np.array(list(dict(self.g.degree).values()))).items())
        k1 = [i[0] for i in k1_sorted]
        p_k1 = [i[1]/self.N for i in k1_sorted]
        
        # if first_points == 'all':
        #     pars1, cov1 = curve_fit(f=power_law, xdata=k1, ydata=p_k1, p0=[0, 0], bounds=(-np.inf, np.inf))
        #     x1 = k1
        #     y1 = power_law(x1, pars1[0], pars1[1])
        # else:
        pars1, cov1 = curve_fit(f=power_law, xdata=k1[start:stop], ydata=p_k1[start:stop], p0=[0, 0], bounds=(-np.inf, np.inf))
        x1 = k1[start:stop]
        y1 = power_law(x1, pars1[0], pars1[1])
        
        # fig, (ax1, ax2) = plt.subplots(1, 2)
        fig, ax1 = plt.subplots()
        fig.suptitle('Rozkład stopni węzłów')
        g1 = sns.scatterplot(x = k1, y = p_k1, ax = ax1, color='b')
        sns.lineplot(x = x1, y = y1, ax = ax1, color='r')
        g1.set(xscale="log", yscale="log", xlabel=r'$k$', ylabel=r"$P(k)$")
        ax1.legend(labels = ["dane",r"fit $\gamma$ = " + f'{np.round(pars1[1],2)}'])
        
        # g2 = sns.scatterplot(x = k2, y = p_k2, ax = ax2, color='b')
        # sns.lineplot(x = x2, y = y2, ax = ax2, color='r')
        # g2.set(xscale="log", yscale="log", xlabel=r'$k$', ylabel=r"$P(k)$", title = 'Sieć opinii')
        # ax2.legend(labels = ["dane",r"fit $\gamma$ = " + f'{np.round(pars2[1],2)}'])
        
        #plt.savefig(graph_path + 'rozklad_wezlow.png')
        plt.show()
        plt.close()
        
        #return [pars1[1], pars2[1]]
    
    def check_topology(self):
        
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
    
    def integrate_network(self):
        
        self.g = nx.empty_graph(self.N, nx.Graph)
        
        for _ in range(self.integration_steps):
            self.check_topology()
        
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
        
        self.new_epidemic_state = copy.deepcopy(self.epidemic_state)
        
        for node in self.nodes_list:
            self.check_epidemic(node)
            
        self.epidemic_state = self.new_epidemic_state
        

        
        