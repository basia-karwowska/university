import matplotlib.pyplot as plt

class Node():
    def __init__(self, key, val=None, parent=None, left=None, right=None):
        self.key=key #identifier of a node
        #3 pointers to other nodes (with which our node is connected through branches in an appropriate way)
        self.parent=parent
        self.left=left
        self.right=right
        self.value=val #we could want to return value instead of the key
        #so it works like a dictionary, now it is easy to get value associated
        #with the largest key, on this tree structure priority queues may be useful
        
    def __repr__(self):
        s="Node(key={}".format(self.key)
        if self.parent is not None:
            s+=" parent={}".format(self.parent.key)
        if self.left is not None:
            s+=" left={}".format(self.left.key)
        if self.right is not None:
            s+=" right={}".format(self.right.key)
        return s+")"

#cost of this operation or what node will be inserted, at which level will the node
#show up, we need to know how conceptually insertion etc. works
#use display function and see what happens in general
  
class BST():
    def __init__(self):
        self.root=None
        self.size=0
    def __repr__(self):
        s="BST tree with {} nodes".format(self.size)
        return s
    def insert(self, node):
        if not isinstance(node, Node):
            raise Exception("Only Nodes can be added to BST!")
        x=self.root
        p=None #parent
        #iterate until we find an empty spot
        while x is not None:
            p=x
            if node.key<p.key:
                #descent on the left
                x=p.left #descending, not creating any node but moving, x
            if node.key>p.key:
                #descent on the right
                x=p.right
            if node.key==p.key:
                raise Exception("We cannot add two nodes with the same key!")
        #p now is a correct parent for x
        #if we did not have any nodes in the tree, we want to insert our node as the root
        if p is None:
            self.root=node #first node we add is the root
        #NONE TYPE HAS NO ATTRIBUTE KEY - IF WE DO NOT DO ELIF AFTER "if p is None"
        elif node.key<p.key:
            #set node as left child of p, we need to perform two operations, child of parent and parent of child
            #connect in both directions
            node.parent=p
            p.left=node
        elif node.key>p.key:
            node.parent=p
            p.right=node
        self.size+=1
        return node #now we know where the node was put inside of the tree
#in the procedure we need to keep track of what is a correct parent
    def display(self, reset=True, color="blue"): #import matplotlib
        if reset: plt.clf() #we want to be able to clf but not in all cases
        #sometimes we want to plot figures at the top of each other
        layer=0 #we initialize and assume layers go down from 0 to -1, -2,...
        prev_nodes=[self.root] #we initialize prev_nodes, first node is root
        next_nodes=[]
        #we want to iterate this process until the list of prev_nodes is not empty
        #by construction we started with list prev_nodes with length equal to 1
        while len(prev_nodes)>0:
            for node in prev_nodes:
                #if our node has left and/or right child, we append to list of
                #nodes in the next layer, next_nodes, these nodes
                if node.left is not None:
                    next_nodes.append(node.left)
                    plt.plot([node.key, node.left.key], [layer, layer-1], "-o", color="blue")
                if node.right is not None:
                    next_nodes.append(node.right)
                    plt.plot([node.key, node.right.key], [layer, layer-1], "-o", color="blue")
            prev_nodes=next_nodes
            next_nodes=[] #we are reinitializing next_nodes
            layer-=1
        return None
    
    def tree_search(self, key):
        x=self.root 
        while (x is not None) and (x.key!=key):
            if x.key<key:
                x=x.right #we move x down to the right
            elif x.key>key:
                x=x.left #we will look for x in the left sub-tree
        return x #x will be the node we look for if it is x.key or will be None
    #regardless, we need to return x
    
    #it queries nodes and returns a node with a specified key, it returns the node
    def __getitem__(self, key): #if the node is contained, it should return the node
        node=self.tree_search(key) 
        if node is None:
            raise Exception("key not found in this BST")
        return node
                
        #first check is None, another is x.key is key because
        #None has no key attribute so None.key would produce error
        #we keep going down until we find that there is a node with some key
        #or not
        
        #maximum key contained in the subtree rooting from a certain node
    def max_subtree(self, node): #we put main, global root if we want to get maximum
    #of the entire tree, node=root then
    #WE ARE LOOKING FOR THE MAXIMUM IN THE SUBTREE ROOTED IN NODE
        x=node
        while (x is not None) and (x.right is not None): #we want to make sure
        #that both x is not None and right child so we proceed to the right and eventually
        #reach the point where x.right is None while x is not yet None
        #and at this point the while loop breaks and we return x
            x=x.right
        return x
        #due to contruction of the trees, it takes logarithmic number of steps
        #we just go to the right as the entries to the right of the root are greater
        #and to the left are smaller so the rightmost entry has the greatest key
        
    def max(self): #for method we can use the keyword, it does not interfere
    #we would not want to overwrite the function though but as a method there
    #is no ambiguity
        return self.max_subtree(self.root)
    
    def min_subtree(self, node, args_check=True):
        if args_check:
            if not isinstance(node, Node):
                raise Exception("need to pass a node")
            #is the node in the tree
        x=node
        while (x is not None) and (x.left is not None):
            x=x.left
        return x
    
    def min(self): #global min, we could equivalently compute it using
    #min_subtree and passing root as the node in the arguments
    #but we want to have an additional method to compute global
    #without the need to pass any arguments as it is obvious
    
    
        return self.min_subtree(self.root) 
    
    def inorder_print(self, node):
        
        #we defined get_item so we can get a reference to a particular node
        #in order to input it into the function
        
        #node is the root of its subtree
        #we assume that the node is contained in the tree
        
        #print whatever is on the left
        if node.left is not None:
            self.inorder_print(node.left) #we call the method on the same node
            
        #print node
        print(node)
        #a lot of frames depending on the number of levels in the tree
        
        #print what is on the right
        if node.right is not None:
            self.inorder_print(node.right)
        pass
            
    #we could use iterator but for now we will just define the function
    #which prints the nodes in the given order
    
#self balancing binary search trees, we want to avoid the case of unbalanced trees
#RECURSIVE PROCEDURE FOR INORDER TRAVERSAL: first we print on the left,
#then root, then right node, it is recursive

#next greater node
    def successor(self, node):
        #node is the root of its subtree
        #we assume that the node is contained in the tree
        ## !!! CASE 1: node has a right child
        if node.right is not None: #right subtree of a node contains nodes with
        #all keys bigger than the key of the parent
            return self.min_subtree(node.right)
        
        
        ## !!! CASE 2: node does not have a right child
        x=node
        p=x.parent
        while (p is not None) and  (x==p.right): #we keep iterating while x is the right child of parent
        #we are looking for the first greater node
        #we keep iterating until the left-child of p is x
            x=p
            p=p.parent #parent of the left node
            #we are going back
            
        return p
    def predecessor(self, node):
        if node.left is not None:
            return self.max_subtree(node.left)
        
        x=node
        p=x.parent
        while (p is not None) and  (x==p.left):
            x=p
            p=p.parent 
        return p
    
    #transplant, we assume that the new root has
    
    def transplant(self, old, new):
        #old and new are two nodes, old is contained in the bst
        #we will use this function as a utility function to support
        #a method for deleting a node, which user is going to use
        if old==self.root:
            self.root=new
        else:
            if new is not None:
                new.parent=old.parent
            #otherwise we will delete the part of the tree, not replacing the old subtree with a new tree
            if old.parent.right==old:
                #old was a right child of its parent
                old.parent.right=new #we are creating a new connection, replacing the old
            elif old.parent.left==old:
                old.parent.left=new
        #update the number of nodes
        return old #we want to return what we removed as it is the last time
    #we can access it and we may want to store it in some container
    def delete(self, z):
        self.size-=1
        l=z.left
        r=z.right
        #CASE 1: z only has a left sub-tree
        #then we have a guarantee that we will preserve the order, we will replace
        #either left subtree or add to right subtree, depending on the value of l
        #the case of no children at all is also contained in this case
        #as transplant will take care, it allows for possibility of a node being None
        
        if r is None:
            return self.transplant(z, l)
        #CASE 2: z only has a right subtree
        if l is None:
            return self.transplant(z, r)
        
        y=self.successor(z)
        x=y.right
        #r==y "the successor of z is its right child
        if r==y: #CASE 3
            #transplant r in place of z
            #attach l on the left of r
            self.transplant(z, r)
            l.parent=r
            r.left=l
        else: #CASE 4
            self.transplant(y, x)
            r.parent=y
            y.right=r
            self.transplant(z, y)
            l.parent=r
            y.left=l
        return z
        
        
    #connect the left child
    #y.left=l
#we are using the fact that keys are ordered to draw a tree on the coordinate system
bst=BST()
a=[5, 4, 9, 10, 2, 7, 8, 6]
for el in a:
    bst.insert(Node(el))
    
#suffled order - it is useful to use the tree structure then
#we treat depth as y-coordinates and keys as x-coordinates 
#since they are ordered, we can do that, ordering property
'''
a=Node(1)

a
Out[15]: Node(key=1)

b=Node(2)

a.right=b

a
Out[18]: Node(key=1 right=2)

b
Out[19]: Node(key=2)

b.parent=a

b
Out[21]: Node(key=2 parent=1)

c=Node(3)

d=Node(4)

b.left=c

b.right=d

c.parent=b

d.parent=b

a
Out[28]: Node(key=1 right=2)
'''