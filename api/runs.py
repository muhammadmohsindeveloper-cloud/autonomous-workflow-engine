from fastapi import APIRouter
from core.database import DatabaseManager
from core.logger import get_logger

router = APIRouter()

logger = get_logger("runs")
db = DatabaseManager(logger)


@router.get("/runs")
def runs():

    return db.get_runs()