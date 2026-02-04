from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.repositories.base import BaseRepository
from app.models.order import Order
from app.models.order_status import OrderStatus

class OrderRepository(BaseRepository[Order]):
    def __init__(self, db: AsyncSession):
        super().__init__(Order, db)

    async def get_by_id(self, order_id: str) -> Optional[Order]:
        return await self.get(order_id)

    async def get_order_status(self, order_id: str, status_code: str = '1') -> Optional[OrderStatus]:
        # OrderStatus logic might belong to a separate repository depending on strictness,
        # but often Order and its Status are aggregate.
        # Alternatively, create OrderStatusRepository.
        # For now, putting it here as a helper method since the Service needs both.
        # Or I can use a separate OrderStatusRepository. 
        # Let's check complexity. It's just one query.
        result = await self.db.execute(
            select(OrderStatus).where(
                OrderStatus.order_id == order_id, 
                OrderStatus.status == status_code
            )
        )
        return result.scalar_one_or_none()
