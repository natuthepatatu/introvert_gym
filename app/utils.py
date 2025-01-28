import httpx
from datetime import datetime

API_URL = "https://www.jumpers-fitness.com/connect/v1/studio/1381129950/utilization"

async def fetch_daily_history():
    """
    Fetch daily utilization history up to the current time.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(API_URL)
        if response.status_code == 200:
            data = response.json()
            
            # Find the current hour entry (isCurrent: true)
            current_time_frame = None
            for item in data["items"]:
                if item["isCurrent"]:
                    current_time_frame = item
                    break

            # Keep all data up to and including the current time frame
            filtered_data = []
            for item in data["items"]:
                filtered_data.append(item)
                if item == current_time_frame:
                    break  # Stop after adding the current entry
            
            return filtered_data
        else:
            return {"error": f"Failed to fetch data, status code: {response.status_code}"}
