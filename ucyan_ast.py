import sys

def represent_node(obj, indent):
    def _repr(obj, indent, printed_set):
        """
        Get the representation of an object, with dedicated pprint-like format for lists.
        """
        if isinstance(obj, list):
            indent += 1
            sep = ",\n" + (" " * indent)
            final_sep = ",\n" + (" " * (indent - 1))
            return (
                "["
                + (sep.join((_repr(e, indent, printed_set) for e in obj)))
                + final_sep
                + "]"
            )
        elif isinstance(obj, Node):
            if obj in printed_set:
                return ""
            else:
                printed_set.add(obj)
            result = obj.__class__.__name__ + "("
            indent += len(obj.__class__.__name__) + 1
            attrs = []
            for name in obj.__slots__:
                if name == "bind":
                    continue
                value = getattr(obj, name)
                value_str = _repr(value, indent + len(name) + 1, printed_set)
                attrs.append(name + "=" + value_str)
            sep = ",\n" + (" " * indent)
            final_sep = ",\n" + (" " * (indent - 1))
            result += sep.join(attrs)
            result += ")"
            return result
        elif isinstance(obj, str):
            return obj
        else:
            return ""

    # avoid infinite recursion with printed_set
    printed_set = set()
    return _repr(obj, indent, printed_set)

class Node:
    """Abstract base class for AST nodes."""

    __slots__ = ("coord", "attrs",)

    def __init__(self, coord=None):
        self.coord = coord
        self.attrs = {}

    def children(self):
        """A sequence of all children that are Nodes"""
        pass

    attr_names = ()

    def __repr__(self):
        """Generates a python representation of the current node"""
        return represent_node(self, 0)

    def show(
        self,
        buf=sys.stdout,
        offset=0,
        attrnames=False,
        nodenames=False,
        showcoord=False,
        _my_node_name=None,
    ):
        """Pretty print the Node and all its attributes and children (recursively) to a buffer.
        buf:
            Open IO buffer into which the Node is printed.
        offset:
            Initial offset (amount of leading spaces)
        attrnames:
            True if you want to see the attribute names in name=value pairs. False to only see the values.
        nodenames:
            True if you want to see the actual node names within their parents.
        showcoord:
            Do you want the coordinates of each Node to be displayed.
        """
        lead = " " * offset
        if nodenames and _my_node_name is not None:
            buf.write(lead + self.__class__.__name__ + " <" + _my_node_name + ">: ")
            inner_offset = len(self.__class__.__name__ + " <" + _my_node_name + ">: ")
        else:
            buf.write(lead + self.__class__.__name__ + ":")
            inner_offset = len(self.__class__.__name__ + ":")

        if self.attr_names:
            if attrnames:
                nvlist = [
                    (n, represent_node(getattr(self, n), offset+inner_offset+1+len(n)+1))
                    for n in self.attr_names
                    if getattr(self, n) is not None
                ]
                attrstr = ", ".join("%s=%s" % nv for nv in nvlist)
            else:
                vlist = [getattr(self, n) for n in self.attr_names]
                attrstr = ", ".join(
                    represent_node(v, offset + inner_offset + 1) for v in vlist
                )
            buf.write(" " + attrstr)

        if showcoord:
            if self.coord and self.coord.line != 0:
                buf.write(" %s" % self.coord)
        buf.write("\n")

        for (child_name, child) in self.children():
            child.show(buf, offset + 4, attrnames, nodenames, showcoord, child_name)

class NodeVisitor:
    """ A base NodeVisitor class for visiting uc_ast nodes.
        Subclass it and define your own visit_XXX methods, where
        XXX is the class name you want to visit with these
        methods.
    """

    _method_cache = None

    def visit(self, node):
        """ Visit a node.
        """

        if self._method_cache is None:
            self._method_cache = {}

        visitor = self._method_cache.get(node.__class__.__name__, None)
        if visitor is None:
            method = 'visit_' + node.__class__.__name__
            visitor = getattr(self, method, self.generic_visit)
            self._method_cache[node.__class__.__name__] = visitor

        return visitor(node)

    def generic_visit(self, node):
        """ Called if no explicit visitor function exists for a
            node. Implements preorder visiting of the node.
        """
        for _, child in node.children():
            self.visit(child)



class AssignmentStatement(Node):
  __slots__ = ("location", "expression",)

  def __init__(self, location, expression, coord=None):
    super().__init__(coord)
    self.location = location
    self.expression = expression
    

  def children(self):
    nodelist = []
    if self.location is not None:
      nodelist.append(('location', self.location))
    if self.expressaoAritmetica is not None:
      nodelist.append(('expression', self.expression))
    return tuple(nodelist)




class BinaryOp(Node):

    __slots__ = ("op", "left", "right",)

    def __init__(self, op, left, right, coord=None):
        super().__init__(coord)
        self.op = op
        self.left = left
        self.right = right

    def children(self):
        nodelist = []
        if self.left is not None:
            nodelist.append(('left', self.left))
        if self.right is not None:
            nodelist.append(('right', self.right))
        return tuple(nodelist)

    attr_names = ("op",)




class BreakStatement(Node):

    # Pode estar errado
    __slots__ = ()

    def __init__(self, op, left, right, coord=None):
        super().__init__(coord)

    def children(self):
        nodelist = []
        return tuple(nodelist)

    attr_names = ()




class ConstDefinition(Node):
  pass
    # <<< YOUR CODE HERE >>>




class ContinueStatement(Node):
  pass
    # <<< YOUR CODE HERE >>>




class ExpressionAsStatement(Node):
  __slots__ = ("expression",)

  def __init__(self, expression, coord=None):
    super().__init__(coord)
    self.expression = expression

  def children(self):
    nodelist = []
    if self.expression is not None:
      nodelist.append(('expression', self.expression))
    return tuple(nodelist)

  attr_names = ()




class IfStatement(Node):
  pass
    # <<< YOUR CODE HERE >>>




class Literal(Node):

    __slots__ = ("type", "value",)

    def __init__(self, type, value, coord=None):
        super().__init__(coord)
        self.type = type
        self.value = value

    def children(self):
        nodelist = []
        return tuple(nodelist)

    attr_names = ("type", "value",)




class Location(Node):

    __slots__ = ("name",)

    def __init__(self, name, coord=None):
      super().__init__(coord)
      self.name = name

    def children(self):
      nodelist = []
      return tuple(nodelist)

    attr_names = ("name",)




class PrintStatement(Node):
  __slots__ = ("expression",)

  def __init__(self, expression, coord=None):
    super().__init__(coord)
    self.expression = expression

  def children(self):
    nodelist = []
    if self.expression is not None:
        nodelist.append(('expression', self.expression))
    return tuple(nodelist)




class Program(Node):

    __slots__ = ("statements",)

    def __init__(self, statements, coord=None):
        super().__init__(coord)
        self.statements = statements

    def children(self):
        nodelist = []
        for i, child in enumerate(self.statements or []):
            nodelist.append(('statements[%d]' % i, child))
        return tuple(nodelist)

    attr_names = ()




class Type(Node):
  __slots__ = ("name",)

  def __init__(self, name, coord=None):
    super().__init__(coord)
    self.name = name

  def children(self):
    nodelist = []
    return tuple(nodelist)

  attr_names = ("name",)




class UnaryOp(Node):
  pass
    # <<< YOUR CODE HERE >>>




class VarDefinition(Node):

  __slots__ = ("name", "dtype", "expression",)

  def __init__(self, name, dtype, expression, coord=None):
    super().__init__(coord)
    self.name = name
    self.dtype = dtype
    self.expression = expression

  def children(self):
    nodelist = []
    if self.dtype is not None:
      nodelist.append(('dtype', self.dtype))
    if self.expression is not None:
      nodelist.append(('expression', self.expression))
    return tuple(nodelist)

  attr_names = ("name",)




class WhileStatement(Node):
  __slots__ = ("test", "body",)

  def __init__(self, test, body, coord=None):
    super().__init__(coord)
    self.test = test
    self.body = body

  def children(self):
    nodelist = []
    if self.test is not None:
      nodelist.append(('test', self.test))
    if self.body is not None:
      nodelist.append(('body', self.body))
    return tuple(nodelist)
