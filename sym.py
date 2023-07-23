import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
from json import load
from tqdm import tqdm

# r0 = 0.8 dla mu=lambda 

plt.rcParams["figure.figsize"] = [14, 8]
plt.rcParams['font.size'] = '15'
plt.rcParams['lines.linewidth'] = '1.5'
plt.rcParams['lines.markersize'] = '9'
plt.rcParams["figure.autolayout"] = True

with open("semestr3\WSZ\programy\wersja1\params_integrated_40.json") as f:
    parameters = load(f)
    
N = parameters['N']
m = parameters['m'] 
T = parameters['T']

epsilon = parameters['epsilon']

lambd_min = parameters['lambd_min'] # prawd. zara.
lambd_max = parameters['lambd_max'] # prawd. zara.
lambd_points = parameters['lambd_points'] # prawd. zara.

mu = parameters['mu'] # prawd. wyzdr.
gamma = parameters['gamma']
realizations = parameters['realizations']
eta = parameters["eta"]
p0 = parameters["p0"]
integration_steps = parameters["integration_steps"]
lambd = parameters["lambd"]
save_path_local = parameters["save_path_local"]

df = pd.DataFrame()
df_ = pd.DataFrame()

from simulation_temporal import simulation

for realization in (range(realizations)):
        
        sym = simulation(N, m, epsilon, lambd, mu, gamma, eta, p0)
        
        infections_list = np.zeros(T)
        susc_list = np.zeros(T)
        R0_list = np.zeros(T)
        #R0_the_list = np.zeros(T)
        
        infections_list[0] = sym.get_inf_number()
        susc_list[0] = sym.get_susc_number()
        R0_list[0] = sym.get_R0()
        #R0_the_list[0] = sym.get_R0_theoretical()
        
        for t in tqdm(range(1, T)):
            
            sym.do_one_step()
            
            infections_list[t] = sym.get_inf_number()
            susc_list[t] = sym.get_susc_number()
            R0_list[t] = sym.get_R0()
            #R0_the_list[t] = sym.get_R0_theoretical()
            
        df_['inf'] = infections_list
        df_['susc'] = susc_list
        df_['R0'] = R0_list
        #df_['R0_the'] = R0_the_list
        
        df_['lambd'] = lambd
        #df_['mu'] = mu
        df_['t'] = np.arange(T)
        
        df = pd.concat([df, df_], ignore_index = True)

df.to_csv(save_path_local + 'test.csv')
