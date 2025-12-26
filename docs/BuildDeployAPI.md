It seems we have hit a bottleneck. If Member A is struggling with the ANTLR Visitor logic, we should **bypass the complex parsing temporarily** to get the API working.

We will switch to a **"Mock Compiler" Strategy**. This allows us to finish the API, connect to the database, and verify the Frontend integration *without* waiting for the complex language parser to be perfect.

Here is the modified task for **Member A** to complete immediately.

---

# 📅 Member A: Emergency Task - Mock API Integration

### **Objective**

Build the `POST /deploy` endpoint using **Fake Data**. instead of actually parsing the text, the backend will return a pre-defined JSON object. This proves the API works and saves data to the database, unblocking the Frontend Developer.

### 🛠️ Step 1: Create the "Mock" Compiler

Instead of the complex ANTLR Visitor, use this simple function. It guarantees a valid output so you can test the database connection.

**File:** `src/compiler/fake_compiler.py` (Replace existing content)

```python
# MOCK VERSION - Use this to get the API working immediately
import json

class GuildFlowCompiler:
    def visit(self, tree):
        """
        Ignores the actual input tree and returns FAKE data 
        to test the API and Database connection.
        """
        print("⚠️ WARNING: Using Mock Compiler")
        
        # This matches the schema Member B built
        return [
            {
                "type": "WORKFLOW",
                "name": "mock_workflow", # We will overwrite this with the real name in main.py
                "trigger": "message",
                "filter": None,
                "actions": [
                    {
                        "type": "ACTION",
                        "command": "SEND_MESSAGE",
                        "params": {
                            "channel": "general",
                            "content": "This is a fake response from the API"
                        }
                    }
                ]
            }
        ]

```

---

### 🛠️ Step 2: The API Implementation

This code is robust. It accepts the request, uses the mock compiler, and saves to SQLite.

**File:** `src/main.py`

```python
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from src.database.db import get_db, engine, Base
from src.database.models import Workflow
# Import the MOCK compiler
from src.compiler.compiler import GuildFlowCompiler

# Initialize DB
Base.metadata.create_all(bind=engine)

app = FastAPI()

class DeployRequest(BaseModel):
    workflow_name: str
    script_content: str
    admin_id: str

@app.post("/api/deploy")
async def deploy_workflow(payload: DeployRequest, db: Session = Depends(get_db)):
    print(f"🚀 Receiving Deployment: {payload.workflow_name}")

    try:
        # 1. SKIP Parsing (Mock Mode)
        # We don't use ANTLR here to avoid errors.
        tree = None 

        # 2. Get Fake Data
        compiler = GuildFlowCompiler()
        compiled_data = compiler.visit(tree)

        # 3. Find the Workflow Object in the fake data
        workflow_json = compiled_data[0]
        
        # 4. Save to Database (Real Logic)
        # Check if exists
        existing = db.query(Workflow).filter(Workflow.name == payload.workflow_name).first()
        
        if existing:
            existing.source_code = payload.script_content
            existing.compiled_json = workflow_json
            print(f"✅ Updated: {payload.workflow_name}")
        else:
            new_flow = Workflow(
                name=payload.workflow_name,
                trigger_event="message", # Hardcoded for now
                source_code=payload.script_content,
                compiled_json=workflow_json
            )
            db.add(new_flow)
            print(f"✨ Created: {payload.workflow_name}")
        
        db.commit()

        return {
            "status": "success",
            "message": "Deployment Successful (MOCK MODE)",
            "data": workflow_json
        }

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

```

---

### 🧪 Input & Expected Output

Member A must verify the task using these exact values.

#### **1. The Input (Request)**

Send this JSON to `POST http://localhost:8000/api/deploy`.

```json
{
    "workflow_name": "demo_test",
    "admin_id": "admin_1",
    "script_content": "This text does not matter because we are using fake data."
}

```

#### **2. The Expected Output (Response)**

If the API is working, you will receive this **200 OK** response.

```json
{
    "status": "success",
    "message": "Deployment Successful (MOCK MODE)",
    "data": {
        "type": "WORKFLOW",
        "name": "mock_workflow",
        "trigger": "message",
        "filter": null,
        "actions": [
            {
                "type": "ACTION",
                "command": "SEND_MESSAGE",
                "params": {
                    "channel": "general",
                    "content": "This is a fake response from the API"
                }
            }
        ]
    }
}

```

#### **3. Verification in Database**

After running the request, check the `guildflow.db` file.

* **Table:** `workflows`
* **Row:** Should see `demo_test` in the `name` column and the fake JSON in the `compiled_json` column.

**Why this helps:**
This allows the Frontend Developer to finish the "Deploy Button" logic *today* without waiting for Member A to fix the ANTLR bugs. Member A can swap the Mock Compiler for the Real Compiler later seamlessly.