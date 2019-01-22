#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

Example script

@author: David P. Fleming [University of Washington, Seattle], 2018
@email: dflemin3 (at) uw (dot) edu

"""

from approxposterior import approx, likelihood as lh
import numpy as np
import george

# Define algorithm parameters
m0 = 50                           # Initial size of training set
m = 20                            # Number of new points to find each iteration
nmax = 10                         # Maximum number of iterations
Dmax = 0.1                        # KL-Divergence convergence limit
kmax = 5                          # Number of iterations for Dmax convergence to kick in
nKLSamples = 10000                # Number of samples from posterior to use to calculate KL-Divergence
bounds = ((-5,5), (-5,5))         # Prior bounds
algorithm = "BAPE"                # Use the Kandasamy et al. (2015) formalism

# emcee MCMC parameters
samplerKwargs = {"nwalkers" : 20}        # emcee.EnsembleSampler parameters
mcmcKwargs = {"iterations" : int(2.0e4)} # emcee.EnsembleSampler.run_mcmc parameters

# Randomly sample initial conditions from the prior
theta = np.array(lh.rosenbrockSample(m0))

# Evaluate forward model log likelihood + lnprior for each theta
y = np.zeros(len(theta))
for ii in range(len(theta)):
    y[ii] = lh.rosenbrockLnlike(theta[ii]) + lh.rosenbrockLnprior(theta[ii])

# Initialize object using the Wang & Li (2017) Rosenbrock function example
# Note that by not supplying a GP, we use the default which is a uses an
# ExpSquaredKernel
ap = approx.ApproxPosterior(theta=theta,
                            y=y,
                            lnprior=lh.rosenbrockLnprior,
                            lnlike=lh.rosenbrockLnlike,
                            priorSample=lh.rosenbrockSample,
                            algorithm=algorithm)

# Run!
ap.run(m=m, nmax=nmax, Dmax=Dmax, kmax=kmax, bounds=bounds,  estBurnin=True,
       nKLSamples=nKLSamples, mcmcKwargs=mcmcKwargs, cache=False,
       samplerKwargs=samplerKwargs, verbose=True)

# Check out the final posterior distribution!
import emcee, corner

# Load in chain from last iteration
samples = ap.sampler.get_chain(discard=ap.iburns[-1], flat=True, thin=ap.ithins[-1])

# Corner plot!
fig = corner.corner(samples, quantiles=[0.16, 0.5, 0.84], show_titles=True,
                    scale_hist=True, plot_contours=True)

fig.savefig("finalPosterior.png", bbox_inches="tight") # Uncomment to save
