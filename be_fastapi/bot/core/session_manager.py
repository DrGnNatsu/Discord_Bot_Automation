from datetime import datetime, timedelta
from sqlalchemy.orm.attributes import flag_modified
from app.db.session import SessionLocal
from app.models import ActiveSession, Workflow


def get_user_session(user_id):
    """
    Finds if the user is in ANY active workflow.
    Auto-deletes sessions older than 15 minutes.
    """
    session = SessionLocal()
    try:
        # Since user_id is part of a composite key, filtering by it returns all sessions for that user.
        # For this bot, we assume a user focuses on one task at a time, so we take the first.
        active = session.query(ActiveSession).filter(ActiveSession.user_id == str(user_id)).first()

        if active:
            # Handle potential None for last_updated if it wasn't set on creation
            last_active = active.last_updated
            if last_active:
                # Convert active.last_updated to naive UTC if it has timezone
                last_active_naive = last_active.replace(tzinfo=None) if last_active.tzinfo else last_active
                
                # Check 15 minute timeout
                time_diff = datetime.utcnow() - last_active_naive
                if time_diff > timedelta(minutes=15):
                    print(f"🧹 [INFO] Session timed out for {user_id}")
                    session.delete(active)
                    session.commit()
                    return None
        
        return active
    finally:
        session.close()


def create_or_update_session(user_id, workflow_name, next_state, new_data=None):
    """
    Resolves workflow_name -> workflow_id (UUID) and updates the session.
    Also merges new_data into variables if provided.
    """
    session = SessionLocal()
    try:
        # 1. Resolve Name to UUID
        target_flow = session.query(Workflow).filter(Workflow.name == workflow_name).first()

        if not target_flow:
            print(f"❌ [ERROR] Workflow named '{workflow_name}' not found in DB.")
            return

        target_uuid = target_flow.id  # The generated UUID

        # 2. Check for existing session
        active = session.query(ActiveSession).filter(
            ActiveSession.user_id == str(user_id),
            ActiveSession.workflow_id == target_uuid
        ).first()

        if active:
            active.current_state = next_state
            # Merge variables
            if new_data:
                current_vars = active.variables or {}
                if isinstance(current_vars, dict):
                    current_vars.update(new_data)
                else:
                    current_vars = new_data # Fallback
                
                active.variables = current_vars
                flag_modified(active, "variables") # Ensure JSON update is tracked
            
            # Explicitly touch last_updated
            active.last_updated = datetime.now() 

        else:
            # 3. Create new session
            new_session = ActiveSession(
                user_id=str(user_id),
                workflow_id=target_uuid,  # UUID
                current_state=next_state,
                variables=new_data or {},
                last_updated=datetime.now()
            )
            session.add(new_session)

        session.commit()
        print(f"💾 [STATE] Session Saved: {user_id} -> {workflow_name} (State: {next_state})")

    except Exception as e:
        print(f"🔥 [ERROR] Session DB Error: {e}")
        session.rollback()
    finally:
        session.close()


def delete_session(user_id):
    """
    Deletes ALL active sessions for this user.
    """
    session = SessionLocal()
    try:
        session.query(ActiveSession).filter(ActiveSession.user_id == str(user_id)).delete()
        session.commit()
    finally:
        session.close()

def clear_all_sessions():
    """
    Nuclear option: Deletes ALL active sessions in the database.
    """
    session = SessionLocal()
    try:
        rows = session.query(ActiveSession).delete()
        session.commit()
        return rows
    finally:
        session.close()
