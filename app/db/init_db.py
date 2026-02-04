import logging
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.auth_tables import Permission, Role
from app.models.user import User
from app.core.config import settings
from app.core.security import get_password_hash

logger = logging.getLogger(__name__)

# 權限定義 (從 PermissionSeeder.php 遷移)
# ... (保持原有的 PERMISSIONS_DATA 字典內容不變)
# 為了避免重複代碼，我這裡會完整重寫包含了之前定義的所有數據
PERMISSIONS_DATA = {
    '*': {
        'subject': '所有權限',
        'pid': None,
        'sort': 0,
        'description': '擁有此權限表示有下列所有權限。'
    },
    'order.*': {
        'subject': '訂單管理',
        'pid': '*',
        'sort': 1,
        'description': '擁有此權限表示有「查看訂單」、「查看訂單詳情的完整內容」、「訂單退貨」、「訂單模擬付款完成」的所有權限。'
    },
    'order.list': {
        'subject': '查看訂單',
        'pid': 'order.*',
        'sort': 1,
        'description': '擁有此權限表示可以查看訂單管理頁面。'
    },
    'order.listAdvanced': {
        'subject': '查看訂單詳情的完整內容',
        'pid': 'order.*',
        'sort': 2,
        'description': '擁有此權限表示可以查看「訂單詳情」彈出視窗內顯示的完整內容，完整內容包含訂單總金額的計算過程與商品的折扣狀態。'
    },
    'order.return': {
        'subject': '訂單退貨',
        'pid': 'order.*',
        'sort': 3,
        'description': '擁有此權限表示可以將訂單做退貨處理。'
    },
    'order.simulationPaymentCompleted': {
        'subject': '訂單模擬付款完成',
        'pid': 'order.*',
        'sort': 4,
        'description': '擁有此權限表示可以模擬訂單付款完成。注：模擬付款完成會讓系統判定訂單真的已經完成付款。'
    },
    'accountancy.*': {
        'subject': '請撥款與差異資料',
        'pid': '*',
        'sort': 2,
        'description': '擁有此權限表示有「查看請款資料」、「查看撥款資料」、「查看差異資料」的所有權限'
    },
    'accountancy.take': {
        'subject': '查看請款資料',
        'pid': 'accountancy.*',
        'sort': 1,
        'description': '擁有此權限表示有查看請款資料的權限。'
    },
    'accountancy.give': {
        'subject': '查看撥款資料',
        'pid': 'accountancy.*',
        'sort': 2,
        'description': '擁有此權限表示有查看撥款資料的權限。'
    },
    'accountancy.diff': {
        'subject': '查看差異資料',
        'pid': 'accountancy.*',
        'sort': 3,
        'description': '擁有此權限表示有查看差異資料的權限。'
    },
    'system.*': {
        'subject': '系統設定',
        'pid': '*',
        'sort': 3,
        'description': '擁有此權限表示有「帳號管理」、「權限組管理」、「系統訊息管理」、「系統日誌」、「任務管理」的所有權限。'
    },
    'system.page.*': {
        'subject': '消費者端文案管理',
        'pid': 'system.*',
        'sort': 1,
        'description': '擁有此權限表示有「查看消費者端文案列表」、「新增消費者端文案」、「編輯消費者端文案」的權限。'
    },
    'system.page.list': {
        'subject': '查看消費者端文案列表',
        'pid': 'system.page.*',
        'sort': 1,
        'description': '擁有此權限表示有查看消費者端文案列表的權限。'
    },
    'system.page.create': {
        'subject': '新增消費者端文案',
        'pid': 'system.page.*',
        'sort': 2,
        'description': '擁有此權限表示有新增消費者端文案的權限。(此權限應該只提供給工程師)'
    },
    'system.page.edit': {
        'subject': '編輯消費者端文案',
        'pid': 'system.page.*',
        'sort': 3,
        'description': '擁有此權限表示有編輯消費者端文案的權限。'
    },
    'system.maintenanceMode.*': {
        'subject': '消費者端維護模式管理',
        'pid': 'system.*',
        'sort': 2,
        'description': '擁有此權限表示有 的權限。'
    },
    'system.maintenanceMode.check': {
        'subject': '查看目前消費者端維護模式狀態',
        'pid': 'system.maintenanceMode.*',
        'sort': 1,
        'description': '擁有此權限表示有查看目前消費者端維護模式狀態的權限。'
    },
    'system.maintenanceMode.toggle': {
        'subject': '切換目前消費者端維護模式狀態',
        'pid': 'system.maintenanceMode.*',
        'sort': 2,
        'description': '擁有此權限表示有切換目前消費者端維護模式狀態的權限。'
    },
    'system.account.*': {
        'subject': '帳號管理',
        'pid': 'system.*',
        'sort': 3,
        'description': '擁有此權限表示有新增帳號、修改帳號基本資料、修改帳號權限、刪除帳號、查看帳號的權限。'
    },
    'system.account.list': {
        'subject': '查看帳號',
        'pid': 'system.account.*',
        'sort': 1,
        'description': '擁有此權限表示有查看系統上所有帳號列表的權限。'
    },
    'system.account.create': {
        'subject': '新增帳號',
        'pid': 'system.account.*',
        'sort': 2,
        'description': '擁有此權限表示有新增帳號的權限。'
    },
    'system.account.edit.*': {
        'subject': '編輯帳號',
        'pid': 'system.account.*',
        'sort': 3,
        'description': '擁有此權限表示有編輯帳號「基本資料」與「權限」的權限。'
    },
    'system.account.edit.basic': {
        'subject': '編輯帳號基本資料',
        'pid': 'system.account.edit.*',
        'sort': 1,
        'description': '擁有此權限表示有編輯帳號的「帳號」、「密碼」、「權限組」、「擁有人姓名」、「帳號到期日」的權限。'
    },
    'system.account.edit.permission': {
        'subject': '編輯帳號權限設定',
        'pid': 'system.account.edit.*',
        'sort': 2,
        'description': '擁有此權限表示有編輯帳號的「權限」的權限。'
    },
    'system.account.delete': {
        'subject': '刪除帳號',
        'pid': 'system.account.*',
        'sort': 4,
        'description': '擁有此權限表示有刪除帳號的權限。'
    },
    'system.account.toggleDisable': {
        'subject': '切換帳號狀態',
        'pid': 'system.account.*',
        'sort': 5,
        'description': '擁有此權限表示有啟用或禁用帳號的權限。'
    },
    'system.role.*': {
        'subject': '權限組管理',
        'pid': 'system.*',
        'sort': 4,
        'description': '擁有此權限表示有權限組的「新增」、「修改基本資料」、「修改權限」、「刪除權限組」的權限。'
    },
    'system.role.list': {
        'subject': '查看權限組',
        'pid': 'system.role.*',
        'sort': 1,
        'description': '擁有此權限表示有查看權限組的權限。'
    },
    'system.role.create': {
        'subject': '新增權限組',
        'pid': 'system.role.*',
        'sort': 2,
        'description': '擁有此權限表示有新增權限組的權限。'
    },
    'system.role.edit.*': {
        'subject': '編輯權限組',
        'pid': 'system.role.*',
        'sort': 3,
        'description': '擁有此權限表示有編輯權限組的「基本資料」與「權限」的權限。'
    },
    'system.role.edit.basic': {
        'subject': '編輯權限組基本資料',
        'pid': 'system.role.edit.*',
        'sort': 1,
        'description': '擁有此權限表示有編輯權限組基本資料的權限。'
    },
    'system.role.edit.permission': {
        'subject': '編輯權限組包含的權限',
        'pid': 'system.role.edit.*',
        'sort': 2,
        'description': '擁有此權限表示有編輯權限組「包含的權限」的權限。'
    },
    'system.role.delete': {
        'subject': '刪除權限組',
        'pid': 'system.role.*',
        'sort': 4,
        'description': '擁有此權限表示有刪除權限組的權限。'
    },
    'system.task.*': {
        'subject': '任務排程',
        'pid': 'system.*',
        'sort': 5,
        'description': '擁有此權限表示有「查看任務排程」、「查看任務排程的詳細資訊」、「新增任務排程」、「編輯任務排程」、「刪除任務排程」、「切換任務排程的啟用或禁用」、「手動執行任務排程」的權限。'
    },
    'system.task.list': {
        'subject': '查看任務排程',
        'pid': 'system.task.*',
        'sort': 1,
        'description': '擁有此權限表示有查看任務排程列表的權限。'
    },
    'system.task.listDetail': {
        'subject': '查看任務排程的詳細資訊',
        'pid': 'system.task.*',
        'sort': 2,
        'description': '擁有此權限表示有查看任務排程的詳細資訊的權限。'
    },
    'system.task.create': {
        'subject': '新增任務排程',
        'pid': 'system.task.*',
        'sort': 3,
        'description': '擁有此權限表示有新增任務排程的權限。'
    },
    'system.task.edit': {
        'subject': '編輯任務排程',
        'pid': 'system.task.*',
        'sort': 4,
        'description': '擁有此權限表示有編輯任務排程的權限。'
    },
    'system.task.delete': {
        'subject': '刪除任務排程',
        'pid': 'system.task.*',
        'sort': 5,
        'description': '擁有此權限表示有刪除任務排程的權限。'
    },
    'system.task.toggle': {
        'subject': '切換任務排程的啟用或禁用',
        'pid': 'system.task.*',
        'sort': 6,
        'description': '擁有此權限表示有啟用或禁用任務排程的權限。'
    },
    'system.task.manual': {
        'subject': '手動執行任務排程',
        'pid': 'system.task.*',
        'sort': 7,
        'description': '擁有此權限表示有手動執行任務排程的權限。'
    },
    'system.log.*': {
        'subject': '系統日誌',
        'pid': 'system.*',
        'sort': 4,
        'description': '擁有此權限表示有查看系統日誌、搜尋系統日誌、清除系統日誌的權限。'
    },
    'system.log.list': {
        'subject': '查看系統日誌列表',
        'pid': 'system.log.*',
        'sort': 1,
        'description': '擁有此權限表示有查看系統日誌的權限。'
    },
    'system.log.info': {
        'subject': '查看系統日誌詳細資訊',
        'pid': 'system.log.*',
        'sort': 2,
        'description': '擁有此權限表示有查看系統日誌詳細資料的權限。'
    },
    'system.log.search': {
        'subject': '搜尋系統日誌',
        'pid': 'system.log.*',
        'sort': 3,
        'description': '擁有此權限表示有搜尋系統日誌的權限。'
    },
    'system.log.delete': {
        'subject': '清除系統日誌',
        'pid': 'system.log.*',
        'sort': 4,
        'description': '擁有此權限表示有清除系統日誌的權限。'
    },
    'system.log.error.list': {
        'subject': '查看錯誤日誌列表',
        'pid': 'system.log.*',
        'sort': 5,
        'description': '擁有此權限表示有查看錯誤日誌的權限。'
    },
    'system.version': {
        'subject': '系統版本',
        'pid': 'system.*',
        'sort': 5,
        'description': '擁有此權限表示有查看系統版本號的權限。'
    },
    'store.*': {
        'subject': '商品主檔資料',
        'pid': '*',
        'sort': 4,
        'description': '擁有此權限表示有查看商品主檔資料的所有權限。'
    },
    'store.ifcontrl': {
        'subject': '查看 IFCONTRL 資料',
        'pid': 'store.*',
        'sort': 1,
        'description': '擁有此權限表示有查看 IFCONTRL 資料的權限。'
    },
    'store.see': {
        'subject': '查看商店資訊',
        'pid': 'store.*',
        'sort': 2,
        'description': '擁有此權限表示有查看 商店 資訊的權限。'
    },
    'store.create': {
        'subject': '新增商店',
        'pid': 'store.*',
        'sort': 3,
        'description': '擁有此權限表示有新增 商店 的權限。'
    },
    'store.edit': {
        'subject': '修改商店座標',
        'pid': 'store.*',
        'sort': 4,
        'description': '擁有此權限表示有修改 商店 座標資訊的權限。'
    },
    'store.delete': {
        'subject': '刪除商店',
        'pid': 'store.*',
        'sort': 5,
        'description': '擁有此權限表示有刪除 商店 資訊的權限。'
    },
    'selfAccount.password': {
        'subject': '個人帳號管理',
        'pid': '*',
        'sort': 4,
        'description': '擁有此權限表示有「自行修改自己帳號的密碼」權限。'
    },
    'system.gps.*': {
        'subject': '消費者端 GPS 定位管理',
        'pid': 'system.*',
        'sort': 6,
        'description': '擁有此權限表示有管理「消費者端 GPS 定位」的權限。'
    },
    'system.gps.setLocation': {
        'subject': '設定消費者端判定 GPS 定位的區間',
        'pid': 'system.gps.*',
        'sort': 1,
        'description': '擁有此權限表示有設定消費者端判定 GPS 定位的區間的權限。'
    },
    'system.gps.toggle': {
        'subject': '切換目前消費者端是否檢查 GPS 定位的狀態',
        'pid': 'system.gps.*',
        'sort': 2,
        'description': '擁有此權限表示有切換目前消費者端是否檢查 GPS 定位的狀態的權限。'
    },
    'system.gps.check': {
        'subject': '查看消費者端的 GPS 定位的設定狀態',
        'pid': 'system.gps.*',
        'sort': 3,
        'description': '擁有此權限表示有查看消費者端的 GPS 定位的設定狀態的權限。'
    }
}

ROLES_DATA = [
    ("Developer", "開發人員", ""),
    ("Admin", "系統管理員", ""),
    ("SalesPerson", "店員", ""),
    ("Accountant", "會計", ""),
    ("Maintain", "維運人員", ""),
]

SUPERUSER_DATA = {
    "account": "kahap",
    "password": "KAHAPkahapForX5Admin",
    "department": "巧禾數位設計股份有限公司 系統預設帳號",
    "owner_name": "初始帳號",
    "disabled": False,
    "logintimes": 0
}

async def init_permissions(db: AsyncSession):
    """初始化權限資料 (Async)"""
    logger.info("開始初始化權限...")
    
    pending_permissions = PERMISSIONS_DATA.copy()
    created_count = 0
    
    while pending_permissions:
        processed_keys = []
        progress_made = False
        
        for name, data in pending_permissions.items():
            # 檢查是否已存在
            result = await db.execute(select(Permission).where(Permission.name == name))
            existing = result.scalar_one_or_none()
            
            if existing:
                processed_keys.append(name)
                progress_made = True
                continue
            
            parent_id = None
            if data['pid']:
                # 嘗試查找父節點
                parent_result = await db.execute(select(Permission).where(Permission.name == data['pid']))
                parent = parent_result.scalar_one_or_none()
                
                if parent:
                    parent_id = parent.id
                else:
                    if data['pid'] not in pending_permissions and data['pid'] not in PERMISSIONS_DATA:
                        logger.warning(f"權限 {name} 的父節點 {data['pid']} 未定義，略過。")
                        processed_keys.append(name)
                    continue
            
            # 建立權限
            permission = Permission(
                id=str(uuid.uuid4()),
                name=name,
                guard_name='web',
                subject=data['subject'],
                description=data.get('description'),
                pid=parent_id,
                sort=data['sort']
            )
            db.add(permission)
            processed_keys.append(name)
            progress_made = True
            created_count += 1
        
        await db.commit()
        
        for key in processed_keys:
            if key in pending_permissions:
                del pending_permissions[key]
                
        if not progress_made and pending_permissions:
            logger.error(f"無法解析剩餘權限的依賴關係: {list(pending_permissions.keys())}")
            break
            
    logger.info(f"權限初始化完成，新增了 {created_count} 筆權限。")


async def init_roles(db: AsyncSession):
    """初始化角色資料 (Async)"""
    logger.info("開始初始化角色...")
    created_count = 0
    
    for role_data in ROLES_DATA:
        name, subject, store_id = role_data
        
        result = await db.execute(select(Role).where(Role.name == name))
        existing = result.scalar_one_or_none()
        
        if not existing:
            role = Role(
                id=str(uuid.uuid4()),
                name=name,
                guard_name='web',
                subject=subject,
                storeId=store_id if store_id else None
            )
            db.add(role)
            created_count += 1
            
    await db.commit()
    logger.info(f"角色初始化完成，新增了 {created_count} 筆角色。")


async def init_superuser(db: AsyncSession):
    """初始化超級管理員 (Async)"""
    logger.info("開始檢查超級管理員帳號...")
    
    account = SUPERUSER_DATA["account"]
    result = await db.execute(select(User).where(User.account == account))
    existing_user = result.scalar_one_or_none()
    
    if not existing_user:
        logger.info(f"建立初始超級管理員: {account}")
        
        user = User(
            uuid=str(uuid.uuid4()),
            account=account,
            password=get_password_hash(SUPERUSER_DATA["password"]),
            department=SUPERUSER_DATA["department"],
            owner_name=SUPERUSER_DATA["owner_name"],
            disabled=SUPERUSER_DATA["disabled"],
            logintimes=SUPERUSER_DATA["logintimes"]
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        logger.info("超級管理員建立完成。")
    else:
        logger.info("超級管理員帳號已存在，略過。")


async def init_db(db: AsyncSession) -> None:
    """初始化資料庫主入口 (Async)"""
    await init_permissions(db)
    await init_roles(db)
    await init_superuser(db)
