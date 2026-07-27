from pydantic import BaseModel


class VaultCreate(BaseModel):
    website: str
    username: str
    password: str


class VaultResponse(BaseModel):
    id: int
    website: str
    username: str

    model_config = {
        "from_attributes": True
    }

class VaultUpdate(BaseModel):
    website: str
    username: str
    password: str