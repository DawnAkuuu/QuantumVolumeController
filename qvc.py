import asyncio
import subprocess
import tkinter as tk
from tkinter import ttk
from tkinter.constants import HORIZONTAL

import cirq

final_volume = 0

def super_position():
    qubit = cirq.GridQubit(0, 0)
    circuit = cirq.Circuit(cirq.X(qubit) ** 0.5, cirq.measure(qubit, key="m"))
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=7)

    global final_volume

    bit_list = result.measurements["m"].flatten()
    binary_str = "".join(map(str, bit_list))
    final_volume = int(binary_str, 2) % 101
    progress_bar.config(mode="indeterminate")
    progress_bar.start(2)
    label.config(text="Superpositioning Particles")
    messages = [
        "Initializing Qubits",
        "Entangling Particles",
        "Analyzing Wave Functions",
        "Making Spaghetti :D",
        "Looking at Schrodingers Cat",
        "Collapsing States",
    ]
    update_labels(messages)

    root.after(5500, set_volume)


def update_labels(messages):
    if messages:

        current_message = messages.pop(0)
        label.config(text=current_message)

        if messages:
            root.after(800, lambda: update_labels(messages))

def set_volume():

    progress_bar.stop()

   # Update UI
    label.config(text=f"Collapsed Volume: {final_volume}%")
    progress_bar.config(value=final_volume, mode="determinate")
    subprocess.run(["osascript", "-e", f"set volume output volume {final_volume}"])

# --- UI SETUP ---
root = tk.Tk()
root.title("Quantum Volume")
root.geometry("500x400")  # Wider and taller to ensure visibility
root.attributes("-topmost", True)

# Create a main frame to hold everything centered
frame = tk.Frame(root)
frame.place(relx=0.5, rely=0.5, anchor="center")

# Row 0: The Label
label = tk.Label(frame, text="Current Volume: --%")
label.grid(row=0, column=0)

# Row 1: The Button
btn = tk.Button(
    frame, text="⚛️ Get Quantum Volume", command=super_position, padx=20, pady=10
)
btn.grid(row=1, column=0)

progress_bar = ttk.Progressbar(frame, orient=HORIZONTAL, mode="determinate")
progress_bar.grid(row=2, column=0)

# Initial volume check so it doesn't say "idk"
try:
    current = (
        subprocess.check_output(
            ["osascript", "-e", "output volume of (get volume settings)"]
        )
        .decode()
        .strip()
    )
    label.config(text=f"Current Volume: {current}%")
    progress_bar.config(value=int(current))
except:
    pass

root.mainloop()
