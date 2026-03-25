"""
CTT Control Systems
Copyright (c) 2026 Americo Simoes. All Rights Reserved.
"""

import numpy as np
import sys
sys.path.insert(0, '/home/americosimoes/CTT-Engineering-Suite/ctt-core')
from ctt_core import ALPHA

class ControlSystem:
    """Nonlinear control systems with CTT stability."""
    
    def __init__(self, dynamics, alpha=ALPHA, velocity_indices=None):
        self.f = dynamics
        self.alpha = alpha
        # Indices of velocity states (default: all even? no, let user specify)
        self.vel_indices = velocity_indices if velocity_indices is not None else []
        
    def simulate(self, x0, u, t_final, steps=100):
        """Simulate system with CTT damping applied to velocities only."""
        dt = t_final / steps
        x = np.array(x0, dtype=float)
        energy = []
        
        # For tracking energy, we'll use a simple sum of squares
        energy.append(np.sum(x**2))
        
        for d in range(33):
            for _ in range(steps // 33):
                # RK4 integration
                x = self._rk4_step(x, u, dt)
            
            # Apply CTT damping ONLY to velocity components
            if len(self.vel_indices) > 0:
                for i in self.vel_indices:
                    x[i] *= np.exp(-self.alpha)
            else:
                # If no indices specified, apply to all (fallback)
                x *= np.exp(-self.alpha)
            
            energy.append(np.sum(x**2))
        
        return x, energy
    
    def _rk4_step(self, x, u, dt):
        """4th order Runge-Kutta integration."""
        k1 = self.f(x, u)
        k2 = self.f(x + 0.5 * dt * k1, u)
        k3 = self.f(x + 0.5 * dt * k2, u)
        k4 = self.f(x + dt * k3, u)
        return x + dt * (k1 + 2*k2 + 2*k3 + k4) / 6.0
    
    def is_stable(self, x0):
        """Check if system is stable via CTT criterion."""
        _, energy = self.simulate(x0, np.zeros_like(x0), 1.0, steps=33)
        return energy[-1] < energy[0] * np.exp(-self.alpha * 33)
