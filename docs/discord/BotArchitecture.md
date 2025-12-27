# Discord Bot Architecture Documentation

This document explains the structure of the refactored Discord bot and the responsibility of each file. The new design uses **Discord.py Cogs** to separate functionality into modular components, making the codebase easier to maintain and extend.

## Directory Structure using Cogs

```text
bot/
├── client.py          # Entry point for FastAPI
├── core/
│   └── bot.py         # Custom Bot Class (The "Brain")
└── cogs/              # Features (The "Limbs")
    ├── automation.py  # Automation Logic
    └── general.py     # General Commands
```

## File Responsibilities

### 1. `bot/core/bot.py` (The Brain)

**Role:** The centralized Bot class.

- Inherits from `discord.ext.commands.Bot`.
- **Responsibilities**:
  - Configuring **Intents** (permissions to see messages, members, etc.).
  - Loading **Extensions (Cogs)** automatically in `setup_hook`
  - Handling startup events like `on_ready`
- **Why?** This keeps the configuration separate from the business logic.

### 2. `bot/cogs/automation.py`(Feature: Automation)

**Role:** A unified module for automation workflows.

- Inherits from `commands.Cog`.
- **Responsibilities**:
  - Listens to events (e.g., `on_message`)
  - Connects to the database (`SessionLocal`) to find and execute workflows.
  - Contains the actual business logic for the bot.
- **Why?** If you need to add a new trigger (e.g., `on_member_join`), you verify it here without breaking other parts of the bot.

### 3. `bot/cogs/general.py` (Feature: Utilities)

**Role:** A module for basic utility commands.

- **Responsibilities**:
  - Handles commands like `ping`, `help`, or `info`.
- **Why?** Keeps the "heavy" automation logic checks separate from simple commands.

### 4. `bot/client.py` (The Bridge)

**Role:** The entry point used by external apps (like FastAPI).

- **Responsibilities**:
  - Exposes a function `get_discord_client()` that returns an instance of our custom `DiscordBot`.
- **Why?** FastAPI doesn't need to know *how* the bot is built, it just needs to get the instance. This acts as an adapter.

### 5. `app/main.py` (The Integration)

**Role:** The main web server file.

- **Responsibilities**:
  - Uses the `lifespan` context manager.
  - Starts the bot task (`asyncio.create_task(bot.start(...))`) when the server starts.
  - Properly closes the bot connection when the server stops.
