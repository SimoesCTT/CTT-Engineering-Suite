"""
CTT Control Systems
Copyright (c) 2026 Americo Simoes. All Rights Reserved.
"""

import numpy as np
from ctt_core import TemporalSystem, ALPHA

class ControlSystem:
    """Nonlinear control systems with CTT stability."""
    
    def __init__(self, dynamics, alpha=ALPHA):
        self.f = dynamics
        self.alpha = alpha
        
    def simulate(self, x0, u, t_final, steps=100):
        """Simulate closed-loop system with CTT stability."""
        n = len(x0)
        
        def closed_loop(x):
            return self.f(x, u)
        
        system = TemporalSystem(closed_loop, alpha=self.alpha)
        x_final, energy = system.evolve(x0, t_final, steps)
        return x_final, energy
    
    def is_stable(self, x0):
        """Check if system is stable via CTT criterion."""
        # CTT stability condition: energy decays
        _, energy = self.simulate(x0, np.zeros_like(x0), 1.0, steps=33)
        return energy[-1] < energy[0] * np.exp(-self.alpha * 33)
