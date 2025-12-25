grammar GuildFlow;

// ========================================
// A. THE STRUCTURE (P1)
// ========================================

// Entry point: accepts multiple definitions
prog
    : (workflow_def | state_def)+ EOF
    ;

// WORKFLOW definition: WORKFLOW name ON event { ... }
workflow_def
    : 'WORKFLOW' IDENTIFIER 'ON' IDENTIFIER '{' statement* '}'
    ;

// STATE definition: STATE name { ... }
state_def
    : 'STATE' IDENTIFIER '{' state_body '}'
    ;

state_body
    : ('ON_ENTRY' '{' statement* '}')?
    | ('ON_EXIT' '{' statement* '}')?
    | ('TRANSITION' 'TO' IDENTIFIER)?
    ;

// ========================================
// B. THE ACTIONS (P1 - P2)
// ========================================

// All statements
statement
    : action_statement
    | if_statement
    | set_statement
    | extract_stmt
    | components_block
    ;

// Action statement wrapper
action_statement
    : action_command ';'?
    ;

// Action commands
action_command
    : 'SEND_MESSAGE' '(' param_list ')'
    | 'REPLY_MESSAGE' '(' param_list ')'
    | 'BAN_USER' '(' param_list? ')'
    | 'TIMEOUT_USER' '(' param_list ')'
    | 'ACTION' ':' action_type param*
    ;

action_type
    : 'BAN_USER'
    | 'SEND_MESSAGE'
    | 'TIMEOUT_USER'
    | 'REPLY_MESSAGE'
    ;

param_list
    : param (',' param)*
    ;

param
    : IDENTIFIER '=' value
    | value
    ;

value
    : STRING_LITERAL
    | NUMBER
    | IDENTIFIER
    ;

// ========================================
// C. THE LOGIC & COMPONENTS (P2 - P3)
// ========================================

// IF statement with nested support
if_statement
    : 'IF' condition '{' statement* '}' ('ELSE' '{' statement* '}')?
    ;

// Conditions
condition
    : expression comparison_op expression
    | expression 'CONTAINS' expression
    | expression
    ;

comparison_op
    : '==' | '!=' | '>' | '<' | '>=' | '<='
    ;

expression
    : IDENTIFIER ('.' IDENTIFIER)*
    | NUMBER
    | STRING_LITERAL
    ;

// SET statement
set_statement
    : 'SET' IDENTIFIER '=' expression ';'?
    ;

// EXTRACT statement
extract_stmt
    : 'EXTRACT' IDENTIFIER 'FROM' expression ('USING' STRING_LITERAL)? ';'?
    ;

// COMPONENTS block
components_block
    : 'COMPONENTS' ':' '[' component (',' component)* ']'
    ;

component
    : 'BUTTON' '{' button_property* '}'
    ;

button_property
    : IDENTIFIER ':' value
    ;

// ========================================
// LEXER RULES
// ========================================

// Keywords
WORKFLOW: 'WORKFLOW';
STATE: 'STATE';
ON: 'ON';
IF: 'IF';
ELSE: 'ELSE';
SET: 'SET';
EXTRACT: 'EXTRACT';
FROM: 'FROM';
USING: 'USING';
COMPONENTS: 'COMPONENTS';
BUTTON: 'BUTTON';
ACTION: 'ACTION';
ON_ENTRY: 'ON_ENTRY';
ON_EXIT: 'ON_EXIT';
TRANSITION: 'TRANSITION';
TO: 'TO';
CONTAINS: 'CONTAINS';

// Action types
BAN_USER: 'BAN_USER';
SEND_MESSAGE: 'SEND_MESSAGE';
REPLY_MESSAGE: 'REPLY_MESSAGE';
TIMEOUT_USER: 'TIMEOUT_USER';

// Literals
STRING_LITERAL
    : '"' (~["\r\n\\] | '\\' .)* '"'
    ;

NUMBER
    : [0-9]+
    ;

IDENTIFIER
    : [a-zA-Z_][a-zA-Z0-9_]*
    ;

// Whitespace and comments
WS: [ \t\r\n]+ -> skip;

LINE_COMMENT: '//' ~[\r\n]* -> skip;

BLOCK_COMMENT: '/*' .*? '*/' -> skip;