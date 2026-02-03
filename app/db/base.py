# 這裡導入所有模型，以便於 Alembic 偵測
from app.db.base_class import Base
from app.models.user import User
from app.models.order import Order
from app.models.order_detail import OrderDetail
from app.models.store import Store
from app.models.permission import Permission, Role
from app.models.ifcontrl import IfContrl

# 未來新增模型請持續在此註冊
