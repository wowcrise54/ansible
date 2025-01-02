from pydantic import BaseModel
from typing import Optional, List

class PlaybookExecuteRequest(BaseModel):
    playbook_name: str
    host: str
    extra_vars: Optional[dict] = None

class PlaybookResponse(BaseModel):
    status: str
    output: str
    playbook_name: str
    host: str

class PlaybookList(BaseModel):
    playbooks: List[str] 