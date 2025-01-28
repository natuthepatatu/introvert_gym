from fastapi import APIRouter
from app.utils import fetch_utilization_data

router = APIRouter()

# Endpoint to get current utilization
@router.get("/current", tags=["Utilization"])
async def get_current_utilization():
    """
    Fetches the current gym utilization percentage.
    """
    current_data = await fetch_utilization_data()
    return current_data
