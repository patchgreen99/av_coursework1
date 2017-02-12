from scipy.stats import norm
import numpy as np

states = np.zeros((6, 2))
measurements = np.zeros((6, 2))

initial_state_mean = None
initial_state_covariance = None

observation_matrices = None
observation_offsets = None
observation_covariance = None
transition_matrices = None
transition_offsets = None
transition_covariance = None

for t in range(6 - 1):
    if t == 0:
        states[t] = norm.rvs(initial_state_mean, np.sqrt(initial_state_covariance))
        measurements[t] = (np.dot(observation_matrices[t], states[t]) + observation_offsets[t] + norm.rvs(0, np.sqrt(
            observation_covariance)))

    states[t + 1] = (
    np.dot(transition_matrices[t], states[t]) + transition_offsets[t] + norm.rvs(0, np.sqrt(transition_covariance)))

    measurements[t + 1] = (
    np.dot(observation_matrices[t + 1], states[t + 1]) + observation_offsets[t + 1] + norm.rvs(np.sqrt(observation_covariance)))
