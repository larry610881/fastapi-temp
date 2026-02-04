from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.repositories.base import BaseRepository
from app.models.order_status import OrderStatus


class OrderStatusRepository(BaseRepository[OrderStatus]):
    """訂單狀態資料存取層"""
    
    def __init__(self, db: AsyncSession):
        super().__init__(OrderStatus, db)

    async def get_by_order_id(self, order_id: str, status_code: str = '1') -> Optional[OrderStatus]:
        """
        根據訂單編號與狀態碼取得訂單狀態
        
        Args:
            order_id: 訂單編號
            status_code: 狀態碼 (預設 '1')
            
        Returns:
            OrderStatus 或 None
        """
        result = await self.db.execute(
            select(OrderStatus).where(
                OrderStatus.order_id == order_id, 
                OrderStatus.status == status_code
            )
        )
        return result.scalar_one_or_none()
