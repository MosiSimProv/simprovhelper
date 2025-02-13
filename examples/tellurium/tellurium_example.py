# Note: This just an example demonstrating how the simulate_and_save_data wrapper-function Tellurium can be used. It is not meant to be executed.

###################
# This script is not meant to be executed.
###################

from tellurium import loada
from simprovhelper.tellurium import *

model_file = "./model.tel"
data_file = "./exp_results.pickle"

r: ExtendedRoadRunner = loada(model_file)
# use a stochastic solver
r.integrator = 'gillespie'
r.integrator.seed = 4321
# selections specifies the output variables in a simulation
selections = ['time'] + r.getBoundarySpeciesIds() + r.getFloatingSpeciesIds()
r.integrator.variable_step_size = False
simulate_and_save_data(r, data_file, start=0, end=60, points=101, selections=selections)
