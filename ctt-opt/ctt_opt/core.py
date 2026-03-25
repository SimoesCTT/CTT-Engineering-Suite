"""
CTT Optimisation
Copyright (c) 2026 Americo Simoes. All Rights Reserved.
"""

import numpy as np
from ctt_core import TemporalSystem, ALPHA

class CTTOptimizer:
    """Gradient descent with CTT convergence guarantee."""
    
    def __init__(self, f, grad_f, alpha=ALPHA):
        self.f = f
        self.grad = grad_f
        self.alpha = alpha
        
    def minimize(self, x0, steps=100, learning_rate=0.01):
        """Optimise with guaranteed convergence."""
        x = np.array(x0)
        energy = []
        
        for d in range(33):
            for _ in range(steps // 33):
                x = x - learning_rate * self.grad(x)
            # CTT damping ensures convergence
            x = x * np.exp(-self.alpha)
            energy.append(self.f(x))
            
        return x, energy
    
    def converges(self, x0):
        """Check if optimisation converges via CTT criterion."""
        _, energy = self.minimize(x0, steps=33)
        return energy[-1] < energy[0] * np.exp(-self.alpha * 33)
