# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 23:21:03 2020

@author: Kristin Geßler
"""

from typing import Union # for defining Union types
import random 
import sys 
import os # OS module in python provides functions for interacting with the operating system


###############################################################################

#instead of working with strings, assign numbers to the colors and directions
black = 0
red = 1

left = 0
right = 1

class Node:
    """ 
    This is a class whose instances will be the nodes of a red black tree. 
      
    Attributes: 
        key (float): The key/value which is associated to a node.
        parent (Node, None): The parent node, i.e. the node a stage above the actual node on which the actual node hangs directly. 
        left (Node, None): The left child node, i.e. the node a stage below the actual node on the left side.
        right (Node, None): The right child node, i.e. the node a stage below the actual node on the right side.
        color (int): The color (red/black) that is associated to a node, where 0 is assigned to black nodes and 1 to red nodes respectively.
    """
    
    
    
    def __init__(self, key:float, color:int = red):
        """ 
        The constructor for Nodes. 
  
        Parameters: 
           key (float): The key/value which is associated to a node.
           color (int): The color (red/black) that is associated to a node (red by default), where 0 is assigned to black nodes and 1 to red nodes respectively.  
        """
        try:
            float(key)
        except ValueError:
            print("That was no possible value for a key in this context!")
            
        if (color is not red) and (color is not black):
            raise ValueError("That was no possible value for a color in this context!")
            
        self.key = key
        self.parent = None  
        self.left = None    
        self.right = None   
        self.color = color
    
    
    
    def __str__(self):
        return "Node("+str(self.key)+")"

###############################################################################
        
class RedBlackTree:
    """ 
    This is a class for operations on a red black tree.
      
    Attribute: 
        root (Node, None): The root node, i.e. the initial node of the tree.
    """
    
    
    def __init__(self):
        """ The constructor for RedBlackTrees. """
        self.root = None    
        
    ###########################################################################    
    # help functions to access the different nodes in a red-black-tree
    # n is an instance of the class Node
    def get_parent(self, n:Node) -> Union[Node,None]:
        """ 
        The function accesses the parent node of the input node. 
  
        Parameter: 
            n (Node): The node whose parent is searched. 
          
        Returns: 
            Node/None: The parent node of n. 
        """
        # the parent of the root-Node is None
        if n is self.root:
            return None
        return n.parent
    
    
    
    def get_grand_parent(self, n:Node) -> Union[Node,None]:
        """ 
        The function accesses the grandparent node of the input node. 
  
        Parameter: 
            n (Node): The node whose grandparent is searched. 
          
        Returns: 
            Node/None: The grandparent node of n. 
        """
        # the grandparent of the root-Node or the children of the root-Node is None
        if (n is self.root) or (n.parent is self.root):
            return None
        return (n.parent).parent
    
    
    
    def get_sibling(self, n:Node) -> Union[Node,None]:
        """ 
        The function accesses the sibling node of the input node. 
  
        Parameter: 
            n (Node): The node whose sibling is searched. 
          
        Returns: 
            Node/None: The sibling node of n. 
        """
        p = self.get_parent(n)
        # if the parent is None, one does not have any siblings
        if p is None:
            return None
        
        # if n is a left child, return the right child 
        if n is p.left:
            return p.right
        # if n is a right child, return the left child
        else:
            return p.left
        
        
        
    def get_uncle(self, n:Node) -> Union[Node,None]:
        """ 
        The function accesses the uncle/aunt node of the input node. 
  
        Parameter: 
            n (Node): The node whose uncle/aunt is searched. 
          
        Returns: 
            Node/None: The uncle/aunt node of n. 
        """
        p = self.get_parent(n)
        # uncle is None if n does not have a parent
        if p is None:
            return None
        return self.get_sibling(p)
    
    ###########################################################################
    # help function for defining the left and right rotation in a single function
    # changes the parts of the left rotation to the corresponding parts of the right rotation if required
    # i.e.: x.right becomes x.left and vice versa
    
    def _left(self, n:Node, direction:int = left) -> Union[Node,None]: 
        if direction is right:
            return n.right
        return n.left
    
    
    
    def _right(self, n:Node, direction:int = left) -> Union[Node,None]: 
        if direction is right:
            return n.left
        return n.right
    
    
    
    # Rotations: the lables X and Y refer to the following figure (the left rotation around X)
    #                   |                               |
    #                   X                               Y
    #                 /   \                           /   \ 
    #                /     \      rotate left        /     \ 
    #               a       Y     ------------>     X       c      
    #                     /   \                   /   \ 
    #                    /     \                 /     \   
    #                   b       c               a       b
    #
    def rotate_around(self, x:Node, direction:int = left) -> None: 
        """ 
        The function performs a left/right rotation around the input node. 
  
        Parameters: 
            x (Node): The node around which is rotated. 
            direction (int): The direction of the rotation (left by default), where 0 stands for left rotation and 1 for right rotation respectively.
          
        Returns: 
            None
        """
        p = self.get_parent(x)
        # the right child of x (here y) takes x's place
        y = self._right(x, direction)
        
        # since the ends of branches (leafes) are None/empty, we have to ensure that they can not move into the middle of the tree (normally this should be nowhere the case)
        if y is None:
            raise Exception("The rotation is not possible since the ends of the branches are empty")
        
        # NEW SETTINGS FOR X:
        # y.left (here b) becomes the new right child of x;
        # the left child of x (here a) stays the same;
        # y becomes the new parent of x
        if direction is left:
            x.right = y.left
        else:
            x.left = y.right 
        x.parent = y
        
        # NEW SETTINGS FOR Y:
        # x becomes the new left child of y;
        # the right child of y (here c) stays the same;
        # the parent of x becomes the new parent of y
        if direction is left:
            y.left = x
        else:
            y.right = x
        y.parent = p
        
        # RECTIFY THE OTHER RELATIONS:
        # if the new x.right is not None, x becomes its new parent
        if self._right(x, direction) is not None:
            if direction is left:
                x.right.parent = x
            else:
                x.left.parent = x
            
        # if p is None (e.g.: if x was the root-Node), we have already finished
        # if p is not None, rectify the relation of p
        # (is the same procedure for both directions, we do not have to use the help functions)
        if p is not None: 
            if x is p.left:
                p.left = y
            elif x is p.right:
                p.right = y
            
                
        return None
                
    
    ##########################################################################
    # insert a node into the red-black-tree
    def insert_rbt(self, n:Node) -> None:
        """ 
        The function inserts the input node into the red black tree while preserving the red-black-tree-properties. 
  
        Parameter: 
            n (Node): The node which is inserted. 
            
        Returns: 
            None
        """
        # check if n is an instance of the class Node
        if not isinstance(n, Node):
            raise ValueError("You can only insert nodes!")
            
        # insert a new node
        self.insert(n)
        
        # fix the tree if the red-black-tree properties were violated by the insertion
        self.fix(n)
        
        return None
     
    ###########################################################################
    def insert(self, n:Node) -> None: 
        """ 
        The function inserts the input node into a binary tree. 
  
        Parameter: 
            n (Node): The node which is inserted. 
            
        Returns: 
            None
        """
        # check if n is an instance of the class Node
        if not isinstance(n, Node):
            raise ValueError("You can only insert nodes!")
            
        # basic properties of the new node
        n.color = red
        n.right = None
        n.left = None
        
        # the actual insertion
        if self.root is None:
            self.root = n
        else:
            self._insert(n, self.root)
            
        return None
                
            
    
    # search recursively for a spare place       
    def _insert(self, n:Node, node:Node) -> None:
        # search for a spare place in the left subtree of node
        if n.key < node.key: 
            
            # if the left place is free, put n on it
            if node.left is None: 
                node.left = n
                n.parent = node
                return None
            # if not, continue with the search
            else: 
                self._insert(n, node.left)
         
        # search for a spare place in the right subtree of node
        else: 
            # if the right place is free, put n on it
            if node.right is None: 
                node.right = n
                n.parent = node
                return None
            # if not, continue with the search
            else: 
                self._insert(n, node.right)
             
    ###########################################################################            
    def fix(self, n:Node) -> None:
        """ 
        The function ensures that the red-black-tree-properties are preserved by fixing them if reqired. 
  
        Parameter: 
            n (Node): The node from which to start fixing the red-black-tree-properties. 
            
        Returns: 
            None
        """
        # check if n is an instance of the class Node
        if not isinstance(n, Node):
            raise ValueError("You can only insert nodes!")
        
        p = self.get_parent(n)
        
        
        # if n is the root-Node, i.e. n's parent is None 
        # (the root-Node must always be black)
        if p is None:
            n.color = black
            return None
            
        # if the parent-Node of n is black, nothing must be fixed
        if p.color is black:
            return None
        
        
        u = self.get_uncle(n)
        g = self.get_grand_parent(n)
        
        
        # if the parent-Node of n is red and the uncle of n is also red
        # the order of the following conjunction is crucial since leafes(=None) do not have a color
        if (p.color is red) and (u is not None) and (u.color is red):
            
            # color the parent and the uncle black
            p.color = black
            u.color = black
            
            # color the grandparent red
            g.color = red
           
            # continue by fixing the tree recursively (starting from the grandparent)
            self.fix(g)
            return None
        
        # if the parent-Node of n is red and the uncle of n is black;
        # the leafes are always black (therefore we must add "u is None") (*)
        if (p.color is red) and ((u is None) or (u.color is black)):# the order is crucial
            # case_1 passes automatically on to case_2
            self._case_1(n)  
            
        else: 
            raise Exception("Something went wrong in fix!")
    
    
    
    # Case 1 of (*):  the red parent and the red child are NOT in a row            
    def _case_1(self, n:Node) -> None:
        
        p = self.get_parent(n)
        g = self.get_grand_parent(n)

        # case a) 
        if (n is p.right) and (g is not None) and (p is g.left):
            self.rotate_around(p, left)
            # continue fixing the tree by starting from the left child of n
            n = n.left  
            
        # case b) 
        elif (n is p.left) and (g is not None) and (p is g.right):
            self.rotate_around(p, right)
            # continue fixing the tree by starting from the right child of n
            n = n.right 
        
        # now we are in case_2
        return self._case_2(n)
        
    
    
    # Case 2 of (*):  the red parent and the red child are in a row      
    def _case_2(self, n:Node) -> None:
        
        p = self.get_parent(n)
        g = self.get_grand_parent(n)
       
        
        # case a)
        if (n is p.left) and (g is not None) and (p is g.left):
            self.rotate_around(g, right)
            
            # after the rotation update the (new) root (could have changed!)
            root = n
            while (self.get_parent(root) is not None):
                root = self.get_parent(root)
            self.root = root
                
            
        # case b)
        elif (n is p.right) and (g is not None) and (p is g.right):
            self.rotate_around(g, left)
            
            # after the rotation update the (new) root (could have changed!)
            root = n
            while (self.get_parent(root) is not None):
                root = self.get_parent(root)
            self.root = root
            
            
        else: 
            raise Exception("Something went wrong in case_2!")
            
        # color changes:
        # the parent becomes black
        p.color = black
        # the grandparent becomes red
        g.color = red
        
        return None
                                      
    ###########################################################################
    def inorder(self) -> list:
        """ The function returns the keys of the nodes inserted in the tree in increasing order. """
        # stores the keys of the nodes inserted in the tree in increasing order
        ordered = []
        
        def _node_inorder(n:Node) -> None: 
            if n is not None:
                _node_inorder(n.left)
                ordered.append(n.key)
                _node_inorder(n.right)
                
        _node_inorder(self.root)
        return ordered
        
            
    def minimum(self) -> Node:
        """ The function returns a node whose key is smaller or equal than the others. """
        x = self.root
        while x.left is not None:
            x = x.left
        return x
        
    
    def maximum(self) -> Node:
        """ The function returns a node whose key is bigger or equal than the others. """
        x = self.root
        while x.right is not None:
            x = x.right
        return x
    
        
###############################################################################
        
    # function to draw the tree in a Tex-file
    def draw_tex(self, output=sys.stdout):
        """ 
        The function draws the red black tree with inserted nodes into a tex-file. 
  
        Parameter: 
            output: The place/ writeable file where to draw the tree into (sys.stdout by default).
            
        Returns: 
            None
        """
        # r"..." : the string (...) is treated as a raw string, i.e. the \... won't be interpreted as commands
        # """...""" (triple-quoted string): unescaped newlines and quotes are allowed (and are retained),
        # except that three unescaped quotes in a row terminate the string.
        # (A ``quote'' is the character used to open the string, i.e. either ' or ".)
        print(r""" 
        \documentclass{article}
        
        \usepackage[landscape,left=1cm,right=1cm,bottom=1cm,top=2cm]{geometry}
        \usepackage{tikz}
        \usepackage{tikz-qtree}
        
        %\parindent=0pt
        %\parskip=0pt
        
        \begin{document}
        \centering
        \begin{tikzpicture}[scale=1,]
        \tikzset{every tree node/.style={, circle, draw=black}}
        \tikzset{every leaf node/.style={fill=black}}
        \Tree""", file=output) # writes the tex-code in output
        
        def _color_nodes(node):
            if node.color is red:
                return "\color{red}"
            return "\color{black}"
        
        def _draw_nodes(node, out):
            if node is not None:
                # the syntax for generating a tree in Tex with the package tikz-qtree:
                # - subtrees are delimited by square brackets
                # - a subtree’s root label is joined by a dot (.) to its opening bracket
                # - spaces are required after every (internal or leaf) node label
                print(r"[.{" + _color_nodes(node) + str(node.key) + r"} ", file=out)
                _draw_nodes(node.left, out)
                _draw_nodes(node.right, out)
                print(r" ]", file=out)
            else:
                print(r" { } ", file=out)
                
        _draw_nodes(self.root, output)
        
        print(r""";
        \end{tikzpicture}
        \end{document}
        """, file=output)
        
        return None
        
###############################################################################

if __name__ == '__main__':
    
    # create the trees
    bt = RedBlackTree() # should represent a binary tree (to show the difference between a binary tree and a red black tree)
    rbt = RedBlackTree()
    rbt_test = RedBlackTree()
    rbt_random = RedBlackTree()
     
    
    
    # insert nodes
    for i in range(1,11):
        rbt.insert_rbt(Node(i))
        bt.insert(Node(i))
        
        
    test_list = [17,193,47,189,102,127,97,198,54,73,115]
    for i in test_list:
        rbt_test.insert_rbt(Node(i))
           
    random_list = []
    for x in range(50):
        i = random.randint(1,200)
        random_list.append(i)
        rbt_random.insert_rbt(Node(i))
    
    print("Random list:",random_list)
        
    
    
    
    # test the other functions
    # inorder
    print()
    print("The random list ordered:", rbt_random.inorder())
    # minimum
    print()
    print("The minimum of the random list:", rbt_random.minimum())
    # maximum
    print()
    print("The maximum of the random list:", rbt_random.maximum())
    
    
    
    
    
    # produce the tex-files
    bt.draw_tex(open("bt.tex", "w"))
    os.system("pdflatex bt.tex")
    rbt.draw_tex(open("rbt.tex", "w"))
    os.system("pdflatex rbt.tex")# executes the command in a subshell
        
    rbt_test.draw_tex(open("rbt_test.tex", "w"))
    os.system("pdflatex rbt_test.tex")
    
    rbt_random.draw_tex(open("rbt_random.tex", "w"))
    os.system("pdflatex rbt_random.tex")




