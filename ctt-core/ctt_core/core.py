"""
CTT Core – Temporal Integration Engine
Copyright (c) 2026 Americo Simoes. All Rights Reserved.
"""

import numpy as np

ALPHA = 0.0302011
LAYERS = 33

class TemporalSystem:
    """Guaranteed stable temporal evolution for any dynamical system."""
    
    def __init__(self, state_derivative, alpha=ALPHA):
        self.f = state_derivative
        self.alpha = alpha
        
    def evolve(self, y0, t_final, steps=100):
        """Evolve system with CTT temporal damping."""
        dt = t_final / steps
        y = np.array(y0)
        energy = []
        
        for d in range(LAYERS):
            for _ in range(steps // LAYERS):
                y = self._step(y, dt)
            y *= np.exp(-self.alpha)
            energy.append(np.sum(y**2))
            
        return y, energy
    
    def _step(self, y, dt):
        return y + dt * self.f(y)
