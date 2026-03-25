"""
CTT Chemical Kinetics
Copyright (c) 2026 Americo Simoes. All Rights Reserved.
"""

import numpy as np
from ctt_core import TemporalSystem, ALPHA

class ReactionNetwork:
    """Chemical kinetics with CTT stability."""
    
    def __init__(self, rates, stoichiometry, alpha=ALPHA):
        self.k = rates
        self.nu = stoichiometry
        self.alpha = alpha
        
    def solve(self, C0, t_final, steps=100):
        """Solve reaction network with CTT stability."""
        def kinetics(C):
            dC = np.zeros_like(C)
            for i, (k, nu) in enumerate(zip(self.k, self.nu)):
                rate = k * np.prod(C**np.maximum(0, -nu))
                dC += nu * rate
            return dC
        
        system = TemporalSystem(kinetics, alpha=self.alpha)
        C_final, energy = system.evolve(C0, t_final, steps)
        return C_final, energy
