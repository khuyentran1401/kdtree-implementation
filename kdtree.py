import math
import numpy as np

class kdTree_node:
    
    def __init__(self, x, y, split_along_x=True):
        self.x = x
        self.y = y
        self.xmax = math.inf
        self.ymax = math.inf
        self.xmin = -math.inf
        self.ymin = -math.inf
        self.split_along_x = split_along_x
        self.left = None
        self.right = None
        
    def __str__(self):
        return "(x="+str(self.x)+",y="+str(self.y)+")"



class kdTree:
    def __init__(self, xs, ys):
        
        i_x_sort = np.argsort(xs)
        i_y_sort = np.argsort(ys)
        self.root = self.__buildTree(xs, ys, i_x_sort, i_y_sort, True)
        
    def print(self):
        self.__printSubtree(self.root)
        
    def __printSubtree(self, node):
        if node.left!=None:
            self.__printSubtree(node.left)
        print(node)
        if node.right!=None:
            self.__printSubtree(node.right)
    
    def __select(self, isorted, isecond):
        iy = np.array([]).astype(int)
        for i in isecond:
            r = (isorted==i)
            if r.any()==True:
                iy=np.append(iy,i)
        return iy
    
    def __buildTree(self, xs, ys, ix, iy, splitx=None, father=None):
        l = ix.shape[0]
        med = l//2
        
        # Split along the xaxis
        if splitx:
            n = kdTree_node(xs[ix[med]], ys[ix[med]], True)
            if father != None:
                
                n.xmin = father.xmin
                n.xmax = father.xmax
                n.ymin = father.ymin
                n.ymax = father.ymax
                
                if n.y <= father.y:
                    n.ymax = father.y
                    
                else:
                    n.ymin = father.y 
                    
            if med > 0:
                sub_iy = self.__select(ix[:med],iy)
                n.left = self.__buildTree(xs, ys, ix[:med], sub_iy, False, n)
            if med+1<l:
                sub_iy = self.__select(ix[med+1:], iy)
                n.right = self.__buildTree(xs, ys, ix[med+1:], sub_iy, False, n)
            
        # This node corresponds to a split of the data along y
        else:

            n = kdTree_node(xs[iy[med]], ys[iy[med]], False)
            if father != None:

                n.xmin = father.xmin
                n.xmax = father.xmax
                n.ymin = father.ymin
                n.ymax = father.ymax

                if n.x < father.x:
                    n.xmax = father.x

                else:
                    n.xmin = father.x

            if med > 0:
                sub_ix = self.__select(iy[:med],ix)
                n.left = self.__buildTree(xs, ys, sub_ix, iy[:med], True, n)
            if med+1<l:
                sub_ix = self.__select(iy[med+1:], ix)
                n.right = self.__buildTree(xs, ys, sub_ix, iy[med+1:], True, n)

        return n 
    
    def is_fully_contained(self, node, r):
        if node:
            if r['xmin'] <= node.xmin and r['xmax'] >= node.xmax and r['ymin'] <= node.ymin and r['ymax'] >= node.ymax:
                return True
        return False
    
    def is_intersect(self, node, r):
        if node:
            if r['ymin'] > node.ymax or r['ymax'] < node.ymin or r['xmin'] > node.xmax or r['xmax'] < node.xmin:
                return False
        return True
    
    def range_search(self, node, r):
       
        results = []
        if node == None:
            return results
        if node.left == None and node.right == None:
            
            if r['xmin'] <= node.x and r['xmax'] >= node.x and r['ymin'] <= node.y and r['ymax'] >= node.y:
                results.append(node)
         
        else:
            if r['xmin'] <= node.x and r['xmax'] >= node.x and r['ymin'] <= node.y and r['ymax'] >= node.y:
                results.append(node)
                
            if self.is_fully_contained(node.left, r):
                results += self.traverse(node.left)
            
            elif self.is_intersect(node.left, r):
                results += self.range_search(node.left, r)
            
            if self.is_fully_contained(node.right, r):
                results += self.traverse(node.right)
                
            elif self.is_intersect(node.right, r):
                results += self.range_search(node.right, r)
               
        return results

    def traverse(self, node):
        members = []
        if node:
            members += self.traverse(node.left)
            members.append(node)
            members += self.traverse(node.right)
        return members