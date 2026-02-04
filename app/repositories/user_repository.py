from typing import Optional
from sqlalchemy.future import select
from app.repositories.base import BaseRepository
from app.models.user import User

class UserRepository(BaseRepository[User, str]):
    async def get_by_account(self, account: str) -> Optional[User]:
        query = select(self.model).where(self.model.account == account)
        result = await self.session.execute(query)
        return result.scalars().first()
