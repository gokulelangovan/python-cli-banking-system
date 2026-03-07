from pydantic import BaseModel, constr, EmailStr

class CreateAccountRequest(BaseModel):
    name: str
    email: EmailStr
    phone: constr(pattern="^[6-9][0-9]{9}$")
    
class DepositRequest(BaseModel):
    account_number: str
    amount: float
    
class WithdrawRequest(BaseModel):
    account_number: str
    amount: float


class TransferRequest(BaseModel):
    sender_account: str
    receiver_account: str
    amount: float
    
class CreateAccountResponse(BaseModel):
    message: str
    account_number: str