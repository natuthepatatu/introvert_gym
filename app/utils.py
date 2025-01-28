import httpx

API_URL = "https://www.jumpers-fitness.com/connect/v1/studio/1381129950/utilization"

async def fetch_utilization_data():
    """
    Fetch utilization data from the gym API.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(API_URL)
        if response.status_code == 200:
            data = response.json()
            current = next((item for item in data["items"] if item["isCurrent"]), None)
            if current:
                return {
                    "startTime": current["startTime"],
                    "endTime": current["endTime"],
                    "percentage": current["percentage"],
                    "level": current["level"],
                }
            else:
                return {"message": "No current utilization data available."}
        else:
            return {"error": f"Failed to fetch data, status code: {response.status_code}"}
