"""The module provides the simulation process."""
import os.path

import numpy as np

from grmpy.simulate.simulate_auxiliary import simulate_unobservables
from grmpy.simulate.simulate_auxiliary import simulate_covariates
from grmpy.simulate.simulate_auxiliary import simulate_outcomes
from grmpy.simulate.simulate_auxiliary import write_output
from grmpy.simulate.simulate_auxiliary import print_info
from grmpy.read.read import read


def simulate(init_file):
    """This function simulates a user-specified version of the Generalized Roy Model."""
    # Transform init file to dictionary
    assert os.path.isfile(init_file)
    init_dict = read(init_file)

    # Distribute information
    num_agents = init_dict['SIMULATION']['agents']
    source = init_dict['SIMULATION']['source']
    seed = init_dict['SIMULATION']['seed']
    np.random.seed(seed)

    Y1_coeffs = init_dict['TREATED']['all']
    Y0_coeffs = init_dict['UNTREATED']['all']
    C_coeffs = init_dict['COST']['all']
    coeffs = [Y0_coeffs, Y1_coeffs, C_coeffs]

    U0_sd, U1_sd, V_sd = init_dict['DIST']['all'][:3]
    vars_ = [U0_sd ** 2, U1_sd ** 2, V_sd ** 2]
    U01, U0_V, U1_V = init_dict['DIST']['all'][3:]
    covar_ = [U01 ** 2, U0_V ** 2, U1_V ** 2]
    Dist_coeffs = init_dict['DIST']['all']

    # Simulate observables
    X = simulate_covariates(init_dict, 'TREATED', num_agents)
    Z = simulate_covariates(init_dict, 'COST', num_agents)

    # Simulate unobservables
    U, V = simulate_unobservables(covar_, vars_, num_agents)

    # Simulate endogeneous variables
    Y, D, Y_1, Y_0 = simulate_outcomes([X, Z], U, coeffs)

    # Write output file
    df = write_output([Y, D, Y_1, Y_0], [X, Z], [U, V], source)

    print_info(df, [Y0_coeffs, Y1_coeffs, C_coeffs, Dist_coeffs], source)

    return df
