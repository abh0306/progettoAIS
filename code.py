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
        ##gestione di una nuova simulazione con gli stessi stati iniziali
        print("Nodi infetti inizialmente:", starting_infected_nodes, "\n")
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
                    continue  # Il nodo non tornerà mai Susceptible
                elif self.graph.nodes[node]['susceptible_time'] == self.tSUS - 1:
                    self.graph.nodes[node]['state'] = 'Susceptible'
                    self.graph.nodes[node]['susceptible_time'] = 0
                else:
                    self.graph.nodes[node]['susceptible_time'] += 1

            elif state == 'Susceptible':
                infected_neighbors = [n for n in self.graph.neighbors(node) if
                                      self.graph.nodes[n]['state'] == 'Infected']
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
                print("\nNumero massimo di step raggiunto. La simulazione è stata interrotta.\n")
                break

        max_infections = max(self.infection_counts.values())
        superspreaders = [node for node, count in self.infection_counts.items() if count == max_infections]
        if step < 100:
            print("\nSimulazione terminata allo step ",step,", non ci sono più nodi infetti.\n")
        print("\033[1mDati simulazione:\nNodi infetti inizialmente:\033[0m ", starting_infected_nodes, "\n\033[1mProbabilità Infezione:\033[0m ", ptrans*100, "% | \033[1mStep Guarigione:\033[0m ", tREC, " | \033[1mStep Immunità:\033[0m ", tSUS)
        if(max_infections==0):
            print("Nessun superspreader: 0 infezioni totali.")
        else:
            print("\033[1mSuperspreaders\033[0m (",max_infections," infezioni ): ",superspreaders, "\n")

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
##input per n° infetti iniziali
while True:
    try:
      n_infected = int(input("Inserire il numero di persone infette inizialmente: "))
      if n_infected > graph.number_of_nodes():
        print("Il valore del numero di infetti non può essere superiore a quello degli utenti.")
        continue
      elif n_infected < 0:
        print("Il valore del numero di infetti non può essere negativo.")
        continue
      break
    except ValueError or TypeError:
        print("Il valore inserito non è un numero intero.")

starting_infected_nodes = random.sample(list(graph.nodes), n_infected)
new_simulation= 'n' #variabile per l'avvio di nuove simulazioni
mod_val = 'n' #variabile per modifica delle variabili iniziali

while True:
    if new_simulation=='n' or mod_val=='y':
        ##input per probabilità di infezione
        while True:
          try:
            ptrans = float(input("Inserire la probabilità (in percentuale) di infezione del proprio vicino: "))
            if ptrans > 100 or ptrans < 0:
              print("La probabilità d'infezione dev'essere compresa tra 0 e 100.")
              continue
            break
          except ValueError or TypeError:
            print("Il valore inserito non è valido.")
        ptrans = ptrans / 100
        ##input step per la guarigione
        while True:
            try:
              tREC = int(input("Inserire il numero di step per la guarigione "))
              if tREC <= 0:
                print("Il numero di step deve essere maggiore di 0.")
                continue
              break
            except ValueError or TypeError:
                print("Il valore inserito non è un numero intero.")
        ##input step per tornare vulnerabili
        while True:
          tSUS_input = input("Inserire il numero di step per diventare nuovamente vulnerabili ('?' per infinito): ")
          if tSUS_input == '?':
              tSUS = float('inf')
              break
          else:
            try:
              tSUS = int(tSUS_input)
              if tSUS <= 0:
                  print("Il numero di step deve essere maggiore di 0.")
              else:
                  break
            except ValueError or TypeError:
                print("Il valore inserito non è un numero intero.")


    ##avvio della simulazione
    simulation = EpidemicSimulation(graph, ptrans, tREC, tSUS, starting_infected_nodes)
    simulation.run_simulation()

    while True:
        new_simulation = input("Vuoi avviare una nuova simulazione con gli stessi stati iniziali dei nodi? y/n ")
        if new_simulation in ['y', 'n']:
            break
        else:
            print("Valore non valido. Inserire 'y' o 'n'.")
    if new_simulation == 'y':
        while True:
          mod_val = input("Vuoi modificare i valori delle variabili? y/n ")
          if mod_val in ['y', 'n']:
            break
          else:
            print("Valore non valido. Inserire 'y' o 'n'.")
    else:
        break