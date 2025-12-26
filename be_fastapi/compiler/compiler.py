from antlr4 import InputStream, CommonTokenStream
from antlr4.error.ErrorListener import ErrorListener
from antlr.compiled_files.GuildFlowLexer import GuildFlowLexer
from antlr.compiled_files.GuildFlowParser import GuildFlowParser
from .visitor import GuildFlowCompiler 

class CompilerError(Exception):
    """Custom exception for compilation errors"""
    pass

class SyntaxErrorListener(ErrorListener):
    """Custom error listener to capture syntax errors"""
    def __init__(self):
        super().__init__()
        self.errors = []
    
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        error_msg = f"Line {line}:{column} - {msg}"
        self.errors.append(error_msg)

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
        CompilerError: If there are syntax or compilation errors
    """
    try:
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
        tree = parser.prog()
        
        # Check for syntax errors
        if error_listener.errors:
            raise CompilerError("Syntax errors found:\n" + "\n".join(error_listener.errors))
        
        # 3. Use Visitor to convert to JSON
        visitor = GuildFlowCompiler()
        result = visitor.visit(tree)
        
        return result
        
    except CompilerError:
        raise
    except Exception as e:
        raise CompilerError(f"Compilation failed: {str(e)}")