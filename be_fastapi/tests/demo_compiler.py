import json
from compiler.compiler import compile_code, CompilerError

sample_source = '''
WORKFLOW WelcomeFlow ON MEMBER_JOIN {
    ACTION: SEND_MESSAGE channel="welcome" content="Hello!"
}
'''

if __name__ == '__main__':
    try:
        compiled = compile_code(sample_source)
        print(json.dumps(compiled, indent=2))
    except CompilerError as e:
        print('CompilerError:', e)
    except Exception as e:
        print('Error:', e)
