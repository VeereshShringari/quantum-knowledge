"""
Shor's Algorithm Implementation using Qiskit
This module demonstrates Shor's algorithm for integer factorization.
"""

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator
import numpy as np
from math import gcd
from fractions import Fraction


def classical_order_finding(a, N):
    """
    Classical function to find the order (period) r such that a^r mod N = 1
    This is used for verification and when quantum part fails
    """
    if gcd(a, N) != 1:
        return None
    
    r = 1
    result = a
    while result != 1:
        result = (result * a) % N
        r += 1
        if r > N:  # Safety check
            return None
    return r


def shors_algorithm_classical(N):
    """
    Classical implementation of Shor's algorithm for educational purposes
    Demonstrates the complete algorithm flow
    """
    print(f"\n{'='*60}")
    print(f"Factoring N = {N} using Shor's Algorithm (Classical simulation)")
    print(f"{'='*60}\n")
    
    # Step 1: Check if N is even
    if N % 2 == 0:
        print(f"N is even. Factor found: 2")
        return 2
    
    # Step 2: Check if N is a prime power
    for p in range(2, int(np.sqrt(N)) + 1):
        if N % p == 0:
            print(f"Found factor using trial division: {p}")
            return p
    
    # Step 3: Choose random a < N
    np.random.seed(42)
    attempts = 0
    max_attempts = 10
    
    while attempts < max_attempts:
        attempts += 1
        a = np.random.randint(2, N)
        
        print(f"\nAttempt {attempts}: Chosen a = {a}")
        
        # Step 4: Check if gcd(a, N) != 1
        g = gcd(a, N)
        if g != 1:
            print(f"Found factor via GCD: {g}")
            return g
        
        # Step 5: Find period r (this would be done quantum mechanically)
        print(f"Finding period r such that {a}^r ≡ 1 (mod {N})...")
        r = classical_order_finding(a, N)
        
        if r is None:
            print("Failed to find period. Trying another a...")
            continue
        
        print(f"Period found: r = {r}")
        
        # Step 6: Check if r is odd or a^(r/2) ≡ -1 (mod N)
        if r % 2 != 0:
            print("Period is odd. Trying another a...")
            continue
        
        x = pow(a, r // 2, N)
        if x == N - 1:
            print(f"a^(r/2) ≡ -1 (mod N). Trying another a...")
            continue
        
        # Step 7: Compute factors
        factor1 = gcd(x + 1, N)
        factor2 = gcd(x - 1, N)
        
        print(f"\nCalculating factors:")
        print(f"  gcd({a}^({r}//2) + 1, {N}) = gcd({x + 1}, {N}) = {factor1}")
        print(f"  gcd({a}^({r}//2) - 1, {N}) = gcd({x - 1}, {N}) = {factor2}")
        
        if factor1 != 1 and factor1 != N:
            print(f"\n✓ Success! Found non-trivial factor: {factor1}")
            print(f"  {N} = {factor1} × {N // factor1}")
            return factor1
        
        if factor2 != 1 and factor2 != N:
            print(f"\n✓ Success! Found non-trivial factor: {factor2}")
            print(f"  {N} = {factor2} × {N // factor2}")
            return factor2
    
    print(f"\nFailed to find factors after {max_attempts} attempts")
    return None


def create_qft_circuit(n):
    """
    Create Quantum Fourier Transform circuit for n qubits
    QFT is a key component of Shor's algorithm
    """
    qc = QuantumCircuit(n)
    
    def qft_rotations(circuit, n):
        """Performs QFT rotations on n qubits"""
        if n == 0:
            return circuit
        n -= 1
        circuit.h(n)
        for qubit in range(n):
            circuit.cp(np.pi/2**(n-qubit), qubit, n)
        qft_rotations(circuit, n)
    
    def swap_registers(circuit, n):
        """Swaps qubits at opposite ends"""
        for qubit in range(n//2):
            circuit.swap(qubit, n-qubit-1)
        return circuit
    
    qft_rotations(qc, n)
    swap_registers(qc, n)
    
    return qc


def create_inverse_qft_circuit(n):
    """
    Create inverse Quantum Fourier Transform circuit
    """
    qc = create_qft_circuit(n)
    return qc.inverse()


def quantum_period_finding_circuit(a, N, n_count):
    """
    Create quantum circuit for period finding
    This is the quantum part of Shor's algorithm
    
    Args:
        a: The base number
        N: The number to factor
        n_count: Number of counting qubits (determines precision)
    """
    # Create quantum registers
    qr_count = QuantumRegister(n_count, 'counting')
    qr_aux = QuantumRegister(N.bit_length(), 'auxiliary')
    cr = ClassicalRegister(n_count, 'classical')
    qc = QuantumCircuit(qr_count, qr_aux, cr)
    
    # Initialize auxiliary register to |1⟩
    qc.x(qr_aux[0])
    
    # Apply Hadamard gates to counting register
    for qubit in range(n_count):
        qc.h(qr_count[qubit])
    
    # Apply controlled-U^(2^j) operations
    # This performs modular exponentiation: |j⟩|x⟩ -> |j⟩|a^(2^j) * x mod N⟩
    for j in range(n_count):
        power = 2**j
        controlled_power_mod = pow(a, power, N)
        # In a full implementation, we would create controlled modular 
        # multiplication gates here
        qc.barrier()
    
    qc.barrier()
    
    # Apply inverse QFT to counting register
    qc.append(create_inverse_qft_circuit(n_count), qr_count)
    
    # Measure counting register
    qc.measure(qr_count, cr)
    
    return qc


def demonstrate_qft():
    """
    Demonstrate Quantum Fourier Transform
    """
    print(f"\n{'='*60}")
    print("Quantum Fourier Transform (QFT) - Key component of Shor's Algorithm")
    print(f"{'='*60}\n")
    
    n_qubits = 3
    qc = create_qft_circuit(n_qubits)
    
    print(f"QFT circuit for {n_qubits} qubits:")
    print(qc.draw(output='text'))
    
    # Create a test circuit
    test_qc = QuantumCircuit(n_qubits, n_qubits)
    
    # Prepare initial state |1⟩
    test_qc.x(0)
    test_qc.barrier()
    
    # Apply QFT operations inline instead of composing
    test_qc.compose(qc, inplace=True)
    test_qc.barrier()
    
    # Measure
    test_qc.measure(range(n_qubits), range(n_qubits))
    
    print("\nTest circuit with initial state |001⟩:")
    print(test_qc.draw(output='text'))
    
    # Simulate
    simulator = AerSimulator()
    job = simulator.run(test_qc, shots=1000)
    result = job.result()
    counts = result.get_counts()
    
    print("\nMeasurement results:")
    for state, count in sorted(counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  |{state}⟩: {count} times ({count/10:.1f}%)")


def demonstrate_period_finding():
    """
    Demonstrate the period finding aspect of Shor's algorithm
    """
    print(f"\n{'='*60}")
    print("Period Finding - Quantum Component of Shor's Algorithm")
    print(f"{'='*60}\n")
    
    # Example: Find period of a^x mod N
    a = 7
    N = 15
    
    print(f"Finding period r such that {a}^r ≡ 1 (mod {N})")
    print(f"\nSequence of powers:")
    
    for x in range(1, 10):
        result = pow(a, x, N)
        print(f"  {a}^{x} mod {N} = {result}")
        if result == 1:
            print(f"\nPeriod found: r = {x}")
            break
    
    # Create quantum circuit (simplified)
    n_count = 4
    print(f"\nCreating quantum circuit with {n_count} counting qubits...")
    qc = quantum_period_finding_circuit(a, N, n_count)
    print(qc.draw(output='text'))


def main():
    """Run Shor's algorithm demonstrations"""
    print("\n" + "="*60)
    print("SHOR'S ALGORITHM FOR INTEGER FACTORIZATION")
    print("="*60)
    
    # Demonstrate QFT
    demonstrate_qft()
    
    # Demonstrate period finding
    demonstrate_period_finding()
    
    # Factor small numbers using classical simulation
    print("\n" + "="*60)
    print("Classical Simulation Examples")
    print("="*60)
    
    numbers_to_factor = [15, 21, 35]
    
    for N in numbers_to_factor:
        factor = shors_algorithm_classical(N)
        if factor:
            print(f"\n✓ Successfully factored {N} = {factor} × {N // factor}")
    
    print("\n" + "="*60)
    print("NOTES:")
    print("="*60)
    print("""
Shor's Algorithm Overview:
1. Classical preprocessing: Check if N is even or a prime power
2. Choose random a < N where gcd(a, N) = 1
3. **Quantum Step**: Use quantum period finding to find period r
   - This is exponentially faster than classical methods!
   - Uses quantum superposition and interference
4. Post-processing: Use r to find factors via gcd(a^(r/2) ± 1, N)

Key Quantum Components:
- Quantum Fourier Transform (QFT)
- Modular exponentiation using quantum gates
- Measurement and classical post-processing

This implementation shows the classical simulation for educational purposes.
A real quantum implementation would provide exponential speedup for large numbers.
""")


if __name__ == "__main__":
    main()
