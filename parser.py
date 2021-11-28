from .lexer import *

@dataclass
class DimensionNode:
    value: any

@dataclass
class NumberNode:
    value: any

    def __repr__(self):
        return f"{self.value}"

@dataclass
class AddNode:
    node_a: any
    node_b: any

    def __repr__(self):
        return f"({self.node_a}+{self.node_b})"

@dataclass
class SubtractNode:
    node_a: any
    node_b: any

    def __repr__(self):
        return f"({self.node_a}-{self.node_b})"

@dataclass
class MultiplyNode:
    node_a: any
    node_b: any

    def __repr__(self):
        return f"({self.node_a}*{self.node_b})"

@dataclass
class DivideNode:
    node_a: any
    node_b: any

    def __repr__(self):
        return f"({self.node_a}/{self.node_b})"

@dataclass
class PowNode:
    node_a: any
    node_b: any
    def __repr__(self):
        return f"({self.node_a}**{self.node_b})"
    
@dataclass
class PlusNode:
    node: any

    def __repr__(self):
        return f"(+{self.node})"
    
@dataclass
class MinusNode:
    node: any

    def __repr__(self):
        return f"(-{self.node})"
    
class Parser():
    def __init__(self, tokens):
        # A parser is an iterable of tokens
        self.tokens = iter(tokens)
        self.advance()
        
    def raise_error(self):
        raise Exception("Invalid Syntax.")
        
    def advance(self):
        try:
            self.current_token = next(self.tokens)
        except StopIteration:
            self.current_token = None
            
    def parse(self):
        if self.current_token == None:
            return None
        result = self.expr()
        if self.current_token != None:
            self.raise_error()
        
        return result
    
    def expr(self):
        result = self.term()

        while self.current_token != None and self.current_token.type in (TokenType.PLUS,
                                                                         TokenType.MINUS):
            if self.current_token.type == TokenType.PLUS:
                self.advance()
                result = AddNode(result, self.term())
            elif self.current_token.type == TokenType.MINUS:
                self.advance()
                result = SubtractNode(result, self.term())
        return result
    

    def term(self):
        result = self.expo()

        while self.current_token != None and self.current_token.type in (TokenType.MULTIPLY,
                                                                         TokenType.DIVIDE):
            if self.current_token.type == TokenType.MULTIPLY:
                self.advance()
                result = MultiplyNode(result, self.expo())
            elif self.current_token.type == TokenType.DIVIDE:
                self.advance()
                result = DivideNode(result, self.expo())
                
        return result

    def expo(self):
        result = self.factor()
    
        while self.current_token != None and self.current_token.type == TokenType.POW:
            self.advance()
            result = PowNode(result, self.factor())    
        return result
    
    
    def factor(self):
        token = self.current_token

        if token.type == TokenType.LPAREN:
            self.advance()
            result = self.expr()

            if self.current_token.type != TokenType.RPAREN:
                self.raise_error()
            
            self.advance()
            return result

        
        elif token.type == TokenType.NUMBER:
            self.advance()
            return NumberNode(token.value)
        
        elif token.type == TokenType.DIMENSION:
            self.advance()
            return DimensionNode(token.value) 

        elif token.type == TokenType.PLUS:
            self.advance()
            return PlusNode(self.factor())
        
        elif token.type == TokenType.MINUS:
            self.advance()
            return MinusNode(self.factor())
        
        self.raise_error()
        
        
if __name__ == "__main__":
    to_parse = [
        "m",
        "L",
        "L*M/T**2",
        "L/T**2",
        "T**(-2)",
        "RAD",
        "L**2*T",
        "L**2*T",
        "L*M",
        "theta",
        "L**10",
        "I**2*T**3/(L**2*M)",
        "1/M",
        "L**1.2",
        "L*theta**3/J",
        "theta**(-4)",   
    ]
    for text in to_parse:
        print(text)
        lexer = Lexer(text)
        lexed = list(lexer.generate_tokens())
        print(lexed)
        parser = Parser(lexed)
        tree = parser.parse()
        print(tree)