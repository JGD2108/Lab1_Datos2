import sqlite3
import bisect
class BPlusTreeNode:
    def __init__(self, order, is_leaf):
        self.order = order
        self.is_leaf = is_leaf
        self.keys = []
        self.values = []
        self.children = []

class BPlusTreeNode:
    def __init__(self, order, is_leaf):
        self.order = order
        self.is_leaf = is_leaf
        self.keys = []
        self.value1 = []
        self.value2 = []
        self.children = []

class BPlusTree:
    def __init__(self, order):
        self.order = order
        self.root = BPlusTreeNode(order, True)

    def insert(self, key, value1, value2):
        #Encontrar la hoja donde el key debe ser insertado
        node = self._find_leaf_node(key)

       #Insertar el key y sus valores en el nodo hoja encontrado
        self._insert_into_leaf(node, key, value1, value2)

        # Si el nodo hoja esta sobrecargado, debemos hacerle un split
        if len(node.keys) == self.order:
            self._split_leaf_node(node)

    def _find_leaf_node(self, key):
        # Traverse the tree to find the leaf node where the key should be inserted
        node = self.root
        while not node.is_leaf:
            i = bisect.bisect_right(node.keys, key) - 1 # sirve para insertar un elemento en una lista ordenada, pero manteniendo ese orden después de la inserción
            node = node.children[i]
        return node

    def _insert_into_leaf(self, node, key, value1, value2):
        # Insert the key and values into the leaf node
        i = bisect.bisect_left(node.keys, key)
        node.keys.insert(i, key)
        node.value1.insert(i, value1)
        node.value2.insert(i, value2)

    def _split_leaf_node(self, node):
        """
        El método primero determina el índice de división como el punto 
        medio de la lista de claves en el nodo. A continuación, crea un 
        nuevo nodo de hoja con el mismo orden que el nodo original y 
        establece sus atributos de keys, value y value2 en la segunda 
        mitad de los atributos correspondientes del nodo original. 
        Finalmente, las claves del nodo original, los atributos value1 y value2 
        se actualizan para incluir solo la primera mitad de sus atributos correspondientes.
        Si el nodo que se divide es la raíz, se crea una nueva raíz y se agregan los nodos 
        original y nuevo como hijos de la raíz. De lo contrario, se busca el nodo padre del 
        nodo original y se inserta el nuevo nodo en la posición correcta en la lista de hijos 
        del padre y se actualiza la lista de claves del padre en consecuencia.
        """
        split_index = len(node.keys) // 2
        new_node = BPlusTreeNode(self.order, True)
        new_node.keys = node.keys[split_index:]
        new_node.value1 = node.value1[split_index:]
        new_node.value2 = node.value2[split_index:]
        node.keys = node.keys[:split_index]
        node.value1 = node.value1[:split_index]
        node.value2 = node.value2[:split_index]

        # Update parent node with new child
        if node == self.root:
            # If the root node was split, create a new root
            self.root = BPlusTreeNode(self.order, False)
            self.root.keys.append(new_node.keys[0])
            self.root.children = [node, new_node]
        else:
            parent = self._find_parent_node(node)
            i = bisect.bisect_left(parent.keys, node.keys[-1])
            parent.keys.insert(i, new_node.keys[0])
            parent.children.insert(i+1, new_node)

    def _find_parent_node(self, node):
        """
        El método comienza definiendo el nodo raíz como el nodo padre. 
        Luego, entra en un bucle while que recorre el árbol buscando el 
        padre del nodo dado. Primero, se verifica si el primer hijo del 
        nodo padre es igual al nodo dado. Si es así, se devuelve el nodo padre.
        Si el primer hijo del nodo padre no es igual al nodo dado, el método 
        recorre la lista de hijos restantes del nodo padre utilizando un bucle for. 
        Para cada hijo restante, el método compara la clave del nodo dado 
        con la clave del hijo actual. Si la clave del nodo dado es menor que la c
        lave del hijo actual, el método actualiza el nodo padre a ser el hijo 
        actual y se rompe el bucle for. Si el hijo actual es igual al nodo dado, 
        el método devuelve el nodo padre. Si el método llega al final de la lista 
        de hijos del nodo padre sin encontrar el nodo dado, el bucle while continuará 
        buscando el padre en el siguiente nivel del árbol.
        """
        # Traverse the tree to find the parent node of the given node
        parent = self.root
        while True:
            if parent.children[0] == node:
                return parent
            for i, child in enumerate(parent.children[1:], start=1):
                if child == node:
                    return parent
                elif node.keys[0] < child.keys[0]:
                    parent = child
                    break
    def find_node(self, key):
        # Find the leaf node that contains the key
        node = self._find_leaf_node(key)

        # Search for the key in the leaf node
        i = bisect.bisect_left(node.keys, key)
        while i < len(node.keys) and node.keys[i] == key:
            print(f"Placa: {key}, Nombre: {node.value1[i]}, Cedula: {node.value2[i]}") # imporime info del nodo
            i += 1

    def _find_leaf_node(self, key):
        # Traverse the tree to find the leaf node that contains the key
        node = self.root
        while not node.is_leaf:
            i = bisect.bisect_right(node.keys, key) - 1
            node = node.children[i]
        return node

    def print_tree(self):
        self._print_node(self.root)

    def _print_node(self, node, level=0):
        indent = "  " * level
        if node.is_leaf:
            print(f"{indent}- {node.keys} -{ node.value1} - {node.value2}")
        else:
            print(f"{indent}* {node.keys}-{ node.value1} - {node.value2}")
            for child in node.children:
                self._print_node(child, level+1)

        
if __name__ == '__main__':
# Open SQLite database and execute query
    conn = sqlite3.connect('Rtramite.db')
    c = conn.cursor()
    c.execute('SELECT placa, nombre, cc FROM mytable')

    # Create new B+ tree
    tree = BPlusTree(order=4)

    # Insert data into B+ tree
    for row in c.fetchall():
        """
        En esta implementación la clase del arbol debe incluye una lista de valores para
        la segunda y tercera columna de nuestra bases de datos
        """
        key = row[0]
        value1 = row[1]
        value2 = row[2]
        tree.insert(key, value1, value2)

    # Close SQLite database connection
    conn.close()
    tree.print_tree()
    tree.find_node("EMT219")
