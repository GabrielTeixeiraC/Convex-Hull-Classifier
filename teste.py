class Node():
    def __init__(self, key, parent=None) -> None:
        self.parent = parent
        self.left = None
        self.right = None
        self.height = 1
        self.key = key
    
    def findHeight(self, node):
        if node == None: return 0
        return node.height
    
    def balanceFactor(node):
        if node == None: return 0
        
        return node.findHeight(node.right) - node.findHeight(node.left)

class AVLTree():
    def __init__(self):
        self.root = None

    def findYZ(self, node):
        Y = node.right if node.findHeight(node.right) >= node.findHeight(node.left) else node.left
        Z = Y.right if node.findHeight(Y.right) >= node.findHeight(Y.left) else Y.left
        return Y, Z

    def checkAndBalance(self, node):
         # Atualizar balanceamentos
        auxNodeBalancing = node
        while auxNodeBalancing != None:
            balanceFactor = auxNodeBalancing.balanceFactor()
            if balanceFactor < -1:  # Unbalanced to the left
                Y, Z = self.findYZ(auxNodeBalancing)
                # Caso 3
                if Z.key > Y.key:
                    self.leftRotate(Z)
                    self.rightRotate(Z)

                # Caso 1
                else: 
                    self.rightRotate(Y)
                
                self.root.height = 1 + max(self.root.findHeight(self.root.left), self.root.findHeight(self.root.right))  # Verificar
            elif balanceFactor > 1:  # Unbalanced to the right
                Y, Z = self.findYZ(auxNodeBalancing)
                # Caso 4
                if Z.key < Y.key:
                    self.rightRotate(Z)
                    self.leftRotate(Z)
                else:  # Caso 2
                    self.leftRotate(Y)
                self.root.height = 1 + max(self.root.findHeight(self.root.left), self.root.findHeight(self.root.right))  # Verificar
                    
            auxNodeBalancing = auxNodeBalancing.parent

    def preBalanceInsertion(self, key):
        parentNode = self.root
        while parentNode != None:
            if key < parentNode.key:
                if parentNode.left == None:
                    parentNode.left = Node(key, parentNode)
                    return parentNode.left
                parentNode = parentNode.left
            else:
                if parentNode.right == None:
                    parentNode.right = Node(key, parentNode)
                    return parentNode.right
                parentNode = parentNode.right

    def exchangeForPredecessor(self, node):
        currentNode = node.left
        while currentNode != None:
            if currentNode.right != None:
                currentNode = currentNode.right
            else:
                self.removeNode(currentNode.key)
                return currentNode.key

    def findPredecessor(self, key):
        currentNode = self.root

        while currentNode != None:
            if key < currentNode.key:
                currentNode = currentNode.left
            elif key > currentNode.key:
                currentNode = currentNode.right
            else:
                auxNode = currentNode
                while auxNode != None:
                    if auxNode.right != None:
                        auxNode = auxNode.right
                    else:
                        return auxNode.key
                return None

    def findSuccessor(self, key):
        currentNode = self.root

        while currentNode != None:
            if key < currentNode.key:
                currentNode = currentNode.left
            elif key > currentNode.key:
                currentNode = currentNode.right
            else:
                auxNode = currentNode
                while auxNode != None:
                    if auxNode.left != None:
                        auxNode = auxNode.left
                    else:
                        return auxNode.key
                return None

    def findKeyToBeRemoved(self, key):
        currentNode = self.root
        if key == self.root.key:
            if self.root.left == None and self.root.right == None:
                self.root = None
                return
            elif currentNode.left == None and currentNode.right != None:
                self.root = currentNode.right
                self.root.parent = None
                return
            elif currentNode.left != None and currentNode.right == None:
                self.root = currentNode.left
                self.root.parent = None
                return

        while currentNode != None:
            if key < currentNode.key:
                currentNode = currentNode.left
            elif key > currentNode.key:
                currentNode = currentNode.right
            else:
                if currentNode.left == None and currentNode.right == None:  # Leaf Node
                    auxNode = currentNode
                    if currentNode.key > currentNode.parent.key:
                        currentNode.parent.right = None
                        self.decreaseHeights(auxNode)
                        self.checkAndBalance(auxNode)
                        
                    else:
                        currentNode.parent.left = None
                        self.decreaseHeights(auxNode)
                        self.checkAndBalance(auxNode)

                elif currentNode.left == None and currentNode.right != None:  # Node only has a right child
                    if currentNode.key < currentNode.parent.key:
                        currentNode.parent.left = currentNode.right
                    else:
                        currentNode.parent.right = currentNode.right
                    currentNode.right.parent = currentNode.parent
                    self.decreaseHeights(currentNode.right)
                    self.checkAndBalance(currentNode.right)  # Testar para remover 1 na árvore
                elif currentNode.left != None and currentNode.right == None:  # Node only has a left child
                    if currentNode.key < currentNode.parent.key:
                        currentNode.parent.left = currentNode.left
                    else:
                        currentNode.parent.right = currentNode.left
                    currentNode.left.parent = currentNode.parent
                    self.decreaseHeights(currentNode.left)
                    self.checkAndBalance(currentNode.left)
                    
                else:  # Node has two children
                     currentNode.key = self.exchangeForPredecessor(currentNode)
                    # troca o nó a ser removido com a folha correspondente (seu antecessor) e chama a função novamente a partir da raiz
                currentNode = None                     
        # TODO caso em que o nó não foi encontrado

    def leftRotate(self, node):
        if node.left != None:
            node.left.parent = node.parent
            
        node.parent.right = node.left
        node.left = node.parent

        if node.parent != self.root:
            if node.parent.key < node.parent.parent.key:
                node.parent.parent.left = node
            else:
                node.parent.parent.right  = node
        else:
            self.root = node

        aux = node.parent
        node.parent = node.parent.parent
        aux.parent = node

        aux.height = 1 + max(aux.findHeight(aux.left), aux.findHeight(aux.right))
        node.height = 1 + max(node.findHeight(node.left), node.findHeight(node.right))

    def rightRotate(self, node):
        if node.right != None:
            node.right.parent = node.parent

        node.parent.left = node.right
        node.right = node.parent

        if node.parent != self.root:
            if node.parent.key < node.parent.parent.key:
                node.parent.parent.left = node
            else:
                node.parent.parent.right  = node
        else:
            self.root = node

        aux = node.parent
        node.parent = node.parent.parent
        aux.parent = node

        aux.height = 1 + max(aux.findHeight(aux.left), aux.findHeight(aux.right))
        node.height = 1 + max(node.findHeight(node.left), node.findHeight(node.right))

    def increaseHeights(self, node):
        auxNodeHeight = node
        while auxNodeHeight.parent != None and auxNodeHeight.parent.height == auxNodeHeight.height:
            auxNodeHeight.parent.height += 1
            auxNodeHeight = auxNodeHeight.parent
    
    def decreaseHeights(self, node):
        auxNodeHeight = node
        while auxNodeHeight != None :
            auxNodeHeight.height = 1 + max(auxNodeHeight.findHeight(auxNodeHeight.left), auxNodeHeight.findHeight(auxNodeHeight.right))
            auxNodeHeight = auxNodeHeight.parent

    def insertNode(self, key):
        if self.root == None:
            self.root = Node(key)
        
        else:
            newNode = self.preBalanceInsertion(key)
            self.increaseHeights(newNode)
            
            # Update Balance
            self.checkAndBalance(newNode)

    def removeNode(self, key):
        self.findKeyToBeRemoved(key)


arvore = AVLTree()
"""
arvore.insertNode(3)
arvore.removeNode(3)  # Teste para árvore com apenas um nó
arvore.insertNode(3)
arvore.insertNode(1)
arvore.insertNode(7)
arvore.insertNode(0)
arvore.insertNode(2)
arvore.insertNode(5)
arvore.insertNode(9)
arvore.insertNode(8)
arvore.insertNode(6)
arvore.insertNode(4)
#arvore.removeNode(7)  # Teste para caso em que o nó tem 2 filhos

arvore.insertNode(12)  # Teste para rotação da raiz na inserção, testar adiconando 13 e 14
arvore.insertNode(13)
#arvore.removeNode(7)
#arvore.removeNode(9)
#arvore.removeNode(2)  # Teste para rotação da raiz na remoção (remover 2 acima)
#arvore.removeNode(6)  # Teste para remoção de nó folha
#arvore.removeNode(9)
#arvore.removeNode(8)  # Teste para node só tem filho à direita

arvore.insertNode(6)
arvore.insertNode(3)
arvore.insertNode(9)
arvore.insertNode(8)

arvore.removeNode(6)
"""

arvore.insertNode(3)
arvore.insertNode(1)
arvore.insertNode(7)
arvore.insertNode(2)
arvore.insertNode(5)
arvore.insertNode(8)
arvore.insertNode(6)
arvore.insertNode(4)
arvore.removeNode(3)
#arvore.removeNode(2)
#arvore.removeNode(7)

print()