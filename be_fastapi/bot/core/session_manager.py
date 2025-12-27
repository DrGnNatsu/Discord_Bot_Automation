from app.db.session import SessionLocal
from app.models import ActiveSession, Workflow


def get_user_session(user_id):
    """
    Finds if the user is in ANY active workflow.
    """
    session = SessionLocal()
    try:
        # Since user_id is part of a composite key, filtering by it returns all sessions for that user.
        # For this bot, we assume a user focuses on one task at a time, so we take the first.
        return session.query(ActiveSession).filter(ActiveSession.user_id == str(user_id)).first()
    finally:
        session.close()


def create_or_update_session(user_id, workflow_name, next_state):
    """
    Resolves workflow_name -> workflow_id (UUID) and updates the session.
    """
    session = SessionLocal()
    try:
        # 1. Resolve Name to UUID
        # We need the UUID because ActiveSession.workflow_id is a ForeignKey
        target_flow = session.query(Workflow).filter(Workflow.name == workflow_name).first()

        if not target_flow:
            print(f"❌ Error: Workflow named '{workflow_name}' not found in DB.")
            return

        target_uuid = target_flow.id  # The generated UUID

        # 2. Check for existing session
        # We try to find a session for this user linked to this specific workflow
        active = session.query(ActiveSession).filter(
            ActiveSession.user_id == str(user_id),
            ActiveSession.workflow_id == target_uuid
        ).first()

        if active:
            active.current_state = next_state
        else:
            # 3. Handle Composite Key Insert
            # If the user was in a DIFFERENT workflow, we might want to clear it first
            # (depending on your logic). For now, we just add the new one.
            new_session = ActiveSession(
                user_id=str(user_id),
                workflow_id=target_uuid,  # UUID
                current_state=next_state
            )
            session.add(new_session)

        session.commit()
        print(f"💾 Session Saved: {user_id} -> {workflow_name} (State: {next_state})")

    except Exception as e:
        print(f"🔥 Session DB Error: {e}")
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
