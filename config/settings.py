
from __future__ import annotations
import os
from pydantic import BaseModel

class Creds(BaseModel):
    username: str
    password: str

class Config(BaseModel):
    base_url: str = os.getenv("BASE_URL", "http://localhost:5173")
    api_url: str = os.getenv("API_URL", "http://localhost:8000/api/v1")
    admin: Creds = Creds(username=os.getenv("ADMIN_USER","admin"), password=os.getenv("ADMIN_PASS","changeme123"))
    regular1: Creds = Creds(username=os.getenv("USER1","test1"), password=os.getenv("PASS1","megaboss19"))
    regular2: Creds = Creds(username=os.getenv("USER2","test28"), password=os.getenv("PASS2","megaboss19"))
    locale: str = os.getenv("TEST_LOCALE", "en-US")

cfg = Config()
