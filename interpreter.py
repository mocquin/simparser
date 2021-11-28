###############################################################################
from lexer import *
from parser import *


from collections import Counter

class Interpreter:
    def __init__(self, tree):
        self.tree = tree
        self.pow_dict = {}
        
    def parse_tree(self):
        return self.visit(self.tree)
        
    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name)
        return method(node)
        
    def visit_int(self, node):
        return Number(node.value)
        
    def visit_float(self, node):
        return NumberNode(node.value)
        
    def visit_NumberNode(self, node):
        return NumberNode(node.value)

    def visit_DimensionNode(self, node):
        #if type(node) is str:
        #    return DimensionNode(Dimension(node))
        #elif type(node) is Dimension:
        #    return DimensionNode(node.value)
        return DimensionNode(node.value)
        #else:
        #    raise ValueError(f"for {node}")
    
    
    def visit_AddNode(self, node):
        return Number(self.visit(node.node_a).value + self.visit(node.node_b).value)
    
    def visit_SubtractNode(self, node):
        return Number(self.visit(node.node_a).value - self.visit(node.node_b).value)

    def visit_MultiplyNode(self, node):
        #print(f"visit_MulNode({node})")
        #if node.node_a.value not in self.pow_dict.keys():
        #    self.pow_dict[node.node_a.value] = 1
        #else:
        #    self.pow_dict[node.node_a.value] += 1
        #if node.node_b.value not in self.pow_dict.keys():
        #    self.pow_dict[node.node_b.value] = 1
        #else:
        #    self.pow_dict[node.node_b.value] += 1
#
        #return  self.pow_dict
        return DimensionNode(self.visit(node.node_a).value * self.visit(node.node_b).value)

    def visit_DivideNode(self, node):
        try:
            return Number(self.visit(node.node_a).value / self.visit(node.node_b).value)
        except:
            raise Exception("Runtime math error")
            
    def visit_PowNode(self, node):
        """
        PowNode's nodes should be leafs only, so not returning with self.visit
        """
        return DimensionNode(self.visit(node.node_a).value ** self.visit(node.node_b).value)
        #if node.node_a.value not in self.pow_dict.keys():
        #    self.pow_dict[self.visit(node.node_a).value] = self.visit(node.node_b.value)
        #else:
        #    self.pow_dict[self.visit(node.node_a).value] += self.visit(node.node_b.value)
        #return self.pow_dict

        
if __name__ == '__main__':
    


    text = "T**2.0"#*L**3*T"#/(L**2*M)"
    lexer = Lexer(text)
    lexed = list(lexer.generate_tokens())
    print(lexed)
    parser = Parser(lexed)
    tree = parser.parse()
    print(tree)

    print("####INTERPRETER")
    interpreter = Interpreter(tree)
    res = interpreter.parse_tree()
    print(type(res), res)
    res.value