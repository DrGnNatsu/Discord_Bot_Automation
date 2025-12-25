"""
Test script to verify GuildFlow grammar parsing
"""
import sys
from antlr4 import *
from antlr.src.antlr_build.GuildFlowLexer import GuildFlowLexer
from antlr.src.antlr_build.GuildFlowParser import GuildFlowParser

def test_grammar():
    # Test input - Anti-Raid example
    input_code = """
        WORKFLOW anti_raid ON member_join {
            IF user.account_age < 7 {
                ACTION: BAN_USER
            } ELSE {
                ACTION: SEND_MESSAGE channel=general content="Welcome!"
            }
        }
    """

    print("=" * 60)
    print("Testing GuildFlow Grammar Parser")
    print("=" * 60)
    print("\nInput Code:")
    print(input_code)
    print("\n" + "=" * 60)
    
    try:
        # Create input stream
        input_stream = InputStream(input_code)
        
        # Create lexer
        lexer = GuildFlowLexer(input_stream)
        
        # Create token stream
        token_stream = CommonTokenStream(lexer)
        
        # Create parser
        parser = GuildFlowParser(token_stream)
        
        # Parse the input
        tree = parser.prog()
        
        # Print the parse tree in LISP format
        print("\nSUCCESS! Parse Tree (LISP format):")
        print("-" * 60)
        print(tree.toStringTree(recog=parser))
        print("-" * 60)
        
        # Check for syntax errors
        if parser.getNumberOfSyntaxErrors() == 0:
            print("\nNo syntax errors detected!")
            print("Grammar validation PASSED!")
            return True
        else:
            print(f"\nFound {parser.getNumberOfSyntaxErrors()} syntax error(s)")
            return False
            
    except Exception as e:
        print(f"\nERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_grammar()
    sys.exit(0 if success else 1)