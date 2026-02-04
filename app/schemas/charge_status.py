"""
訂單狀態反查回應 Schema
"""
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict


class ChargeStatusResponse(BaseModel):
    """訂單狀態反查回應"""
    
    model_config = ConfigDict(from_attributes=True)
    
    success: bool = Field(..., description="API 呼叫是否成功")
    order_id: str = Field(..., description="訂單編號")
    gateway: str = Field(..., description="金流閘道 (ICP, OP, CTBC)")
    raw_response: Optional[str] = Field(None, description="閘道原始回應")
    data: Optional[Dict[str, Any]] = Field(None, description="解析後的資料")
    error: Optional[str] = Field(None, description="錯誤訊息")
