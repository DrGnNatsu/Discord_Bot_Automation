grammar GuildFlow;

// ====== The Structure ======
prog: definition+ EOF;

definition
    : workflow_def
    | state_def
    ;

workflow_def
    : WORKFLOW IDENTIFIER ON event_type (WHERE condition)? LBRACE statement* RBRACE
    ;

event_type: IDENTIFIER;

state_def
    : STATE IDENTIFIER LBRACE statement* RBRACE
    ;

// Main statement rule collecting all possible operations
statement
    : action_statement
    | transition_statement
    | if_statement
    | set_statement
    | extract_statement
    | component_statement
    ;

// ===== The Actions ======
action_statement
    : ACTION COLON? command param*
    ;

command
    : 'SEND_MESSAGE'
    | 'REPLY_MESSAGE'
    | 'BAN_USER'
    | 'TIMEOUT_USER'
    | 'ADD_ROLE'
    ;

param
    : IDENTIFIER EQ expr
    ;

// ===== The Logic & Flow ======
if_statement
    : IF condition LBRACE statement* RBRACE (ELSE LBRACE statement* RBRACE)?
    ;

condition
    : expr comparator expr
    ;
    
comparator: '==' | '!=' | '>' | '<' | 'contains';

transition_statement
    : ENTER_STATE IDENTIFIER
    ;

// ===== UI Components ======
// This structure now supports any UI component (Button, SelectMenu, Modal, etc.)
component_statement
    : COMPONENTS COLON LBRACK component_element (COMMA component_element)* RBRACK
    ;

component_element
    : component_type LBRACE component_prop* RBRACE
    ;

// Allow any identifier as a component type (e.g., SelectMenu, TextInput)
// We also explicitly allow BUTTON to prevent conflicts with the reserved keyword
component_type: IDENTIFIER;

component_prop
    : prop_key EQ expr
    ;

// Allow keys to be any identifier or reserved keywords
prop_key: IDENTIFIER; 

// ===== Variable Assignments ======
set_statement
    : SET variable EQ expr
    ;

extract_statement
    : EXTRACT FIELD variable AS IDENTIFIER
    ;

// ===== Expressions & Values (Enhanced) ======
expr
    : value
    | variable
    | LPAREN expr RPAREN
    ;

variable
    : IDENTIFIER ('.' IDENTIFIER)*
    ;

// Enhanced value rule to support complex data structures (Arrays and Objects)
value
    : STRING
    | NUMBER
    | 'TRUE'
    | 'FALSE'
    | array_literal   // Support for lists (e.g., options=[...])
    | object_literal  // Support for nested objects
    ;

array_literal
    : LBRACK (expr (COMMA expr)*)? RBRACK
    ;

object_literal
    : LBRACE (component_prop (COMMA component_prop)*)? RBRACE
    ;

// ===== LEXICAL RULES ======

// Keywords
WORKFLOW: 'WORKFLOW';
ON: 'ON';
WHERE: 'WHERE';
STATE: 'STATE';
IF: 'IF';
ELSE: 'ELSE';
ENTER_STATE: 'ENTER_STATE'; 
SET: 'SET';
EXTRACT: 'EXTRACT';
FIELD: 'FIELD';
AS: 'AS';
ACTION: 'ACTION';

// Component Keywords
COMPONENTS: 'COMPONENTS';

// Separators and Operators
LBRACE: '{';
RBRACE: '}';
LBRACK: '[';
RBRACK: ']';
LPAREN: '(';
RPAREN: ')';
COLON: ':';
COMMA: ',';
EQ: '=';

// Identifiers and Literals
IDENTIFIER: [a-zA-Z_][a-zA-Z0-9_]*;
NUMBER
    : [+-]? ( [0-9]+ ('.' [0-9]*)? | '.' [0-9]+ ) ([eE][+-]?[0-9]+)?
    ;
STRING: '"' .*? '"';

// Skip rules
WS: [ \t\r\n]+ -> skip;
COMMENT: '//' ~[\r\n]* -> skip;