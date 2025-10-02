"""
Quantum Gates Examples using Qiskit
This module demonstrates the implementation and visualization of basic quantum gates.
"""

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.visualization import plot_histogram, circuit_drawer
from qiskit_aer import AerSimulator
import numpy as np


def hadamard_gate_example():
    """
    Hadamard Gate: Creates superposition
    H|0⟩ = (|0⟩ + |1⟩)/√2
    """
    print("\n=== Hadamard Gate Example ===")
    qc = QuantumCircuit(1, 1)
    qc.h(0)  # Apply Hadamard gate
    qc.measure(0, 0)
    
    print(qc.draw(output='text'))
    
    # Simulate
    simulator = AerSimulator()
    job = simulator.run(qc, shots=1000)
    result = job.result()
    counts = result.get_counts()
    print(f"Results: {counts}")
    print("Expected: ~50% |0⟩ and ~50% |1⟩")
    return qc


def pauli_gates_example():
    """
    Pauli Gates: X (NOT), Y, Z gates
    X|0⟩ = |1⟩, X|1⟩ = |0⟩
    """
    print("\n=== Pauli-X Gate (NOT Gate) Example ===")
    qc = QuantumCircuit(1, 1)
    qc.x(0)  # Apply X gate (bit flip)
    qc.measure(0, 0)
    
    print(qc.draw(output='text'))
    
    simulator = AerSimulator()
    job = simulator.run(qc, shots=1000)
    result = job.result()
    counts = result.get_counts()
    print(f"Results: {counts}")
    print("Expected: 100% |1⟩")
    
    # Pauli-Y Gate
    print("\n=== Pauli-Y Gate Example ===")
    qc_y = QuantumCircuit(1, 1)
    qc_y.y(0)  # Apply Y gate
    qc_y.measure(0, 0)
    print(qc_y.draw(output='text'))
    
    # Pauli-Z Gate
    print("\n=== Pauli-Z Gate Example ===")
    qc_z = QuantumCircuit(1, 1)
    qc_z.h(0)  # Create superposition first
    qc_z.z(0)  # Apply Z gate (phase flip)
    qc_z.h(0)  # Apply Hadamard again
    qc_z.measure(0, 0)
    print(qc_z.draw(output='text'))
    
    return qc


def cnot_gate_example():
    """
    CNOT Gate: Controlled-NOT gate (2-qubit gate)
    Creates entanglement between qubits
    """
    print("\n=== CNOT Gate (Controlled-NOT) Example ===")
    qc = QuantumCircuit(2, 2)
    
    # Prepare Bell State: (|00⟩ + |11⟩)/√2
    qc.h(0)  # Create superposition on qubit 0
    qc.cx(0, 1)  # Apply CNOT with qubit 0 as control, qubit 1 as target
    qc.measure([0, 1], [0, 1])
    
    print(qc.draw(output='text'))
    
    simulator = AerSimulator()
    job = simulator.run(qc, shots=1000)
    result = job.result()
    counts = result.get_counts()
    print(f"Results: {counts}")
    print("Expected: ~50% |00⟩ and ~50% |11⟩ (entangled state)")
    return qc


def phase_gate_example():
    """
    Phase Gates: S and T gates
    S gate: Adds π/2 phase, T gate: Adds π/4 phase
    """
    print("\n=== S Gate (Phase Gate) Example ===")
    qc = QuantumCircuit(1, 1)
    qc.h(0)
    qc.s(0)  # Apply S gate
    qc.h(0)
    qc.measure(0, 0)
    
    print(qc.draw(output='text'))
    
    print("\n=== T Gate (π/8 Gate) Example ===")
    qc_t = QuantumCircuit(1, 1)
    qc_t.h(0)
    qc_t.t(0)  # Apply T gate
    qc_t.h(0)
    qc_t.measure(0, 0)
    
    print(qc_t.draw(output='text'))
    return qc


def swap_gate_example():
    """
    SWAP Gate: Swaps the states of two qubits
    """
    print("\n=== SWAP Gate Example ===")
    qc = QuantumCircuit(2, 2)
    
    # Prepare qubit 0 in |1⟩ state
    qc.x(0)
    qc.barrier()
    
    # Apply SWAP gate
    qc.swap(0, 1)
    qc.barrier()
    
    qc.measure([0, 1], [0, 1])
    
    print(qc.draw(output='text'))
    
    simulator = AerSimulator()
    job = simulator.run(qc, shots=1000)
    result = job.result()
    counts = result.get_counts()
    print(f"Results: {counts}")
    print("Expected: 100% |01⟩ (states swapped)")
    return qc


def toffoli_gate_example():
    """
    Toffoli Gate (CCX): Controlled-Controlled-NOT gate
    3-qubit gate, flips target if both controls are |1⟩
    """
    print("\n=== Toffoli Gate (CCNOT) Example ===")
    qc = QuantumCircuit(3, 3)
    
    # Set control qubits to |1⟩
    qc.x(0)
    qc.x(1)
    qc.barrier()
    
    # Apply Toffoli gate
    qc.ccx(0, 1, 2)  # Controls: 0, 1; Target: 2
    qc.barrier()
    
    qc.measure([0, 1, 2], [0, 1, 2])
    
    print(qc.draw(output='text'))
    
    simulator = AerSimulator()
    job = simulator.run(qc, shots=1000)
    result = job.result()
    counts = result.get_counts()
    print(f"Results: {counts}")
    print("Expected: 100% |111⟩")
    return qc


def rotation_gates_example():
    """
    Rotation Gates: RX, RY, RZ
    Rotate qubit state around X, Y, Z axis
    """
    print("\n=== Rotation Gates Example ===")
    qc = QuantumCircuit(1, 1)
    
    # Rotate by π/2 around Y-axis
    qc.ry(np.pi/2, 0)
    qc.measure(0, 0)
    
    print(qc.draw(output='text'))
    
    simulator = AerSimulator()
    job = simulator.run(qc, shots=1000)
    result = job.result()
    counts = result.get_counts()
    print(f"Results: {counts}")
    print("Expected: ~50% |0⟩ and ~50% |1⟩")
    return qc


def main():
    """Run all quantum gate examples"""
    print("="*60)
    print("QUANTUM GATES EXAMPLES")
    print("="*60)
    
    hadamard_gate_example()
    pauli_gates_example()
    cnot_gate_example()
    phase_gate_example()
    swap_gate_example()
    toffoli_gate_example()
    rotation_gates_example()
    
    print("\n" + "="*60)
    print("All examples completed!")
    print("="*60)


if __name__ == "__main__":
    main()
