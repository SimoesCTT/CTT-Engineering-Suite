"""
CTT Biological Systems
Copyright (c) 2026 Americo Simoes. All Rights Reserved.
"""

import numpy as np
from ctt_core import TemporalSystem, ALPHA

class BiologicalSystem:
    """Population dynamics with CTT stability."""
    
    def __init__(self, growth, interaction, alpha=ALPHA):
        self.r = growth
        self.A = interaction
        self.alpha = alpha
        
    def solve(self, N0, t_final, steps=100):
        """Solve Lotka-Volterra type systems."""
        def dynamics(N):
            return N * (self.r + self.A @ N)
        
        system = TemporalSystem(dynamics, alpha=self.alpha)
        N_final, energy = system.evolve(N0, t_final, steps)
        return N_final, energy
    
    def carrying_capacity(self):
        """Compute equilibrium using CTT."""
        # CTT ensures convergence to equilibrium
        N0 = np.ones(len(self.r))
        N_eq, _ = self.solve(N0, 100.0)
        return N_eq
