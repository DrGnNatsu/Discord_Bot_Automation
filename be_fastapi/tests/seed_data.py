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
