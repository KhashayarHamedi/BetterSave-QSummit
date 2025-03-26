"""
imports_config.py
Contains all imports and basic configuration for the BetterSave Energy Dashboard
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import numpy as np
import calendar
import os
import time

# Set page configuration
def configure_page():
    """Configure the Streamlit page settings"""
    st.set_page_config(
        page_title="BetterSave Energy Dashboard",
        page_icon="⚡",
        layout="wide",
        initial_sidebar_state="expanded"
    )

# Define plot theme configuration to match Webflow dark theme (can be imported by visualization modules)
PLOT_THEME = {
    "template": "plotly_dark",
    "plot_bgcolor": "#101935",  # --secondary--color-1
    "paper_bgcolor": "rgba(16, 25, 53, 0)",  # Transparent version of --secondary--color-1
    "font_color": "#aeb9e1",  # --neutral--400
    "grid_color": "rgba(55, 68, 107, 0.5)",  # --neutral--600 with transparency
    "color_sequence": ["#6c72ff", "#57c3ff", "#9a91fb", "#fdb52a", "#343b4f"]  # Webflow colors
}
