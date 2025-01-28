from fastapi import APIRouter
from app.utils import fetch_daily_history
import matplotlib.pyplot as plt
import io
import base64
from fastapi.responses import HTMLResponse

# Initialize the router
router = APIRouter()

@router.get("/", tags=["Home"])
async def plot_occupancy():
    """
    Generate and serve a modern-styled matplotlib plot for daily gym occupancy up to the current time.
    """
    # Fetch historical data
    data = await fetch_daily_history()
    if "error" in data:
        return {"error": data["error"]}

    # Extract times, percentages, and find the current time frame
    times = []
    percentages = []
    current_time_frame = None

    for item in data:
        times.append(item["startTime"])
        percentages.append(item["percentage"])

        if item["isCurrent"]:
            current_time_frame = item
            break  # Stop after the current time

    # Set style for the plot
    plt.style.use("ggplot")

    # Create the plot
    plt.figure(figsize=(12, 6))

    # Shaded zones based on occupancy
    plt.axhspan(0, 28, color="green", alpha=0.2)  # Comfortable
    plt.axhspan(28, 37, color="orange", alpha=0.2)  # Okay-ish
    plt.axhspan(37, 100, color="red", alpha=0.2)  # Too crowded

    # Plot occupancy line
    plt.plot(
        times,
        percentages,
        linestyle="-",  # Smooth line
        alpha=0.8,
        linewidth=3,
        color="#2980b9",  # Elegant blue
        label="Occupancy (%)",
    )

    # Highlight the current time frame
    if current_time_frame:
        plt.scatter(
            current_time_frame["startTime"],
            current_time_frame["percentage"],
            color="#e74c3c",  # Red
            s=200,  # Bigger dot
            label=f"Current ({current_time_frame['percentage']}%)",
            zorder=5  # Ensure it overlays the line
        )

    # Style the plot
    plt.title("Gym Occupancy Throughout the Day", fontsize=18, fontweight="bold", color="#2c3e50")
    plt.xlabel("Time", fontsize=14, color="#2c3e50")
    plt.ylabel("Occupancy (%)", fontsize=14, color="#2c3e50")
    plt.ylim((0,100))
    plt.xticks(rotation=45, fontsize=12, color="#34495e")
    plt.yticks(fontsize=12, color="#34495e")
    plt.grid(visible=True, linestyle="--", alpha=0.5)
    plt.legend(fontsize=12, loc="upper left")

    # Save the plot to a BytesIO stream
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close()

    # Convert plot to Base64 for embedding in HTML
    img_base64 = base64.b64encode(buf.getvalue()).decode("utf-8")

    # Build the text summary
    if current_time_frame:
        summary = (
            f"<h2 style='color: #2c3e50;'>"
            f"Current Gym Occupancy: {current_time_frame['percentage']}% "
            f"({current_time_frame['startTime']} - {current_time_frame['endTime']})"
            f"</h2>"
        )
    else:
        summary = "<h2 style='color: #2c3e50;'>No current occupancy data available.</h2>"

    # Return an HTML page with the text and the image
    html_content = f"""
    <html>
        <body style="text-align: center; font-family: Arial, sans-serif;">
            <h1 style="color: #34495e;">Introvert Gym Occupancy</h1>
            {summary}
            <img src="data:image/png;base64,{img_base64}" style="max-width: 100%; height: auto;"/>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)
