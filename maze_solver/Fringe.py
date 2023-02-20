"""
- Fringe is the base class of fringe subclasses.
  Let f be a fringe.
    - f.put(x)  :
    - f.get(x)  :
    - x in f    : membership (i.e., __contains__)
    - size
    - len(f)    : length (i.e., __len__)
    - for x in f: __iter__() use in for loops

Stack and Queue
    Subclasses of Fringe class

FSStack and FSQueue
    A FSStack object contains a stack and a set. They contain the same values.
    The set is used for find membership fast (with O(1) runtime). This is also
    the same for FSQueue.

IDFSStack
    Iterative Deepening FSStack. The depth limit is increased with each iteration
    of the search. 
"""



import collections


class Fringe(object):
    def __init__(self):
        object.__init__(self)
    def put(self, x):
        raise NotImplementedError
    def get(self, x):
        raise NotImplementedError
    def __contains__(self):
        raise NotImplementedError
    def size(self):
        raise NotImplementedError
    def __len__(self):
        return 0 # Must be overwritten
    def __contains__(self, x):
        raise NotImplementedError
    def __iter__(self):
        raise NotImplementedError
 
    
class Stack(Fringe):
    def __init__(self):
        Fringe.__init__(self)
        self.deque = collections.deque()
    def put(self, node):
        if node.state not in [n.state for n in self.deque]:
            self.deque.append(node)
    def get(self):
        return self.deque.pop()
    def __len__(self):
        return len(self.deque)
    def size(self):
        return len(self.deque)
    def __contains__(self, node):
        for n in self.deque:
            if node.state == n.state:
                return True
        return False
    def __str__(self):
        s = str(self.deque)[7:-2]
        return '<Stack [%s]>' % s
    def __iter__(self):
        return iter(self.deque)

    
class Queue(Fringe):
    def __init__(self):
        Fringe.__init__(self)
        self.deque = collections.deque()
    def put(self, x):
        self.deque.append(x)
    def get(self):
        return self.deque.popleft()
    def __len__(self):
        return len(self.deque)
    def size(self):
        return len(self.deque)
    def __contains__(self, node):
        for n in self.deque:
            if node.state == n.state:
                return True
        return False
    def __str__(self):
        s = str(self.deque)[7:-2]
        return '<Queue [%s]>' % s
    def __iter__(self):
        return iter(self.deque)


class FSStack(Fringe):
    def __init__(self):
        Fringe.__init__(self)
        self.stack = Stack()
        self.dict = {}
    def put(self, node):
        if not node in self:
            self.stack.put(node)
            self.dict[node.state] = 1
    def get(self):
        r = self.stack.get()
        del self.dict[r.state]
        return r
    def __len__(self):
        return len(self.stack) 
    def size(self):
        return len(self.stack)
    def __contains__(self, node):
        return self.dict.has_key(node.state)
    def __str__(self):
        return str(self.stack)
    def __iter__(self):
        return iter(self.stack)

    
class FSQueue(Fringe):
    def __init__(self):
        Fringe.__init__(self)
        self.queue = Queue()
        self.dict = {}
    def put(self, node):
        if not node in self:
            self.queue.put(node)
            self.dict[node.state] = 1
    def get(self):
        r = self.queue.get()
        del self.dict[r.state]
        return r
    def __len__(self):
        return len(self.queue)
    def size(self):
        return len(self.queue)
    def __contains__(self, node):
        return self.dict.has_key(node.state)
    def __str__(self):
        return str(self.queue)    
    def __iter__(self):
        return iter(self.queue)


class IDFSStack(FSStack):
    def __init__(self):
        FSStack.__init__(self)
        self.limit = 0
        self.deeper_state = False
    
    def put(self, node):
        if (node.priority() <= self.limit) and (not node in self):
            self.stack.put(node)
            self.dict[node.state] = 1
        elif node.priority() > self.limit:
            self.deeper_state = True
    
    def set_limit(self, x):
        self.limit = x
        
    def deeper_limit(self):
        return self.deeper_state

class UCSFringe(Fringe):
    def __init__(self):
        Fringe.__init__(self)
        self.array = []
        self.d = {}
         
    def put(self, node):
        if not node in self:
            self.d[node.state] = len(self.array)
            self.array.append(node)
            index = len(self.array) - 1
        else:
            n1 = self.array[self.d[node.state]] 
            index = self.d[node.state]
            if node.priority() < n1.priority():
                self.array[self.d[node.state]] = node
            else : pass
        self.heapify_up(index)

    def get(self):
        r = self.array[0]
        self.array[0] = self.array[len(self.array) - 1]
        self.d[self.array[0].state] = 0
        del self.array[len(self.array) - 1]
        del self.d[r.state]
        
        self.heapify_down()
        return r

    def heapify_down(self, i=0):
        xs = self.array
        while 1:
            l, r = self.left(i), self.right(i)
            swap_index = -1
            if (l < len(xs)) and (r < len(xs)):         # 2 children
                if xs[l].priority() <= xs[r].priority():
                    swap_index = l
                elif xs[l].priority() > xs[r].priority():
                    swap_index = r
            elif (l < len(xs)) and (r >= len(xs)):   # 1 (left) child
                    swap_index = l

            if (swap_index != -1) and (xs[swap_index].priority() < xs[i].priority()):
                xs[i], xs[swap_index] = xs[swap_index], xs[i]
                self.d[xs[i].state], self.d[xs[swap_index].state] = self.d[xs[swap_index].state], self.d[xs[i].state]
                i = swap_index
            else:
                break

    def heapify_up(self, i):    # i = len(array)-1 / index of the new node
        xs = self.array
        while (i > 0) and (xs[i].priority() < xs[self.parent(i)].priority()):
            state = xs[i].state
            p_state = xs[self.parent(i)].state
            
            xs[i], xs[self.parent(i)] = xs[self.parent(i)], xs[i]
            self.d[state], self.d[p_state] = self.d[p_state], self.d[state]
            i = self.parent(i)
    
    def parent(self, i):        # parent of node at index i is (i - 1) / 2
        while i > 0:
            return (i - 1) / 2  
    def left(self, i):          # left child node at index i is 2*i + 1
        return (2 * i) + 1
    def right(self, i):         # right child node at index i is 2*i + 2
        return (2 * i) + 2
    def __len__(self):
        return len(self.array)
    def size(self):
        return len(self.array)
    def __contains__(self, node):
        return self.d.has_key(node.state)
    def __str__(self):
        s = ', '.join(str(x) for x in self.array)
        return '<UCSFringe [%s]>' % s
    def __iter__(self):
        return iter(self.array)


if __name__ == '__main__':
    from SearchNode import SearchNode
    print ("Testing stackfringe with search nodes from (0,0) -> (1,0) -> (1,1) by actions ['E', 'S']")
    fringe = Stack()
    state00 = (0, 0)
    node00 = SearchNode(state00)
    state01 = (0, 1)
    node01 = SearchNode(state01, node00, 'E', 1)
    state11 = (1, 1)
    node11 = SearchNode(state11, node01, 'S', 1)
    print(node00)
    print(node01)
    print(node11)

    print(fringe)
    fringe.put(node00)
    print(node00 in fringe)
    print(node01 in fringe)
    print(node11 in fringe)
    
    print(fringe)
    fringe.put(node01)
    print(node00 in fringe)
    print(node01 in fringe)
    print(node11 in fringe)

    print(fringe)
    fringe.put(node11)
    print(node00 in fringe)
    print(node01 in fringe)
    print(node11 in fringe)

    print(fringe)
    n = fringe.get()
    print(n)
    print(node00 in fringe)
    print(node01 in fringe)
    print(node11 in fringe)

    print(fringe)
    n = fringe.get()
    print(n)
    print(node00 in fringe)
    print(node01 in fringe)
    print(node11 in fringe)
    
    print(fringe)
    n = fringe.get()
    print(n)
    print(node00 in fringe)
    print(node01 in fringe)
    print(node11 in fringe)

    print(fringe)
    try:    
        n = fringe.get()
        print(n)
    except IndexError:
        print("stack fringe is empty ... cannot get()")
    print(node00 in fringe)
    print(node01 in fringe)
    print(node11 in fringe)
   
    class TestSearchNode:
        def __init__(self, state, pri):
            self.state = state
            self.pri = pri
        def priority(self):
            return self.pri
        def __str__(self):
            return '<%s %s>' % (self.state, self.pri)
   
   
    n0 = TestSearchNode('a', 8)
    n1 = TestSearchNode('b', 7)
    n2 = TestSearchNode('c', 4)
    n3 = TestSearchNode('d', 2)
    n4 = TestSearchNode('e', 6)
    n5 = TestSearchNode('f', 1)
    
    ns = [n0, n1, n2, n3, n4, n5]
    f = UCSFringe()
    print(f)
    for n in ns:
        f.put(n)
        print ("insert", n, "...", f)

    print ("Checking fringe ...")
    #f.check()

    print ("Testing inserting duplicate state with larger priority")
    f.put(TestSearchNode('e',10))
    print(f)
    
    print ("Testing inserting duplicate state with smaller priority")
    f.put(TestSearchNode('e', 0))
    print(f)
    
    while len(f) != 0:
        n = f.get()
        print ("get", n, "...", f)


    
