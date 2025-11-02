
### **11. `tools-setup/angr_installation.md`**
```markdown
# Angr Installation Guide

## Introduction
Angr è un framework per analisi binaria che combina esecuzione simbolica, fuzzing e analisi statica.

## Installation Methods

### Method 1: PIP Installation
```bash
# Create virtual environment
python3 -m venv angr-env
source angr-env/bin/activate

# Install angr
pip install angr

Method 2: From Source
bash
git clone https://github.com/angr/angr.git
cd angr
pip install -e .
Method 3: Kali Linux
bash
sudo apt update
sudo apt install python3-angr
Dependencies
System Dependencies
bash
# Ubuntu/Debian
sudo apt install python3-dev libffi-dev build-essential

# Additional tools
sudo apt install cmake git
Python Dependencies
bash
pip install wheel unicorn capstone ropper
Verification
Test Installation
python
import angr
import claripy

print("Angr version:", angr.__version__)
print("Installation successful!")
Simple Example
python
import angr

# Load binary
project = angr.Project("/bin/true", auto_load_libs=False)

# Create initial state
state = project.factory.entry_state()

# Create simulation manager
simgr = project.factory.simulation_manager(state)

print("Binary loaded successfully!")
Common Issues & Solutions
Issue 1: Unicorn Engine
bash
# Reinstall unicorn
pip uninstall unicorn
pip install unicorn --no-binary=unicorn
Issue 2: Z3 Solver
bash
# Install z3 separately
pip install z3-solver
Issue 3: Library Dependencies
bash
# Install missing libraries
sudo apt install libssl-dev libffi-dev
Usage Examples
Basic Symbolic Execution
python
import angr

project = angr.Project('vulnerable_binary')
initial_state = project.factory.entry_state()
simgr = project.factory.simgr(initial_state)

# Explore to find specific address
simgr.explore(find=0x400000)
Constraint Solving
python
import claripy

# Create symbolic variables
x = claripy.BVS('x', 32)
y = claripy.BVS('y', 32)

# Add constraints
constraints = [x > 10, y < 20, x + y == 30]

# Solve
solver = claripy.Solver()
solution = solver.eval(x, 1, extra_constraints=constraints)
Integration with Other Tools
AFL + Angr
python
# Use angr to generate test cases for AFL
import angr
import afl

afl.init()
IDA Pro Integration
python
# Use angr with IDA Pro for binary analysis
import angr
import idc
Best Practices
1. Virtual Environments
Sempre usa ambienti virtuali per evitare conflitti di dipendenze.

2. Memory Management
Angr può usare molta memoria. Monitora l'utilizzo durante analisi lunghe.

3. Performance Optimization
Disabilita auto_load_libs per binari semplici

Usa concrete per analisi più veloci

Limita la profondità di esplorazione
