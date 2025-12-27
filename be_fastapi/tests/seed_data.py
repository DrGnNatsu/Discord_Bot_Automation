from app.db.session import SessionLocal
from app.models import Workflow

db = SessionLocal()
try:
    # Check if exists first to avoid duplicates
    existing = db.query(Workflow).filter_by(name='test_flow').first()
    if not existing:
        dummy_rule = Workflow(
            name='test_flow',
            trigger_event='message',
            source_code='test source',
            compiled_json={"type": "TEST_RESPONSE", "content": "Hello World"}
        )
        db.add(dummy_rule)
        db.commit()
        print("✅ Dummy rule inserted.")
    else:
        print("ℹ️ Dummy rule already exists.")
finally:
    db.close()

session = SessionLocal()

# 1. Define the Logic JSON
logic_rule = {
    "trigger": "message",
    "actions": [
        {
            "type": "LOGIC_IF",
            "condition": {
                "left": "message.content",
                "operator": "contains",
                "right": "secret"
            },
            "body": [
                {
                    "type": "ACTION",
                    "command": "REPLY_MESSAGE",
                    "params": {
                        "content": "🤫 You found the secret logic path!"
                    }
                }
            ],
            "else_body": []
        }
    ]
}

# 2. Insert into DB
try:
    # Check if exists
    existing = session.query(Workflow).filter_by(name="logic_test").first()
    if not existing:
        new_flow = Workflow(
            name='logic_test',
            trigger_event='message',
            source_code='test source',
            compiled_json=logic_rule  # SQLAlchemy handles JSON conversion usually
        )
        session.add(new_flow)
        session.commit()
        print("✅ injected 'logic_test' rule into database.")
    else:
        # Update existing for testing
        existing.compiled_json = logic_rule
        session.commit()
        print("🔄 Updated 'logic_test' rule.")

except Exception as e:
    print(f"❌ Error: {e}")
finally:
    session.close()

def seed_session_data():
    session = SessionLocal()
    print("🌱 Seeding Data (UUID Compatible)...")

    # --- 1. The Trigger Workflow ---
    # Name: 'report_flow'
    start_logic = {
        # 👇 CHANGE THIS from "!report" to "|report"
        "filter": { "left": "message.content", "operator": "==", "right": "|report" },
        "actions": [
            { "type": "ACTION", "command": "REPLY_MESSAGE", "params": { "content": "📝 Who to report?" } },
            { "type": "ACTION", "command": "ENTER_STATE", "params": { "target": "step_2_ban" } }
        ]
    }

    # --- 2. The Sub-Routine Workflow ---
    # Name: 'step_2_ban'
    step_2_logic = {
        "actions": [
            { "type": "ACTION", "command": "REPLY_MESSAGE", "params": { "content": "✅ Report logged via Session." } },
            { "type": "ACTION", "command": "EXIT_WORKFLOW", "params": {} }
        ]
    }

    try:
        # Helper to upsert (Insert or Update) based on Name
        def upsert_workflow(name, data, trigger="message"):
            existing = session.query(Workflow).filter_by(name=name).first()
            if not existing:
                # UUID is generated automatically by your model's default=generate_uuid
                new_flow = Workflow(
                    name=name,
                    trigger_event=trigger,
                    compiled_json=data,
                    source_code="Manual Seed",
                    is_active=True
                )
                session.add(new_flow)
                print(f"   ✅ Created '{name}'")
            else:
                existing.compiled_json = data
                print(f"   🔄 Updated '{name}'")

        upsert_workflow("report_flow", start_logic)
        upsert_workflow("step_2_ban", step_2_logic)

        # Insert/Update Row 2
        existing_step = session.query(Workflow).filter_by(name="step_2_ban").first()
        if not existing_step:
            session.add(Workflow(
                name="step_2_ban",
                # 👇 CHANGE THIS from "message" to "manual" (or "state")
                trigger_event="manual",
                source_code="Manual Seed",
                compiled_json=step_2_logic,
                is_active=True
            ))
            print("   ✅ Created 'step_2_ban'")
        else:
            # Update existing rows too
            existing_step.trigger_event = "manual"  # <--- FORCE UPDATE THIS
            existing_step.compiled_json = step_2_logic
            print("   🔄 Updated 'step_2_ban'")

        session.commit()

    except Exception as e:
        print(f"❌ Error: {e}")
        session.rollback()
    finally:
        session.close()

seed_session_data()