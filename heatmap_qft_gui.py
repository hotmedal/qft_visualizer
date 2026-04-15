import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from qiskit.quantum_info import Statevector
from perturbed_qft import create_circuit

def get_marginal_probs(input_num, thetas, use_iqft, use_final_qft):
    qc = create_circuit(input_num, thetas, use_iqft, use_final_qft)
    sv = Statevector(qc)
    probs = sv.probabilities_dict()
    
    marginal_probs = np.zeros(4)
    for state_str, p in probs.items():
        if state_str[3] == '1': marginal_probs[0] += p # q0 (Least significant bit)
        if state_str[2] == '1': marginal_probs[1] += p # q1
        if state_str[1] == '1': marginal_probs[2] += p # q2
        if state_str[0] == '1': marginal_probs[3] += p # q3 (Most significant bit)
        
    return marginal_probs

def main():
    fig, ax = plt.subplots(figsize=(12, 7))
    plt.subplots_adjust(left=0.15, bottom=0.35)
    
    initial_thetas = [0.0, 0.0, 0.0, 0.0]
    
    # Pre-compute initial configuration probabilities
    Z = np.zeros((4, 16))
    for inp in range(16):
        Z[:, inp] = get_marginal_probs(inp, initial_thetas, True, True)
        
    # Draw static heatmap framework
    cax = ax.imshow(Z, aspect='auto', cmap='viridis', origin='lower', vmin=0, vmax=1)
    
    # Beautiful colorbar
    cbar = fig.colorbar(cax, ax=ax, pad=0.02)
    cbar.set_label('Marginal Probability $P(|1\\rangle)$')
    
    # Fix Y-ticks for Qubits
    ax.set_yticks([0, 1, 2, 3])
    ax.set_yticklabels(['Qubit 0', 'Qubit 1', 'Qubit 2', 'Qubit 3'])
    
    # Fix X-ticks for binary input states
    ax.set_xticks(np.arange(16))
    ax.set_xticklabels([f"({i}) |{format(i, '04b')}>" for i in range(16)], rotation=90)
    
    ax.set_xlabel('Computational Input State')
    ax.set_title('Continuous Interference Mapping: 16-State Output Probabilities')
    
    # Axes for sliders located at bottom
    axcolor = 'lightgoldenrodyellow'
    ax_theta0 = plt.axes([0.15, 0.20, 0.65, 0.03], facecolor=axcolor)
    ax_theta1 = plt.axes([0.15, 0.15, 0.65, 0.03], facecolor=axcolor)
    ax_theta2 = plt.axes([0.15, 0.10, 0.65, 0.03], facecolor=axcolor)
    ax_theta3 = plt.axes([0.15, 0.05, 0.65, 0.03], facecolor=axcolor)
    
    # Initialize the sliders mapping continuous range -pi to pi
    s_theta0 = Slider(ax_theta0, 'Theta 0 (rad)', -np.pi, np.pi, valinit=initial_thetas[0])
    s_theta1 = Slider(ax_theta1, 'Theta 1 (rad)', -np.pi, np.pi, valinit=initial_thetas[1])
    s_theta2 = Slider(ax_theta2, 'Theta 2 (rad)', -np.pi, np.pi, valinit=initial_thetas[2])
    s_theta3 = Slider(ax_theta3, 'Theta 3 (rad)', -np.pi, np.pi, valinit=initial_thetas[3])
    
    # Fast recalculation callback
    def update(val):
        thetas = [s_theta0.val, s_theta1.val, s_theta2.val, s_theta3.val]
        
        new_Z = np.zeros((4, 16))
        for inp in range(16):
            new_Z[:, inp] = get_marginal_probs(inp, thetas, True, True)
            
        # Update merely the data, not the plot layout! Keep everything fast.
        cax.set_data(new_Z)
        fig.canvas.draw_idle()
        
    # Hook sliders into update callback
    s_theta0.on_changed(update)
    s_theta1.on_changed(update)
    s_theta2.on_changed(update)
    s_theta3.on_changed(update)
    
    # Present UI
    plt.show()

if __name__ == '__main__':
    main()
