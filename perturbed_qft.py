import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, CheckButtons, Button
from qiskit import QuantumCircuit
from qiskit.circuit.library import QFT
from qiskit.quantum_info import Statevector

def create_circuit(input_num, thetas, use_iqft, use_final_qft):
    num_qubits = 4
    qc = QuantumCircuit(num_qubits)
    
    # Initialize the input number representation (0 to 15)
    binary_str = format(int(input_num), '04b')
    for i, bit in enumerate(reversed(binary_str)): # Qiskit's little-endian ordering
        if bit == '1':
            qc.x(i)
            
    # Apply initial Inverse QFT (or normal QFT if desired, but user specified iqt)
    if use_iqft:
        qc.append(QFT(num_qubits, inverse=True), range(num_qubits))
    
    # Apply phase gates (theta per qubit)
    for i in range(num_qubits):
        qc.p(thetas[i], i)
        
    # Optional final QFT to decode the perturbed phase state
    if use_final_qft:
        qc.append(QFT(num_qubits, inverse=True), range(num_qubits))
        
    return qc



# =============================================================================
# NEW 3D SURFACE PLOTS CODE
# =============================================================================
def main():
    use_iqft = True
    use_final_qft = True
    
    # Create a 16x16 grid for configurations
    theta_nums = np.arange(16)
    input_nums = np.arange(16)
    X, Y = np.meshgrid(theta_nums, input_nums)
    
    # Array to hold marginal probabilities for all 4 qubits
    Z = np.zeros((4, 16, 16))
    
    for i in range(16): # rows: inputs
        for j in range(16): # columns: thetas
            input_num = Y[i, j]
            theta_num = X[i, j]
            
            # Map theta binary string to actual phase angles
            # e.g. theta_num=1 is '0001', bit='1' -> np.pi, bit='0' -> 0.0
            binary_theta = format(theta_num, '04b')
            thetas = [np.pi if bit == '1' else 0.0 for bit in reversed(binary_theta)]
            
            # Simulate the circuit
            qc = create_circuit(input_num, thetas, use_iqft, use_final_qft)
            sv = Statevector(qc)
            probs = sv.probabilities_dict()
            
            # Compute marginal probability of measuring |1> for each qubit
            marginal_probs = np.zeros(4)
            for state_str, p in probs.items():
                if state_str[3] == '1': marginal_probs[0] += p # q0
                if state_str[2] == '1': marginal_probs[1] += p # q1
                if state_str[1] == '1': marginal_probs[2] += p # q2
                if state_str[0] == '1': marginal_probs[3] += p # q3
                
            Z[0, i, j] = marginal_probs[0]
            Z[1, i, j] = marginal_probs[1]
            Z[2, i, j] = marginal_probs[2]
            Z[3, i, j] = marginal_probs[3]
            
    # Draw the four 3D Surface Plots
    fig = plt.figure(figsize=(16, 12))
    
    for q in range(4):
        ax = fig.add_subplot(2, 2, q+1, projection='3d')
        
        # X: Thetas (0-15), Y: Inputs (0-15), Z: Probability
        surf = ax.plot_surface(X, Y, Z[q], cmap='viridis', edgecolor='none')
        
        ax.set_title(f'Qubit {q} Marginal Probability of |1>')
        ax.set_xlabel('Thetas (Binary 0-15)')
        ax.set_ylabel('Input State (Binary 0-15)')
        ax.set_zlabel('P(|1>)')
        ax.set_zlim(0, 1)
        
        fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5, pad=0.1)
        
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    main()
