import streamlit as st
import requests

# -------------------- CONFIG --------------------
API_URL = "http://localhost:8000/analyze"

st.set_page_config(
    page_title="AI Image Research Agent",
    page_icon="🧠",
    layout="centered"
)

# -------------------- UI HEADER --------------------
st.title("🧠 AI Image Research Agent")
st.caption("Upload an image and get AI-powered insights")

# -------------------- FILE UPLOAD --------------------
uploaded_file = st.file_uploader(
    "Upload Image",
    type=["png", "jpg", "jpeg"]
)

if uploaded_file:
    st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)

    # -------------------- ANALYZE BUTTON --------------------
    if st.button("🔍 Analyze Image"):

        with st.spinner("Analyzing image... Please wait ⏳"):
            try:
                response = requests.post(
                    API_URL,
                    files={"file": uploaded_file.getvalue()},
                    timeout=30
                )

                # Handle HTTP errors
                if response.status_code != 200:
                    st.error(f"Server Error: {response.status_code}")
                    st.stop()

                result = response.json()

            except requests.exceptions.Timeout:
                st.error("⏱ Request timed out. Server is slow or stuck.")
                st.stop()

            except requests.exceptions.ConnectionError:
                st.error("🚫 Cannot connect to backend. Is FastAPI running?")
                st.stop()

            except Exception as e:
                st.error(f"Unexpected error: {str(e)}")
                st.stop()

        # -------------------- RESPONSE HANDLING --------------------
        st.divider()
        st.subheader("📊 Analysis Result")

        if result.get("status") != "success":
            st.error(result.get("error", "Unknown error occurred"))
            
            # Debug mode (important for dev)
            with st.expander("🛠 Debug Info"):
                st.json(result)
            st.stop()

        # -------------------- SUCCESS UI --------------------
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("📝 Summary")
            st.success(result.get("summary", "No summary available"))

        with col2:
            st.subheader("🔍 Objects Detected")
            objects = result.get("objects_detected", [])
            if objects:
                st.write(objects)
            else:
                st.info("No objects detected")

        st.subheader("🧠 Insights")
        insights = result.get("insights", "No insights available")

        with st.expander("View Insights"):
            st.write(insights)

        # -------------------- OPTIONAL: RAW RESPONSE --------------------
        with st.expander("📦 Raw API Response"):
            st.json(result)