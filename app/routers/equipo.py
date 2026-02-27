from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def listar_equipos():
    return []