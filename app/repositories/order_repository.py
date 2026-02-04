from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.base import BaseRepository
from app.models.order import Order


class OrderRepository(BaseRepository[Order]):
    """訂單資料存取層"""
    
    def __init__(self, db: AsyncSession):
        super().__init__(Order, db)

    async def get_by_id(self, order_id: str) -> Optional[Order]:
        """根據訂單編號取得訂單"""
        return await self.get(order_id)
