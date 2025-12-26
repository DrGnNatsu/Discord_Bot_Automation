from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.workflow import Workflow
# Import the MOCK compiler
from app.compiler.fake_compiler import GuildFlowCompiler

router = APIRouter()

from app.schemas.deploy import DeployRequest, DeploymentResponse

@router.post("/deploy", response_model=DeploymentResponse)
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
