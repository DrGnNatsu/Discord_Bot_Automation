from antlr4 import InputStream, CommonTokenStream
from antlr4.error.ErrorListener import ErrorListener
from antlr.compiled_files.GuildFlowLexer import GuildFlowLexer
from antlr.compiled_files.GuildFlowParser import GuildFlowParser
from .visitor import GuildFlowCompiler 

class SyntaxException(Exception):
    """Custom exception for syntax errors with location details"""
    def __init__(self, message, line, column):
        self.message = message
        self.line = line
        self.column = column
        super().__init__(self.message)

class SyntaxErrorListener(ErrorListener):
    """Custom error listener to capture syntax errors and raise immediately"""
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        # Raise immediately on first error to match requested behavior
        raise SyntaxException(msg, line, column)

def compile_code(source_code: str):
    """
    Function to take in the string of source code in GuildFlow DSL,
    parse it using ANTLR, and convert it to a JSON representation
    using the GuildFlowCompiler visitor.
    
    Args:
        source_code: the GuildFlow DSL source code as a string. 
        
    Returns:
        dict: JSON representation of workflow/state definitions
        
    Raises:
        SyntaxException: If there are syntax errors
        Exception: For other compilation errors
    """
    # 1. Initialize ANTLR Pipeline
    input_stream = InputStream(source_code)
    lexer = GuildFlowLexer(input_stream)
    
    # Add error listener to lexer
    error_listener = SyntaxErrorListener()
    lexer.removeErrorListeners()
    lexer.addErrorListener(error_listener)
    
    stream = CommonTokenStream(lexer)
    parser = GuildFlowParser(stream)
    
    # Add error listener to parser
    parser.removeErrorListeners()
    parser.addErrorListener(error_listener)
    
    # 2. Create parse tree
    # This will raise SyntaxException if errors are found
    tree = parser.prog()
    
    # 3. Use Visitor to convert to JSON
    visitor = GuildFlowCompiler()
    result = visitor.visit(tree)
    
    return result