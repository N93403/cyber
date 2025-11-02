#!/usr/bin/env python3
import sys
import afl
import os

def test_function(a, b, c):
    """
    Example test function for AFL fuzzing
    Replace with your actual test logic
    """
    if a == 0 and b < 5 and c == 1:
        # This path triggers the assertion (simulated crash)
        assert False, "Vulnerable path triggered!"
    
    # Normal execution
    return a + b + c

def main():
    try:
        in_str = sys.stdin.read()
        if not in_str.strip():
            return
            
        values = [int(x) for x in in_str.strip().split()]
        if len(values) >= 3:
            test_function(values[0], values[1], values[2])
            
    except Exception as e:
        # AFL will detect crashes from exceptions
        pass

if __name__ == "__main__":
    afl.init()
    main()
    os._exit(0)

#Setup e Esecuzione
# Compila con AFL
afl-gcc -o vulnerable_app vulnerable_app.c

# Prepara test cases
mkdir input output
echo "1 2 3" > input/test1.txt

# Esegui fuzzing
afl-fuzz -i input -o output -- ./vulnerable_app @@
