import math
import random
from array import array

##  NODE CLASS  ##
class Node:
    def __init__(self, position_x, position_y, parent=None):
        self.position = array('f',[position_x,position_y])  # Coordenadas del nodo (x, y)
        self.parent = parent      # Nodo padre (None para la raíz)


##  RRT CLASS  ##
class RRTPatchSearch:
    def __init__(self, my_map, tile_size, width, height, distance_at_node, max_iterations=200):
        self.map = my_map
        self.distance_at_node = distance_at_node
        self.max_iterations = max_iterations  # Número máximo de iteraciones para generar nodos
        self.tree = []

        ## Dimensiones del entorno
        self.tile_size = tile_size
        self.width = width
        self.height = height

    def is_in_collision(self, x, y):
        # Verifica si el punto (x, y) está dentro de un obstáculo
        for obstacle in self.map.obstacles_coordinates:
            if (int(x), int(y)) == (int(obstacle[0]), int(obstacle[1])):
                return True
            

            # for i in range(2):
            #     for j in range(2):
            #         if (int(x)+i, int(y)+j) == (int(obstacle[0]), int(obstacle[1])):
            #             return True 
            # for i in range(2):
            #     for j in range(2):
            #         if (int(x)-i, int(y)-j) == (int(obstacle[0]), int(obstacle[1])): 
            #             return True           

            if (int(x), int(y)) == (int(obstacle[0])+10 , int(obstacle[1]) +10):
                return True
            if (int(x), int(y)) == (int(obstacle[0])+10 , int(obstacle[1]) -10):
                return True
            if (int(x), int(y)) == (int(obstacle[0])-10 , int(obstacle[1]) +10):
                return True
            if (int(x), int(y)) == (int(obstacle[0])-10 , int(obstacle[1]) -10):
                return True
        return False

    def generate_random_node(self):
        # Genera un nodo aleatorio dentro de los límites del mapa
        x = random.randint(0, self.width // self.tile_size - 1)
        y = random.randint(0, self.height // self.tile_size - 1)
        return x, y

    def find_nearest_node(self, tree, random_node):
        # Encuentra el nodo más cercano en el árbol al nodo aleatorio
        nearest_node = tree[0]
        min_dist = float('inf')
        for node in tree:
            dist = math.sqrt((node.position[0] - random_node[0]) ** 2 + (node.position[1] - random_node[1]) ** 2)
            if dist < min_dist:
                min_dist = dist
                nearest_node = node
        return nearest_node

    def steer(self, from_node, to_node):
        # "Dirige" el nodo más cercano hacia el nodo aleatorio, creando un nuevo nodo
        direction = [to_node[0] - from_node.position[0], to_node[1] - from_node.position[1]]
        distance = math.sqrt(direction[0] ** 2 + direction[1] ** 2)
        try:
            direction = [direction[0] / distance, direction[1] / distance]
        except: 
            direction = [direction[0] / 0.00000001, direction[1] / 0.00000001]
        new_position = [
            from_node.position[0] + direction[0] * self.distance_at_node,
            from_node.position[1] + direction[1] * self.distance_at_node
        ]
        return Node(new_position[0],new_position[1], parent=from_node)

    def filter_path_to_destiny(self, tree, destiny):
        """
        Filtra las ramas que no llevan al destino en el árbol generado.
        """
        def find_nearest_node_to_goal(nodes, goal):
            nearest_node = None
            min_distance = float('inf')
            for node in nodes:
                distance = math.sqrt((node.position[0] - goal[0]) ** 2 + (node.position[1] - goal[1]) ** 2)
                if distance < min_distance:
                    min_distance = distance
                    nearest_node = node
            return nearest_node

        def retrieve_path(node):
            current_node = node
            filtered_path = []
            while current_node is not None:
                filtered_path.append([int(current_node.position[0]), int(current_node.position[1])])
                current_node = current_node.parent
            filtered_path.reverse()  # Invertir el camino para ir desde el inicio al destino
            return filtered_path

        # Encuentra el nodo más cercano al destino en el árbol
        nearest_node_to_goal = find_nearest_node_to_goal(tree, destiny)

        # Recuperar solo el camino que lleva al destino
        filtered_path = retrieve_path(nearest_node_to_goal)

        return filtered_path

    def genere_patch(self,xi , yi, goal):
        del self.tree
        self.tree = [Node(xi, yi)]  # Inicializa el árbol con la posición actual del bot

        for _ in range(self.max_iterations):
            random_node = self.generate_random_node()

            nearest_node = self.find_nearest_node(self.tree, random_node)
            new_node = self.steer(nearest_node, random_node)

            #if not self.is_in_collision(int(new_node.position[0]), int(new_node.position[1])):
            if True:
                self.tree.append(new_node)

                # Si el nuevo nodo está lo suficientemente cerca del objetivo, termina
                if math.sqrt((new_node.position[0] - goal[0]) ** 2 + (new_node.position[1] - goal[1]) ** 2) < 5:
                    self.tree.append(Node(goal[0],goal[1], parent=new_node))
                    break
            del new_node

        # Filtrar el camino que lleva al destino
        self.tree = self.filter_path_to_destiny(self.tree, goal)

        return self.tree

