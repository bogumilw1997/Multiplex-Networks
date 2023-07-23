import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
from json import load
from tqdm import tqdm
import sys

# r0 = 0.8 dla mu=lambda 

plt.rcParams["figure.figsize"] = [14, 8]
plt.rcParams['font.size'] = '15'
plt.rcParams['lines.linewidth'] = '1.5'
plt.rcParams['lines.markersize'] = '9'
plt.rcParams["figure.autolayout"] = True

with open("semestr3\WSZ\programy\wersja1\params_integrated_20.json") as f:
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

save_path_local = parameters["save_path_local"]

df = pd.DataFrame()
df_ = pd.DataFrame()

lambda_list = np.linspace(lambd_min, lambd_max, lambd_points, endpoint=True)

from simulation_integrated import simulation

for lambd in tqdm(lambda_list):
    
    inf_list = np.zeros(realizations)
    
    for realization in tqdm(range(realizations)):
            
            sym = simulation(N, m, epsilon, lambd, mu, gamma, eta, p0, integration_steps)

            for t in tqdm(range(1, T)):
                sym.do_one_step()

            inf_list[realization] = sym.get_inf_number()
            
    df_['inf'] = inf_list
    df_['R0'] = sym.get_R0()
        
    df_['lambd'] = lambd
    df_['mu'] = mu
    
    df = pd.concat([df, df_], ignore_index = True)

df.to_csv(save_path_local + 'integrated_40.csv')