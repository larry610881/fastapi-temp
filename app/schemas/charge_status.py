from typing import Optional, Dict, Any, Union
from pydantic import BaseModel, Field

class ChargeStatusResponse(BaseModel):
    success: bool = Field(..., description="Whether the status check transaction was successful (communication-wise)")
    # For payment status, we might need another field, but usually 'success' implies the API call worked.
    # The actual payment status (paid/unpaid) is in 'data'.
    
    order_id: str
    gateway: str = Field(..., description="Payment gateway (ICP, OP, CTBC)")
    
    raw_response: Optional[str] = Field(None, description="Raw response text from the gateway")
    data: Optional[Dict[str, Any]] = Field(None, description="Parsed data from the response")
    error: Optional[str] = Field(None, description="Error message if any")

    class Config:
        from_attributes = True
