# Multiplex-Networks

University project intended for simulating epidemic spreading on temporal network.
For the network topology I'm using Activity Driven Network model (https://www.nature.com/articles/srep00469).

# Usage

* For simulating epidemic spreading on purely temporal network run `sym_temporal.py` script.
* For simulating epidemic spreading on integrated ADN network run `sym_integrated.py` script.

# Parameters

Simulation parameters for temporal and integreted networks are controled by `params_temporal.json` nad `params_integrated.json` files respectively.
* `N` is the size of a network (nodes)
* `m` is the number of connections made by active node in every time step
* `T` is the time of the simulations (steps)
* `integration_steps` is the number of steps after which network is beeing integrated
* `lambd_min` and `lambd_max` are the minimal and maximal values of  
* `mu` is the epidemic spreading rate
* `eta`, `epsilon` and `gamma` are parameters of the ADN model
* `p0` is probability of each node beeing infected in T=0
* `realizations` is the number of system realizations per parameters set
  
