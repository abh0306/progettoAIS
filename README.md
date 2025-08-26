Epidemic Simulation

This project implements an epidemic simulation model on networks using Python, NetworkX, and Matplotlib.
It allows users to simulate how an infection spreads across a network of connected nodes, with customizable parameters such as infection probability, recovery time, and immunity duration.

The simulation is visualized step by step on a graph, where each node represents an individual and edges represent possible transmission paths.

✨ Features
	•	🦠 Customizable epidemic model
	•	Infection probability (ptrans)
	•	Recovery time (tREC)
	•	Immunity duration (tSUS) – can also be infinite
	•	🎲 Random initial infections – select the number of initially infected nodes randomly from the network
	•	📊 Tracking infection spread – count infections per node and identify superspreaders
	•	🎨 Graph visualization – animated step-by-step simulation with color-coded states:
	•	🟢 Susceptible
	•	🔴 Infected
	•	🟠 Recovered
	•	📂 CSV-based graph loading – define the network edges in a .csv file
