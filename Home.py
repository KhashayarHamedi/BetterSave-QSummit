"""
Home.py
Landing page for the BetterSave Energy application
"""

import streamlit as st
import base64  # Required for background image encoding
from imports_config import configure_page
from styling import apply_webflow_theme, render_navigation, render_footer

# ✅ Function to Set Full-Page Background Image with Dark Overlay
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image:
        encoded_image = base64.b64encode(image.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded_image}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}

        /* Dark overlay for readability */
        .stApp::before {{
            content: "";
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.4); /* Semi-transparent black */
            z-index: -1;
        }}

        /* Ensure text is readable */
        .stText, .stMarkdown, h1, h2, h3 {{
            color: white !important;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7);
            text-align: center;
        }}

        /* Center the buttons */
        .btn-container {{
            display: flex;
            justify-content: center;
            margin-top: 50px;
            gap: 20px;
        }}

        /* Button styling */
        .custom-btn {{
            font-size: 20px;
            font-weight: bold;
            color: white !important;
            text-decoration: none;
            padding: 12px 25px;
            border: 2px solid white;
            border-radius: 5px;
            transition: 0.3s ease-in-out;
            animation: blink 1.5s infinite; /* Slower blinking */
            background-color: transparent;
            cursor: pointer;
            position: relative;
        }}

        /* Green glowing effect */
        .custom-btn::before {{
            content: "";
            position: absolute;
            top: -2px;
            left: -2px;
            right: -2px;
            bottom: -2px;
            border-radius: 5px;
            background: linear-gradient(45deg, #00ffcc, #00ffcc, #00ffcc, #00ffcc);
            z-index: -1;
            opacity: 0;
            animation: glow 3s infinite; /* Slow glowing effect */
        }}

        /* Slower blinking animation */
        @keyframes blink {{
            0% {{ background-color: white; color: black; }}
            50% {{ background-color: black; color: white; }}
            100% {{ background-color: white; color: black; }}
        }}

        /* Glowing animation */
        @keyframes glow {{
            0% {{ opacity: 0; box-shadow: 0 0 5px #00ffcc; }}
            50% {{ opacity: 1; box-shadow: 0 0 20px #00ffcc; }}
            100% {{ opacity: 0; box-shadow: 0 0 5px #00ffcc; }}
        }}

        /* Hover Effect */
        .custom-btn:hover {{
            animation: none; /* Stop blinking on hover */
            background-color: rgba(255, 255, 255, 0.2);
        }}

        .custom-btn:hover::before {{
            opacity: 1; /* Show glow on hover */
        }}

        /* Floating Email Button */
        .email-button {{
            position: fixed;
            bottom: 20px;
            right: 20px;
            background-color: white;
            color: black;
            font-size: 16px;
            font-weight: bold;
            padding: 12px 20px;
            border-radius: 5px;
            text-align: center;
            text-decoration: none;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.2);
            border: 2px solid black;
            transition: 0.3s ease-in-out;
        }}

        .email-button:hover {{
            background-color: black;
            color: white;
            transform: scale(1.05);
        }}

        </style>
        """,
        unsafe_allow_html=True
    )

def render_navigation():
    import streamlit as st
    st.sidebar.title("Navigation")
    pages = ["Dashboard", "Prediction", "About"]
    selection = st.sidebar.radio("Go to", pages)
    # Set a query parameter to let your app know which page to display
    st.experimental_set_query_params(page=selection)

# **✅ Apply Background Image**
add_bg_from_local("static/BK1.jpg")  # Path to the background image in static folder

# **State Variables for Video Playback**
if "play_video" not in st.session_state:
    st.session_state.play_video = False

# ✅ **"EXPLORE MORE" Button**
if st.button("EXPLORE MORE", key="explore"):
    st.session_state.play_video = True  # Set session state to trigger video

# ✅ **Render Video & Close Button**
if st.session_state.play_video:
    st.video("static/Final_video.MP4")  # Path to the video file inside static folder

    # Close Video Button
    if st.button("CLOSE VIDEO", key="close"):
        st.session_state.play_video = False  # Stop playing the video
        st.rerun()  # ✅ Use the correct method to refresh the page

# ✅ **Floating Email Button in Bottom-Right**
st.markdown(
    '<a class="email-button" href="mailto:officialkhashayar@gmail.com">Write to Us</a>',
    unsafe_allow_html=True
)
