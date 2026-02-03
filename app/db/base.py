# 這裡導入所有模型，以便於 Alembic 偵測
from app.db.base_class import Base
from app.models.user import User
from app.models.order import Order

# 如果有其他模型，也要一併在這裡 import
