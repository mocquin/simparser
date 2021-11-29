from enum import Enum
import ast
from dataclasses import dataclass
from dimension import BasicDimension

class TokenType(Enum):
    """
    Create a new attribute for each token allowed.
    """
    DIMENSION = 0
    MULTIPLY = 1
    DIVIDE = 2
    POW = 3
    NUMBER = 4
    PLUS = 5
    MINUS = 6
    LPAREN = 7
    RPAREN = 8
    
    
@dataclass
class Token():
    type: TokenType
    value: any = None
    
    def __repr__(self):
        return self.type.name + (f":{self.value}" if self.value != None else "")
    
WHITESPACE = ""
DIGITS = '0123456789'
DIMENSION = [
    "m", "s", "K", "cd", "rad", "kg",
    "L", "T", "theta", "RAD", "M", "I", "J",
]

class Lexer():
    def __init__(self, text):
        self.text = iter(text)
        self.advance()
        
    def advance(self):
        try:
            self.current_char = next(self.text)
        except StopIteration:
            self.current_char = None
            
    def generate_tokens(self):
        while self.current_char != None:
            if self.current_char in WHITESPACE:
                self.advance()
            elif self.current_char == "." or self.current_char in DIGITS:
                yield self.generate_number()
            elif self.current_char == "*":
                #self.advance()
                #yield Token(TokenType.MULTIPLY)
                yield self.generate_mulpow()
            elif self.current_char == "^":
                self.advance()
                yield Token(TokenType.POW)
            elif self.current_char == "/":
                self.advance()
                yield Token(TokenType.DIVIDE)
            elif self.current_char in "".join(DIMENSION):
                #self.advance()
                #yield Token(TokenType.DIMENSION)
                yield self.generate_dim()
            elif self.current_char == "-":
                self.advance()
                yield Token(TokenType.MINUS)
            elif self.current_char == "+":
                self.advance()
                yield Token(TokenType.PLUS)
            elif self.current_char == "(":
                self.advance()
                yield Token(TokenType.LPAREN)
            elif self.current_char == ")":
                self.advance()
                yield Token(TokenType.RPAREN)
            else:
                raise Exception
            
    def generate_mulpow(self):
        self.advance()
        if self.current_char != None and (self.current_char == "*"):
            self.advance()
            return Token(TokenType.POW)
        else:
            return Token(TokenType.MULTIPLY)
                
    def generate_number(self):
        decimal_point_count = 0
        number_str = self.current_char
        self.advance()
        
        while self.current_char != None and (self.current_char == "." or self.current_char in DIGITS):
            if self.current_char == ".":
                decimal_point_count +=1
                if decimal_point_count>1:
                    break
            number_str += self.current_char
            self.advance()
        
        if number_str.startswith('.'):
            number_str = '0'+ number_str
        if number_str.endswith('.'):
            number_str = number_str + "0"
        return Token(TokenType.NUMBER, 
                     ast.literal_eval(number_str))
            
    def generate_dim(self):
        dimension_str = self.current_char
        self.advance()
        
        while self.current_char != None and self.current_char in "".join(DIMENSION):
            dimension_str += self.current_char
            self.advance()
        #dim = Dimension(dimension_str)
        #return Token(TokenType.DIMENSION,
        #             dim)
        return Token(TokenType.DIMENSION, 
                    BasicDimension(dimension_str))
    
    
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
        for t in lexed:
            print(repr(t), type(t.value), t.value)
        #print(ast.dump(ast.parse(text)))