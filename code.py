import networkx as nx
import random
import matplotlib.pyplot as plt
import pandas as pd

class EpidemicSimulation:
    def __init__(self, graph, ptrans, tREC, tSUS, starting_infected_nodes):
        self.graph = graph
        self.ptrans = ptrans
        self.tREC = tREC
        self.tSUS = tSUS
        self.pos = nx.spring_layout(self.graph, seed=1)
        self.initialize_nodes()
        self.infection_counts = {node: 0 for node in self.graph.nodes}
        self.infected_edges = {}
        self.new_simulation = new_simulation
        self.starting_infected_nodes = starting_infected_nodes

    def initialize_nodes(self):
        for node in self.graph.nodes:
            self.graph.nodes[node]['state'] = 'Susceptible'
            self.graph.nodes[node]['recovery_time'] = 0
            self.graph.nodes[node]['susceptible_time'] = 0
        print("Initially infected nodes", starting_infected_nodes, "\n")
        for node in starting_infected_nodes:
            self.graph.nodes[node]['state'] = 'Infected'

    def update_node_states(self):
        self.infected_edges = {}
        new_infected_nodes = []
        for node in list(self.graph.nodes):
            state = self.graph.nodes[node]['state']

            if state == 'Infected':
                if self.graph.nodes[node]['recovery_time'] == self.tREC:
                    self.graph.nodes[node]['state'] = 'Recovered'
                    self.graph.nodes[node]['recovery_time'] = 0
                    self.graph.nodes[node]['susceptible_time'] = 0
                else:
                    self.graph.nodes[node]['recovery_time'] += 1

            elif state == 'Recovered':
                if self.tSUS == float('inf'):
                    continue  # Node will never become susceptible again
                elif self.graph.nodes[node]['susceptible_time'] == self.tSUS - 1:
                    self.graph.nodes[node]['state'] = 'Susceptible'
                    self.graph.nodes[node]['susceptible_time'] = 0
                else:
                    self.graph.nodes[node]['susceptible_time'] += 1

            elif state == 'Susceptible':
                infected_neighbors = [n for n in self.graph.neighbors(node) if self.graph.nodes[n]['state'] == 'Infected']
                for neighbor in infected_neighbors:
                    if random.random() <= self.ptrans and neighbor not in new_infected_nodes:
                        self.graph.nodes[node]['state'] = 'Infected'
                        self.infection_counts[neighbor] += 1
                        self.infected_edges[node] = neighbor
                        new_infected_nodes.append(node)
                        print("•", neighbor, "ha infettato", node, "\n")
                        break

    def run_simulation(self):
        self.visualize(-1)
        step = 0
        while not self.all_nodes_susceptible():
            self.update_node_states()
            self.visualize(step)
            step += 1
            if step == 100:
                print("\nMaximum number of steps reached. The simulation has been interrupted.\n")
                break

        max_infections = max(self.infection_counts.values())
        superspreaders = [node for node, count in self.infection_counts.items() if count == max_infections]
        if step < 100:
            print("\nSimulation ended at step ",step,", there aren't any infected nodes.\n")
        print("\033[1mSimulation Data:\nStarting infected nodes:\033[0m ", starting_infected_nodes, "\n\033[1mInfection probability:\033[0m ", ptrans*100, "% | \033[1mRecovery Steps:\033[0m ", tREC, " | \033[1mImmunity Steps:\033[0m ", tSUS)
        if(max_infections==0):
            print("No superspreader: 0 total infections.")
        else:
            print("\033[1mSuperspreaders\033[0m (",max_infections," infections ): ",superspreaders, "\n")

    def all_nodes_susceptible(self):
        for node in self.graph.nodes:
            state = self.graph.nodes[node]['state']
            if state == 'Infected':
                return False
        return True

    def visualize(self, step):
        state_colors = {'Susceptible': 'green', 'Infected': 'red', 'Recovered': 'orange'}
        node_colors = [state_colors[self.graph.nodes[node]['state']] for node in self.graph.nodes]
        edge_colors = ['red' if (u, v) in self.infected_edges.items() or (v, u) in self.infected_edges.items() else 'blue'
                       for u, v in self.graph.edges()]
        fig, ax = plt.subplots(figsize=(10, 10))
        nx.draw(self.graph, pos=self.pos, with_labels=True, node_color=node_colors, edge_color=edge_colors,
                node_size=500, font_size=10)
        if step >= 0:
            plt.title(f"Grafo allo step {step+1}")
        else:
            plt.title("Stato iniziale")
        self.infected_edges = {}
        plt.show()


def load_graph_from_csv(csv_file):
    df = pd.read_csv(csv_file)
    G = nx.Graph()
    for _, row in df.iterrows():
        G.add_edge(row['source'], row['target'])
    return G


graph = load_graph_from_csv('test.csv')
##input for the number of starting infected nodes
while True:
    try:
      n_infected = int(input("Input the number of starting infected nodes: "))
      if n_infected > graph.number_of_nodes():
        print("The number of infected cannot exceed the number of nodes.")
        continue
      elif n_infected < 0:
        print("The number of infected nodes cannot be negative.")
        continue
      break
    except ValueError or TypeError:
        print("The value entered is not an integer.")

starting_infected_nodes = random.sample(list(graph.nodes), n_infected) #randomly defining starting infected nodes 
new_simulation= 'n' #variable for starting new simulations
mod_val = 'n' #variabile for editing initial values

while True:
    if new_simulation=='n' or mod_val=='y':
        ##input probability of infection
        while True:
          try:
            ptrans = float(input("Enter the probability (in percentage) of infection of the neighbours: "))
            if ptrans > 100 or ptrans < 0:
              print("The probability of infection must be between 0 and 100.")
              continue
            break
          except ValueError or TypeError:
            print("The value entered is invalid.")
        ptrans = ptrans / 100
        ##input step for recovery
        while True:
            try:
              tREC = int(input("Enter the number of steps for recovery: "))
              if tREC <= 0:
                print("The number of steps must be greater than 0.")
                continue
              break
            except ValueError or TypeError:
                print("The value entered is not an integer.")
        ##input step for immunity
        while True:
          tSUS_input = input("Enter the number of steps to become vulnerable again (‘?’ for infinity): ")
          if tSUS_input == '?':
              tSUS = float('inf')
              break
          else:
            try:
              tSUS = int(tSUS_input)
              if tSUS < 0:
                  print("The number of steps must be greater than or equal to 0.")
              else:
                  break
            except ValueError or TypeError:
                print("The value entered is not an integer.")


    ##avvio della simulazione
    simulation = EpidemicSimulation(graph, ptrans, tREC, tSUS, starting_infected_nodes)
    simulation.run_simulation()

    while True:
        new_simulation = input("Do you want to start a new simulation with the same initial states of the nodes? y/n: ")
        if new_simulation in ['y', 'n']:
            break
        else:
            print("Invalid value. Enter ‘y’ or ‘n’.")
    if new_simulation == 'y':
        while True:
          mod_val = input("Do you want to change the values of the variables? y/n: ")
          if mod_val in ['y', 'n']:
            break
          else:
            print("Invalid value. Enter ‘y’ or ‘n’.")
    else:
        break
