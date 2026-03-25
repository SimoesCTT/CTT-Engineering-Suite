"""
CTT Quantum Mechanics
Copyright (c) 2026 Americo Simoes. All Rights Reserved.
"""

import numpy as np
from ctt_core import TemporalSystem, ALPHA

class QuantumSystem:
    """Schrödinger equation with CTT decoherence."""
    
    def __init__(self, H, alpha=ALPHA):
        self.H = H
        self.alpha = alpha
        
    def evolve(self, psi0, t_final, steps=100):
        """Evolve quantum state with CTT decoherence."""
        n = len(psi0)
        
        def dynamics(psi):
            # Real and imaginary parts
            psi_real = psi[:n]
            psi_imag = psi[n:]
            psi_complex = psi_real + 1j * psi_imag
            dpsi = -1j * self.H @ psi_complex
            return np.concatenate([np.real(dpsi), np.imag(dpsi)])
        
        y0 = np.concatenate([np.real(psi0), np.imag(psi0)])
        system = TemporalSystem(dynamics, alpha=self.alpha)
        y_final, energy = system.evolve(y0, t_final, steps)
        psi_final = y_final[:n] + 1j * y_final[n:]
        return psi_final, energy
    
    def decoherence_time(self):
        """Return CTT decoherence time."""
        return 1 / self.alpha
