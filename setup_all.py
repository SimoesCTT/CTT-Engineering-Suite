#!/usr/bin/env python3
"""
Install all CTT modules
"""
import subprocess
import sys

modules = [
    "ctt-core",
    "ctt-navier-stokes",
    "ctt-fe",
    "ctt-thermal",
    "ctt-em",
    "ctt-acoustic",
    "ctt-control",
    "ctt-opt",
    "ctt-finance",
    "ctt-quantum",
    "ctt-chemistry",
    "ctt-bio"
]

for module in modules:
    print(f"Installing {module}...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-e", f"./{module}"])
