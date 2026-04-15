import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, CheckButtons, Button
from qiskit.quantum_info import Statevector
from perturbed_qft import create_circuit

def main():
    fig, ax = plt.subplots(figsize=(10, 7))
    plt.subplots_adjust(left=0.15, bottom=0.50)
    
    initial_num = 0
    initial_thetas = [0.0, 0.0, 0.0, 0.0]
    
    axcolor = 'lightgoldenrodyellow'
    
    # Create axes for sliders
    ax_theta0 = plt.axes([0.15, 0.40, 0.70, 0.03], facecolor=axcolor)
    ax_theta1 = plt.axes([0.15, 0.35, 0.70, 0.03], facecolor=axcolor)
    ax_theta2 = plt.axes([0.15, 0.30, 0.70, 0.03], facecolor=axcolor)
    ax_theta3 = plt.axes([0.15, 0.25, 0.70, 0.03], facecolor=axcolor)
    ax_input  = plt.axes([0.15, 0.15, 0.70, 0.03], facecolor=axcolor)
    ax_check  = plt.axes([0.15, 0.02, 0.35, 0.10], frameon=False)
    ax_btn    = plt.axes([0.55, 0.04, 0.30, 0.06])
    
    # Setup sliders
    s_theta0 = Slider(ax_theta0, 'Theta 0 (rad)', -np.pi, np.pi, valinit=initial_thetas[0])
    s_theta1 = Slider(ax_theta1, 'Theta 1 (rad)', -np.pi, np.pi, valinit=initial_thetas[1])
    s_theta2 = Slider(ax_theta2, 'Theta 2 (rad)', -np.pi, np.pi, valinit=initial_thetas[2])
    s_theta3 = Slider(ax_theta3, 'Theta 3 (rad)', -np.pi, np.pi, valinit=initial_thetas[3])
    s_input = Slider(ax_input, 'Input State', 0, 15, valinit=initial_num, valstep=1)
    
    # Options for circuit variations
    check = CheckButtons(ax_check, ['Apply Initial IQFT', 'Apply Final QFT'], [True, False])
    
    def update(val):
        t0 = s_theta0.val
        t1 = s_theta1.val
        t2 = s_theta2.val
        t3 = s_theta3.val
        input_num = int(s_input.val)
        
        try:
            status = check.get_status()
            use_iqft, use_final_qft = status[0], status[1]
        except AttributeError:
            use_iqft, use_final_qft = [lines[0].get_visible() for lines in check.lines]
        
        qc = create_circuit(input_num, [t0, t1, t2, t3], use_iqft, use_final_qft)
        sv = Statevector(qc)
        probs = sv.probabilities_dict()
        
        ax.clear()
        
        all_states = [format(i, '04b') for i in range(16)]
        values = [probs.get(state, 0.0) for state in all_states]
        
        labels = [f"{state}\n({int(state, 2)})" for state in all_states]
        bars = ax.bar(labels, values, color='royalblue', edgecolor='black')
        
        ax.set_ylim(0, 1.05)
        ax.set_title(f'Sample Probabilities (Input: |{format(input_num, "04b")}>)')
        ax.set_ylabel('Probability')
        ax.tick_params(axis='x', rotation=45)
        
        fig.canvas.draw_idle()
    
    s_theta0.on_changed(update)
    s_theta1.on_changed(update)
    s_theta2.on_changed(update)
    s_theta3.on_changed(update)
    s_input.on_changed(update)
    check.on_clicked(update)
    
    btn_circuit = Button(ax_btn, 'Show Circuit')
    def on_show_circuit(event):
        try:
            status = check.get_status()
            use_iqft, use_final_qft = status[0], status[1]
        except AttributeError:
            use_iqft, use_final_qft = [lines[0].get_visible() for lines in check.lines]
            
        qc = create_circuit(int(s_input.val), [s_theta0.val, s_theta1.val, s_theta2.val, s_theta3.val], use_iqft, use_final_qft)
        
        sv = Statevector(qc)
        print("\n--- Current Circuit Diagram ---")
        print(qc.draw())
        print("\n--- Statevector (LaTeX Source) ---")
        print(sv.draw('latex_source', decimals=3))
        
        try:
            fig_c = qc.draw('mpl')
            fig_c.show()
        except Exception as e:
            print(f"Could not draw mpl circuit: {e}")
            
    btn_circuit.on_clicked(on_show_circuit)
    
    update(None)
    plt.show()

if __name__ == '__main__':
    main()
