"""
Recover the CCLE IC50 dataset using NP. We use K,L=5,5.

Measure the convergence over iterations and time.
We run the algorithm 20 times and average the training error and time stamps.
We only store the MSE.
"""

import sys, os
project_location = os.path.dirname(__file__)+"/../../../../"
sys.path.append(project_location)

from BNMTF_ARD.code.models.nmtf_np import nmtf_np
from BNMTF_ARD.data.drug_sensitivity.load_data import load_ccle_ic50

import numpy
import scipy
import random
import matplotlib.pyplot as plt


''' Location of toy data, and where to store the performances. '''
output_folder = project_location+"BNMTF_ARD/experiments/experiments_ccle_ic/convergence_average/results/"
output_file_performances = output_folder+'nmtf_np_all_performances.txt'
output_file_times = output_folder+'nmtf_np_all_times.txt'


''' Model settings. '''
iterations = 1000

init_FG = 'kmeans'
init_S = 'random'
K, L = 10, 10
repeats = 20


''' Load in data. '''
R, M = load_ccle_ic50()


''' Run the algorithm, :repeats times, and average the timestamps. '''
times_repeats = []
performances_repeats = []
for i in range(0,repeats):
    # Set all the seeds
    numpy.random.seed(i), random.seed(i), scipy.random.seed(i)
    
    # Run the classifier
    BNMTF = nmtf_np(R,M,K,L) 
    BNMTF.initialise(init_FG=init_FG, init_S=init_S)
    BNMTF.run(iterations)

    # Extract the performances and timestamps across all iterations
    times_repeats.append(BNMTF.all_times)
    performances_repeats.append(BNMTF.all_performances['MSE'])


''' Print out the performances, and the average times, and store them in a file. '''
all_times_average = list(numpy.average(times_repeats, axis=0))
all_performances_average = list(numpy.average(performances_repeats, axis=0))
print "all_times_average = %s" % all_times_average
print "all_performances_average = %s" % all_performances_average
open(output_file_times,'w').write("%s" % all_times_average)
open(output_file_performances,'w').write("%s" % all_performances_average)


''' Plot the average time plot, and performance vs iterations. '''
plt.figure()
plt.title("Performance against average time")
plt.plot(all_times_average, all_performances_average)
plt.ylim(0,2000)

plt.figure()
plt.title("Performance against iteration")
plt.plot(all_performances_average)
plt.ylim(0,2000)