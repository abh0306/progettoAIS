# Epidemic Simulation on Graphs

This project implements an epidemic simulation on graphs using NetworkX.
The model follows infection, recovery, and return-to-susceptibility dynamics, and visualizes the epidemic evolution with Matplotlib.

## Features

-Load a graph from a .csv edge list file.

-Random selection of initially infected nodes.

-Customizable parameters:

- Infection probability (ptrans)

- Number of steps to recover (tREC)

- Number of steps of immunity (tSUS, with option for infinity ?)

-Step-by-step visualization with node colors:

🟩 Susceptible

🟥 Infected

🟧 Recovered

-Final statistics:

 - Infection count per node

 - Identification of potential superspreaders

 -Option to restart simulations with the same or new parameters.

## CSV file format

The graph is defined by an edge list with headers source and target.
A .csv file is necessary to run the program.

## Usage

Clone the repository:

```sh
git clone https://github.com/your-username/epidemic-simulation.git
cd epidemic-simulation
   ```

Install dependencies:
```sh
pip install networkx matplotlib pandas
```

Run the script:

```sh
python epidemic_simulation.py
   ```

## Technologies

Python 3.x

NetworkX
 → graph management

Matplotlib
 → visualization

Pandas
 → CSV file handling

 ## Notes

The simulation ends when there are no infected nodes left or after 100 steps (to prevent infinite loops).

If no node spreads the infection, there are no superspreaders.
