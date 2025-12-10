# GuildFlow: Project Documentation & Developer Guide

**Project Goal:** Create a Domain-Specific Language (DSL) that allows Discord server admins to write human-readable automation rules for moderation and event handling.  
**Architecture Strategy:** "Compiler-First" (DSL → JSON → Bot Execution).  
**Deadline:** 23/12/2025.

## 1. System Architecture

The system is a **monolithic Python application** (Bot + API) paired with a **React Frontend**. It does not use a live interpreter; instead, it compiles user scripts into a JSON "Instruction Set" that the bot reads and executes.

### 1.1 Data Flow

1. **Input:** User types script in **React Web UI**.
2. **Transport:** Frontend sends script string to **FastAPI Endpoint** (`POST /deploy`).
3. **Compilation:** Python backend runs **ANTLR4 Visitor** to convert Script → **JSON State Machine**.
4. **Storage:** JSON logic is saved to **SQLite** (`workflows` table).
5. **Execution:** **Discord Bot** listens for events, queries SQLite, and executes the JSON instructions.

#### 1.1.1 User Interaction (The Runtime Execution)

- **Goal**: The bot executes logic in real-time when a user chats in Discord.
- **Design Pattern**: The Command Pattern (Data-Driven) .
- **Why this solves the problem**: It eliminates massive if/else chains in your bot code. Instead of hardcoding logic, the bot acts as a generic "engine" that executes whatever instructions are found in the JSON database. This decouples the logic (Python code) from the behavior (JSON data).

##### How does is work?

1. Input:
    - Event: A Discord message object (e.g., content=!report).
    - Context: The User's current state from the database (e.g., state="awaiting_reason").
2. Logic (The "Command Dispatcher"):
    - The bot queries SQLite to retrieve the Action List (JSON) associated with the current state or trigger.
    - It iterates through the list. For each item, it looks up the type in a pre-defined Command Map.
    - The Command Map: A Python dictionary mapping string keys to functions.

    ```python
    COMMAND_MAP = {
        "SEND_MESSAGE": actions.send_message,
        "BAN_USER": actions.ban_user,
        "ENTER_STATE": actions.transition_state
    }
    ```

    - It calls the function: `COMMAND_MAP[action["type"]](action["params"])`.
3. Output:
    - The specific function executes (e.g., await channel.send("Hello")).
    - Database update (if the action was ENTER_STATE).

##### Associated Grammar Rules (Runtime)

| Rule Name | Pseudo-Grammar | Purpose | Implementation Difficulty | Example | Related Modules |
|---|---|---|---|---|---|
| **Trigger Filter** (P1) | ON message WHERE content contains "text" | Filters events to only proceed when specific criteria are met. | ⭐⭐ (Med)  | `ON message WHERE user_id IS NOT "admin" AND content CONTAINS "bad word"`| Event Listener  |
| **Action: Reply** (P1) | ACTION: SEND_MESSAGE channel=#log "Bad word detected" | Sends a message to a specified channel or user.  | ⭐ (Low) | `ACTION: SEND_MESSAGE channel=#mod_alerts "User {user} triggered a warning."` | Messaging API |
| **Action: Punish** (P1) | ACTION: TIMEOUT_USER duration="1h"  | Enforces moderation actions on a user. | ⭐ (Low) | `ACTION: TIMEOUT_USER duration="1h" reason="Spamming"` | Moderation API |
| **State Transition** (P2) | 'ENTER_STATE' ID  | The Navigator. Moves the user from one step of the flow to another, updating their persistent session | ⭐ (Low) SQL UPDATE query. | `ENTER_STATE awaiting_response` | Bot (user_states table update), DB |
| **Conditional Logic** (P3) | IF condition { ... } ELSE { ... }  | Allows branching execution based on runtime conditions. | ⭐⭐⭐ (High) | `IF user_role IS "member" { ACTION: WARN_USER }` | Logic Evaluator |
| **Variable Set** (P3) | 'SET' variable '=' expr | Persisting data (Memory).         | ⭐⭐⭐ (High) | `SET user.strikes = user.strikes + 1` | DB (Variable storage), Bot |

#### 1.1.2 Admin Deployment (The Compilation)

- **Goal**: Admin writes a script, and the system converts it into the JSON format required by Flow 1.
- **Design Pattern**: The Visitor Pattern.
- **Why this solves the problem**: ANTLR generates a complex "Parse Tree" that is hard to work with. The Visitor pattern provides a structured way to "visit" every node in that tree and return a value (the simplified JSON). This separates the parsing logic from the rest of your application

##### How does is work?

1. Input:
    - Raw Text String from Monaco Editor: `WORKFLOW demo ON message { ACTION: BAN_USER }`
    - Context: The User's current state from the database (e.g., state="awaiting_reason").
2. Logic (The "Tree Walker"):
    - The raw text is fed into the generated `GuildFlowParser`, which creates a `Parse Tree`
    - Your custom `GuildFlowCompiler` (which inherits from `Visitor`) is instantiated.
    - You call `compiler.visit(tree)`.
    - The Visit Loop:
        - The compiler hits the Workflow node $\rightarrow$ calls `visitWorkflow_def`.
        - `visitWorkflow_def` creates a dictionary { "type": "WORKFLOW" }.
        - It then calls `self.visit(child)` on all children (`the Actions`).
        - It aggregates the results into a list: "actions": `[{...}, {...}]`..
3. Output:
    - A clean JSON Object that is saved to the SQLite workflows table.
    - Validation: If the Visitor hits a node it doesn't understand (or a syntax error occurs), it raises an exception immediately, preventing bad code from entering the DB.

##### Associated Grammar Rules (Runtime)

| Rule Name | Pseudo-Grammar | Purpose | Implementation Difficulty | Example | Related Modules |
|---|---|---|---|---|---|
| **Program Definition** (P1) | definition+ EOF | The Root. The entry point for the parser. Validates that the file contains at least one valid definition | ⭐ (Low) | (The entire file content) | Compiler (visitProg), Web UI (Validation) |
| **Workflow Definition** (P1) | WORKFLOW name ON event { ... } | Defines the entry point for an automated process. | ⭐ (Low) | `WORKFLOW monitor_spam ON message { ... }` | Core Engine |
| **State Definition** (P2) | 'STATE' ID '{' stmt* '}' | The Sub-Routine. Defines a discrete step in a multi-step process. Compiles into a separate JSON block. | ⭐ (Low) | `STATE welcome_step_2 { ... }` | Compiler (visitState_def), DB |
| **Components Program** (P2) |'COMPONENTS:' '[' button... '] | The UI Builder. Defines interactive elements (Buttons) attached to a message. Essential for the "Interactive" requirement | ⭐⭐⭐ (High) Must map strings to Discord UI Objects.| `COMPONENTS: [ BUTTON "Yes" -> transition_to(next) ]` | Compiler (Validation), Bot (Dynamic UI Generation)|

### 1.2 Technology Stack

* **Core Logic:** Python 3.10+
* **Bot Framework:** `discord.py` (v2.0+)
* **API Framework:** `FastAPI` + `Uvicorn`
* **Language Parsing:** `ANTLR4` (Python Target)
* **Database:** `SQLite` (File-based)
* **Frontend:** `React` (Vite) or `NextJS` usign + `HTML Textarea` (MVP) or `Monaco Editor` (P2)
* **Hosting:** Localhost (Primary Dev) / Render.com (Production)

## 2. Directory Structure

```text
/guildflow-project
├── /src
│   ├── /antlr_build          # Generated by: antlr4 -Dlanguage=Python3 -visitor GuildFlow.g4
│   │   ├── GuildFlowLexer.py
│   │   ├── GuildFlowParser.py
│   │   └── GuildFlowVisitor.py
│   ├── /compiler
│   │   └── compiler.py       # Your Logic: Converts Parse Tree -> JSON
│   ├── /bot
│   │   ├── client.py         # The Discord Bot logic
│   │   └── actions.py        # Command Pattern (The actual implementation of BAN, SEND)
│   ├── /database
│   │   └── db.py             # SQLite connection & schema
│   └── main.py               # Entry Point: Runs FastAPI + Bot loop
├── /web                      # React Frontend (Vite)
│   ├── src/App.jsx
│   └── package.json
├── GuildFlow.g4              # The Grammar Definition
├── requirements.txt          # Python dependencies
└── Dockerfile                # Deployment config
```

## 3. Grammar rule

### 3.1 Rules Implementation

| Rule Name | Pseudo-Grammar | Purpose | Implementation Difficulty | Example | Related Modules |
|---|---|---|---|---|---|

| **Data Extraction**     | EXTRACT FIELD FROM input AS variable_name             | Parses data from the event for later use in actions or conditions. | ⭐⭐⭐ (High)                | `EXTRACT FIELD message.author.id AS user_id`                                  | Data Parser     |
| **Conditional Logic**   | IF condition { ... } ELSE { ... }                     | Allows branching execution based on runtime conditions.            | ⭐⭐⭐ (High)                | `IF user_role IS "member" { ACTION: WARN_USER }`                              | Logic Evaluator |
| **Variable Set** | SET user.strikes = user.strikes + 1 | Persisting data (Memory).         | ⭐⭐⭐ (High) |

### 3.2 Example

``` g4
grammar GuildFlow;

// --- ENTRY POINT ---
prog: definition+ EOF;

definition
    : workflow_def
    | state_def
    ;

// --- WORKFLOW DEFINITIONS ---
workflow_def
    : 'WORKFLOW' ID 'ON' event_type ('WHERE' condition)? '{' statement* '}'
    ;

event_type: 'message' | 'member_join';

// --- STATEMENTS ---
statement
    : action_statement
    | if_statement
    | set_statement
    ;

// --- ACTIONS (The "What") ---
action_statement: 'ACTION:' action_command;

action_command
    : 'SEND_MESSAGE' 'channel' '=' ID 'content' '=' STRING
    | 'REPLY_MESSAGE' 'content' '=' STRING
    | 'ADD_ROLE' 'role' '=' STRING
    | 'BAN_USER'
    | 'TIMEOUT_USER' 'duration' '=' STRING
    ;

// --- LOGIC (The "How") ---
if_statement: 'IF' condition '{' statement* '}' ('ELSE' '{' statement* '}')?;

set_statement: 'SET' ID '=' expr;

// --- EXPRESSIONS ---
condition: expr comparator expr;
expr: ID | INT | STRING | 'user.strikes';
comparator: '==' | '!=' | 'contains' | '>=' | '<=';

// --- LEXER TOKENS ---
ID: [a-zA-Z_][a-zA-Z0-9_]*;
INT: [0-9]+;
STRING: '"' .*? '"';
WS: [ \t\r\n]+ -> skip;
```

## 4. Implementation Details

### 4.1 The Compiler (Visitor Pattern)

Goal: Transform the complex ANTLR tree into a simple dictionary.

File: `src/compiler/compiler.py`

```python
from antlr_build.GuildFlowVisitor import GuildFlowVisitor

class GuildFlowCompiler(GuildFlowVisitor):
    def visitWorkflow_def(self, ctx):
        return {
            "type": "WORKFLOW",
            "name": ctx.ID().getText(),
            "trigger": ctx.event_type().getText(),
            # Recursively visit children to get actions
            "actions": [self.visit(child) for child in ctx.statement()]
        }

    def visitAction_statement(self, ctx):
        # Simplified example
        cmd = ctx.action_command()
        return {
            "type": "ACTION",
            "command": cmd.start.text, # e.g., 'SEND_MESSAGE'
            "params": self._extract_params(cmd)
        }
```

## 5. Developer Setup (Localhost)

Use this method for development and the final demo if cloud deployment fails.

Prerequisites:

1. Python 3.10+ installed.
2. Node.js installed (for Frontend).
3. Discord Bot Token (with Message Content Intent enabled).
