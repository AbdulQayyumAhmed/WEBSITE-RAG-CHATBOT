from pydantic import BaseModel, EmailStr

# Website input
class WebsiteRequest(BaseModel):
    url: str

# Chat input
class ChatRequest(BaseModel):
    message: str
    use_website: bool = False

# User creation input
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

# User output
class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        orm_mode = True

# Chat output
class ChatOut(BaseModel):
    mode: str
    response: str

# Website output
class WebsiteOut(BaseModel):
    message: str
    chunks_stored: int
    website_id: int