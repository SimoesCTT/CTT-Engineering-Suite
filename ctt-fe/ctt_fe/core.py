"""
CTT Finite Element Analysis
Copyright (c) 2026 Americo Simoes. All Rights Reserved.
"""

import numpy as np
from ctt_core import TemporalSystem, ALPHA

class FEAnalysis:
    """Structural dynamics with CTT temporal damping."""
    
    def __init__(self, mass, stiffness, damping=0.0):
        self.M = mass
        self.K = stiffness
        self.C = damping * np.eye(len(mass))
        self.alpha = ALPHA
        
    def solve(self, u0, v0, t_final, steps=100):
        """Solve M·a + C·v + K·u = 0 with CTT stability."""
        n = len(self.M)
        y0 = np.concatenate([u0, v0])
        
        def dynamics(y):
            u = y[:n]
            v = y[n:]
            a = np.linalg.solve(self.M, -self.C @ v - self.K @ u)
            return np.concatenate([v, a])
        
        system = TemporalSystem(dynamics, alpha=self.alpha)
        y_final, energy = system.evolve(y0, t_final, steps)
        return y_final[:n], y_final[n:], energy
