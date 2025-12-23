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

##### 1.1.1.1 User Work Flow

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

##### 1.1.1.2 User Associated Grammar Rules (Runtime)

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

##### 1.1.2.1 Admin Work Flow

1. Input:
    - Source: Admin types code in the Monaco Editor (Web UI).
    - Raw Text String from Monaco Editor: `WORKFLOW demo ON message { ACTION: BAN_USER }`
    - Action: Admin clicks the "Deploy" button.
    - Payload: The React Frontend sends a POST request to the backend:

    ```JSON
    {
        "admin_id": "847382...",
        "script_content": "WORKFLOW anti_spam..."
    }
    ```

    - Context: The User's current state from the database (e.g., state="awaiting_reason").
2. Logic (The "Tree Walker"): This logic happens inside your Python Backend (main.py), which runs both `FastAPI (API)` and `discord.py (Bot)`.
    - Step A: The Compiler (Visitor Pattern):
        1. The FastAPI Endpoint receives the text.
        2. It invokes the GuildFlowParser to generate the Parse Tree.
        3. It calls compiler.visit(tree).
        4. **Validation**: If the Visitor finds a syntax error, it throws an exception. FastAPI catches this and returns a `400 Error` to the Web UI (e.g., "Error at line 3: Missing '}'").
        5. **Success**: If valid, the Visitor returns the JSON Object.
    - Step B: The Persistence:
        1. The JSON is saved to the SQLite workflows table.
        2. Crucial: The bot's internal memory cache is updated so it doesn't need to read the DB for the very next message.
    - Step C: The Notification (The Missing Link)
        1. The API retrieves the running Bot Instance.
        2. It looks up the configured #mod-logs channel ID.
        3. It triggers a background task: `await bot.get_channel(log_channel_id).send(...)`.
3. Output:
    - Output 1 (To Database): The logic file is updated.
    - Output 2 (To Web UI): A `200 OK response`. The admin sees a green `"Success"` toast on the website.
    - Output 3 (To Discord):
        - Channel: `#mod-logs`
        - Message: "✅ Deployment Successful: Workflow anti_spam updated by Admin."
        - Why this matters: This confirms to the admin (and other mods) that the code is actually live on the server.

##### 1.1.2.2 Admin Associated Grammar Rules (Runtime)

| Rule Name | Pseudo-Grammar | Purpose | Implementation Difficulty | Example | Related Modules |
|---|---|---|---|---|---|
| **Program Definition** (P1) | definition+ EOF | The Root. The entry point for the parser. Validates that the file contains at least one valid definition | ⭐ (Low) | (The entire file content) | Compiler (visitProg), Web UI (Validation) |
| **Workflow Definition** (P1) | WORKFLOW name ON event { ... } | Defines the entry point for an automated process. | ⭐ (Low) | `WORKFLOW monitor_spam ON message { ... }` | Core Engine |
| **State Definition** (P2) | 'STATE' ID '{' stmt* '}' | The Sub-Routine. Defines a discrete step in a multi-step process. Compiles into a separate JSON block. | ⭐ (Low) | `STATE welcome_step_2 { ... }` | Compiler (visitState_def), DB |
| **Components Program** (P2) |'COMPONENTS:' '[' button... '] | The UI Builder. Defines interactive elements (Buttons) attached to a message. Essential for the "Interactive" requirement | ⭐⭐⭐ (High) Must map strings to Discord UI Objects.| `COMPONENTS: [ BUTTON "Yes" -> transition_to(next) ]` | Compiler (Validation), Bot (Dynamic UI Generation)|

#### 1.1.3 Example of Grammar Rule

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

### 1.2 Technology Stack

- **Core Logic:** Python 3.10+
- **Bot Framework:** `discord.py` (v2.0+)
- **API Framework:** `FastAPI` + `Uvicorn`
- **Language Parsing:** `ANTLR4` (Python Target)
- **Database:** `SQLite` (File-based)
- **Frontend:** `React` (Vite) or `NextJS` usign + `HTML Textarea` (MVP) or `Monaco Editor` (P2)
- **Hosting:** Localhost (Primary Dev) / Render.com (Production)

### 1.3 Database Schema

```SQL
-- 1. THE LOGIC TABLE (Read-Mostly)
-- Stores the compiled instructions generated by the Admin Website.
CREATE TABLE IF NOT EXISTS workflows (
    workflow_id TEXT PRIMARY KEY,   -- The name defined in DSL: 'WORKFLOW my_flow ...'
    trigger_event TEXT NOT NULL,    -- 'message', 'member_join', 'button_click'
    trigger_filter TEXT,            -- Optional: The compiled WHERE clause (e.g. "content contains '!help'")
    compiled_json TEXT NOT NULL,    -- The huge JSON output from your Visitor/Compiler
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT 1     -- Allows 'Soft Delete' / Disabling without deleting data
);

-- Index for Speed: The Bot queries this EVERY time a message comes in.
CREATE INDEX idx_trigger ON workflows(trigger_event);


-- 2. THE CONTEXT TABLE (Read-Write)
-- Stores the "Memory" of every user currently interacting with the bot.
CREATE TABLE IF NOT EXISTS active_sessions (
    user_id TEXT NOT NULL,          -- Discord User ID (String)
    workflow_id TEXT NOT NULL,      -- Link to the workflow they are in
    current_state TEXT NOT NULL,    -- 'start', 'awaiting_reason', 'step_2'
    variables JSON DEFAULT '{}',    -- Dynamic storage: {"strikes": 1, "reason": "spam"}
    last_updated DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    -- Composite Primary Key: A user can only be in ONE instance of a specific workflow at a time.
    PRIMARY KEY (user_id, workflow_id),
    FOREIGN KEY (workflow_id) REFERENCES workflows(workflow_id) ON DELETE CASCADE
);
```

#### Table 1: `workflows`

1. Meaning:
    - Represents the **Instruction Manual** containing the static rules of the server.
    - Stores compiled workflow JSON so parsing is not repeated.
    - Represents **Flow 2 (Admin Deployment) output**.
2. Code Usage
    - Compiler (Flow 2 - Write)

        ```SQL
        INSERT OR REPLACE INTO workflows (workflow_id, trigger_event, compiled_json)
        VALUES (...);
        ```

    - Bot (Flow 1 - Read)

        ```SQL
        SELECT * FROM workflows WHERE trigger_event = 'message';
        ```

3. Optimization: Loaded into RAM dictionary cache on startup to avoid disk I/O.

#### Table 2: `active_sessions`

1. Meaning
    - Represents **Short-Term Memory**.
    - Tracks per-user Finite State Machine progression (multi-step workflows).
    - Handles different states for different users simultaneously.
2. Code Usage
    - Bot (Flow 1 - Read)

        ```SQL
        SELECT current_state FROM active_sessions WHERE user_id = '123';
        ```

    - Bot (Flow 1 - Write)
        - State Transition:

            ```SQL
            UPDATE active_sessions SET current_state = 'next_step' WHERE user_id = '123';
            ```

        - Variable Update:

            ```SQL
            UPDATE active_sessions SET variables = '{"strikes": 2}' WHERE user_id = '123';'123';
            ```

        - Workflow Completion:

            ```SQL
            DELETE FROM active_sessions WHERE user_id = '123';
            ```

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



## 3. Implementation Details

### 3.1 The Compiler (Visitor Pattern)

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

## 4. Developer Setup (Localhost)

Use this method for development and the final demo if cloud deployment fails.

Prerequisites:

1. Python 3.10+ installed.
2. Node.js installed (for Frontend).
3. Discord Bot Token (with Message Content Intent enabled).
