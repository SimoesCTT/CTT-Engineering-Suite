"""
CTT Heat Transfer
Copyright (c) 2026 Americo Simoes. All Rights Reserved.
"""

import numpy as np
import sys
sys.path.insert(0, '/home/americosimoes/CTT-Engineering-Suite/ctt-core')
from ctt_core import TemporalSystem, ALPHA

class ThermalAnalysis:
    """Transient heat conduction with CTT stability."""
    
    def __init__(self, conductivity, heat_capacity):
        self.K = conductivity
        self.C = heat_capacity
        self.alpha = ALPHA
        
    def solve(self, T0, Q, t_final, steps=100):
        """Solve C·dT/dt + K·T = Q."""
        n = len(T0)
        
        def dynamics(T):
            return np.linalg.solve(self.C, Q - self.K @ T)
        
        system = TemporalSystem(dynamics, alpha=self.alpha)
        T_final, energy = system.evolve(T0, t_final, steps)
        return T_final, energy
