from sqlalchemy.orm import Session
from app.models.admin_user import AdminUser
from app.enums.role import Role
from app.schemas.register import RegisterCreateUserDTO

class UserRepository:
    def get_user_by_email(self, email: str, db: Session) -> AdminUser | None:
        return db.query(AdminUser).filter(AdminUser.username == email).first()

    def create_user(self, data: RegisterCreateUserDTO, db: Session) -> AdminUser:
        user = AdminUser(
            username=str(data.email),
            password_hash=data.password,
            role=Role.admin
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
