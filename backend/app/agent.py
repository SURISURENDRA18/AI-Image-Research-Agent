from app.tools.vision_tool import analyze_image
from app.tools.search_tool import search_web


def run_agent(image_bytes):
    # Step 1: Vision analysis
    vision_result = analyze_image(image_bytes)

    # 🚨 Step 2: Handle failure FIRST
    if "error" in vision_result:
        return {
            "status": "failed",
            "error": vision_result["error"]
        }

    # Step 3: Extract keywords safely
    keywords = vision_result.get("objects", [])

    # Step 4: External research (only if keywords exist)
    research = search_web(keywords) if keywords else []

    # Step 5: Combine reasoning safely
    final_output = {
        "status": "success",
        "summary": vision_result.get("description", ""),
        "objects_detected": keywords,
        "insights": research
    }

    return final_output


