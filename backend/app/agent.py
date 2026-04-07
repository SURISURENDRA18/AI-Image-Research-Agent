from app.tools.vision_tool import analyze_image
from app.tools.search_tool import search_web


def run_agent(image_bytes):
    # Vision analysis
    vision_result = analyze_image(image_bytes)

    #Handle failure FIRST
    if "error" in vision_result:
        return {
            "status": "failed",
            "error": vision_result["error"]
        }

    #Extract keywords safely
    keywords = vision_result.get("objects", [])

    #External research (only if keywords exist)
    research = search_web(keywords) if keywords else []

    #Combine reasoning safely
    final_output = {
        "status": "success",
        "summary": vision_result.get("description", ""),
        "objects_detected": keywords,
        "insights": research
    }

    return final_output


