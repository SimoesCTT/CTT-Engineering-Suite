"""
CTT Acoustics
Copyright (c) 2026 Americo Simoes. All Rights Reserved.
"""

import numpy as np
from ctt_core import TemporalSystem, ALPHA

class AcousticSolver:
    """Wave equation with CTT stability."""
    
    def __init__(self, c, rho):
        self.c = c
        self.rho = rho
        self.alpha = ALPHA
        
    def solve(self, p0, v0, t_final, steps=100):
        """Solve acoustic wave equations."""
        n = len(p0)
        y0 = np.concatenate([p0, v0])
        
        def dynamics(y):
            p = y[:n]
            v = y[n:]
            dp = -self.rho * self.c**2 * np.gradient(v)
            dv = -(1/self.rho) * np.gradient(p)
            return np.concatenate([dp, dv])
        
        system = TemporalSystem(dynamics, alpha=self.alpha)
        y_final, energy = system.evolve(y0, t_final, steps)
        return y_final[:n], y_final[n:], energy
