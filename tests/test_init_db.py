import pytest
from sqlalchemy.future import select
from app.db.init_db import init_db
from app.db.session import SessionLocal
from app.models.user import User
from app.models.auth_tables import Role, Permission

@pytest.mark.asyncio
async def test_init_db():
    async with SessionLocal() as db:
        # Run initialization
        await init_db(db)
        
        # Verify Superuser
        result = await db.execute(select(User).where(User.account == "kahap"))
        superuser = result.scalar_one_or_none()
        assert superuser is not None, "Superuser 'kahap' should exist"
        
        # Verify Roles
        result = await db.execute(select(Role))
        roles = result.scalars().all()
        assert len(roles) > 0, "Roles should be created"
        role_names = [r.name for r in roles]
        assert "Developer" in role_names
        assert "Admin" in role_names
        
        # Verify Permissions
        result = await db.execute(select(Permission))
        permissions = result.scalars().all()
        assert len(permissions) > 0, "Permissions should be created"
        
        # Check specific permission
        result = await db.execute(select(Permission).where(Permission.name == "order.list"))
        perm = result.scalar_one_or_none()
        assert perm is not None, "Permission 'order.list' should exist"
