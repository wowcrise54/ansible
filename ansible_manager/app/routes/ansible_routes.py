from fastapi import APIRouter, HTTPException
from app.services.ansible_service import AnsibleService
from app.models.schemas import PlaybookExecuteRequest, PlaybookResponse, PlaybookList

router = APIRouter()
ansible_service = AnsibleService()

@router.get("/playbooks", response_model=PlaybookList)
async def list_playbooks():
    """Получить список доступных плейбуков"""
    playbooks = ansible_service.get_available_playbooks()
    return {"playbooks": playbooks}

@router.post("/execute", response_model=PlaybookResponse)
async def execute_playbook(request: PlaybookExecuteRequest):
    """Выполнить плейбук на указанном хосте"""
    try:
        result = await ansible_service.execute_playbook(
            request.playbook_name,
            request.host,
            request.extra_vars
        )
        return result
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 