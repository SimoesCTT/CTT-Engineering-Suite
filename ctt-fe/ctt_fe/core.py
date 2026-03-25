"""
CTT Finite Element Analysis
Copyright (c) 2026 Americo Simoes. All Rights Reserved.
"""

import numpy as np
import sys
sys.path.insert(0, '/home/americosimoes/CTT-Engineering-Suite/ctt-core')
from ctt_core import TemporalSystem, ALPHA

class FEAnalysis:
    """Structural dynamics with CTT temporal damping."""
    
    def __init__(self, mass, stiffness, damping=0.0):
        self.M = mass
        self.K = stiffness
        # Ensure damping is a matrix
        if isinstance(damping, (int, float)):
            self.C = damping * np.eye(len(mass))
        else:
            self.C = damping
        self.alpha = ALPHA
        
    def solve(self, u0, v0, t_final, steps=100):
        """Solve M·a + C·v + K·u = 0 with CTT stability."""
        n = len(self.M)
        y0 = np.concatenate([u0, v0])
        
        def dynamics(y):
            u = y[:n]
            v = y[n:]
            try:
                a = np.linalg.solve(self.M, -self.C @ v - self.K @ u)
            except np.linalg.LinAlgError:
                a = np.linalg.lstsq(self.M, -self.C @ v - self.K @ u, rcond=None)[0]
            return np.concatenate([v, a])
        
        system = TemporalSystem(dynamics, alpha=self.alpha)
        y_final, energy = system.evolve(y0, t_final, steps)
        return y_final[:n], y_final[n:], energy
