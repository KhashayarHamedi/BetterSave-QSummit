"""
styling.py
CSS styling and UI component functions for the BetterSave Energy Dashboard
"""

import streamlit as st

# Apply Webflow-inspired theme
def apply_webflow_theme():
    """Apply Webflow-inspired CSS theme to the Streamlit app"""
    # Load the CSS directly here
    webflow_css = """
    /* Import variables from the Webflow theme */
    :root {
      /* Dark theme colors */
      --neutral--800: #080f25;
      --neutral--700: #212c4d;
      --neutral--600: #37446b;
      --neutral--500: #7e89ac;
      --neutral--400: #aeb9e1;
      --neutral--300: #d1dbf9;
      --neutral--200: #d9e1fa;
      --neutral--100: white;

      /* Accent colors */
      --accent--primary-1: #6c72ff;
      --secondary--color-1: #101935;
      --secondary--color-2: #9a91fb;
      --secondary--color-3: #57c3ff;
      --secondary--color-4: #343b4f;
      --secondary--color-5: #fdb52a;

      /* System colors */
      --system--green-300: #14ca74;
      --system--300: #ff5a65;
      --system--red-400: #dc2b2b;
    }

    /* Base styling for the entire app */
    .stApp {
      background-color: var(--neutral--800);
      color: var(--neutral--100);
      font-family: 'Roboto', sans-serif;
    }

    /* Main content area */
    .main .block-container {
      padding: 2rem;
    }

    /* Improve text contrast throughout the app */
    .stMarkdown, .stText, p, li, span, div[data-testid="StyledLinkIconContainer"] {
      color: var(--neutral--100) !important;
    }

    /* Headers styling */
    h1, h2, h3, h4, h5, h6 {
      color: var(--neutral--100);
      font-weight: 500;
    }

    h1 {
      font-size: 28px;
      line-height: 1.571em;
      margin-bottom: 16px;
    }

    h2 {
      font-size: 24px;
      line-height: 1.417em;
      margin-bottom: 16px;
    }

    h3 {
      font-size: 22px;
      line-height: 1.273em;
      margin-bottom: 8px;
    }

    /* Card styling */
    div[data-testid="stExpander"] {
      border: 0.6px solid var(--secondary--color-4);
      background-color: var(--secondary--color-1);
      border-radius: 12px;
      box-shadow: 0 2px 7px 0 rgba(20, 20, 43, 0.07);
      padding: 1rem;
      margin-bottom: 1rem;
    }

    /* Button styling */
    .stButton > button {
      background-color: var(--accent--primary-1);
      color: var(--neutral--100);
      text-align: center;
      border-radius: 4px;
      padding: 8px 16px;
      font-weight: 500;
      line-height: 1.167em;
      border: none;
      transition: background-color 0.3s, color 0.3s;
    }

    .stButton > button:hover {
      background-color: var(--neutral--700);
      color: var(--neutral--100);
    }

    /* Secondary button style */
    .stButton > button.secondary {
      background-color: var(--neutral--700);
      color: var(--neutral--100);
    }

    .stButton > button.secondary:hover {
      background-color: var(--neutral--100);
      color: var(--neutral--700);
    }

    /* Input fields */
    div[data-baseweb="input"], div[data-baseweb="select"], div[data-baseweb="textarea"] {
      background-color: var(--neutral--100);
    }

    .stTextInput > div > div > input,
    .stSelectbox > div > div > div,
    .stTextArea > div > div > textarea {
      border: 0.6px solid var(--secondary--color-4);
      background-color: var(--secondary--color-1);
      color: var(--neutral--100);
      border-radius: 4px;
      padding: 14px;
      font-size: 12px;
      line-height: 1.167em;
      box-shadow: 0 2px 4px rgba(1, 5, 17, 0.2);
    }

    .stTextInput > div > div > input:hover,
    .stSelectbox > div > div > div:hover,
    .stTextArea > div > div > textarea:hover {
      border-color: var(--neutral--500);
      box-shadow: 0 2px 12px 0 rgba(20, 20, 43, 0.03);
    }

    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > div:focus,
    .stTextArea > div > div > textarea:focus {
      border-color: var(--accent--primary-1);
    }

    /* Metrics styling */
    div[data-testid="stMetric"] {
      background-color: var(--secondary--color-1);
      border: 0.6px solid var(--secondary--color-4);
      border-radius: 12px;
      padding: 1.5rem;
      margin: 0.5rem;
      box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
      transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    div[data-testid="stMetric"]:hover {
      transform: translateY(-5px);
      box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }

    div[data-testid="stMetric"] label {
      color: var(--neutral--100) !important;
      font-size: 1.1rem;
      font-weight: 600;
      margin-bottom: 0.5rem;
    }

    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
      color: var(--neutral--100) !important;
      font-size: 2.2rem;
      font-weight: 700;
      margin-bottom: 0.5rem;
    }

    /* Sidebar styling */
    section[data-testid="stSidebar"] {
      background-color: var(--neutral--800);
      border-right: 0.6px solid var(--neutral--600);
    }

    section[data-testid="stSidebar"] .block-container {
      padding: 2rem 1rem;
    }

    /* Make sidebar elements cleaner */
    section[data-testid="stSidebar"] [data-testid="stMarkdown"] h1,
    section[data-testid="stSidebar"] [data-testid="stMarkdown"] h2,
    section[data-testid="stSidebar"] [data-testid="stMarkdown"] h3 {
      color: var(--accent--primary-1);
      font-size: 1.3em;
      margin-bottom: 1rem;
    }

    /* Improve sidebar text contrast */
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stSelectbox,
    section[data-testid="stSidebar"] .stMultiSelect span,
    section[data-testid="stSidebar"] .stRadio label,
    section[data-testid="stSidebar"] .stCheckbox label {
      color: var(--neutral--100) !important;
    }

    /* Sidebar control labels */
    .stRadio label, .stCheckbox label, .stSlider label, .stSelectbox label, .stMultiSelect label {
      color: var(--neutral--100) !important;
      font-weight: 500 !important;
    }

    /* Progress bars */
    div[role="progressbar"] {
      background-color: var(--neutral--600);
      border-radius: 0.8px;
    }

    div[role="progressbar"] > div {
      background-color: var(--accent--primary-1);
    }

    /* Status elements */
    div[data-testid="stInfo"] {
      background-color: rgba(33, 150, 243, 0.1);
      border-left: 4px solid var(--accent--primary-1);
      padding: 1rem;
      margin: 1rem 0;
      border-radius: 4px;
    }

    div[data-testid="stSuccess"] {
      background-color: rgba(20, 202, 116, 0.1);
      border-left: 4px solid var(--system--green-300);
      padding: 1rem;
      margin: 1rem 0;
      border-radius: 4px;
    }

    div[data-testid="stWarning"] {
      background-color: rgba(255, 152, 0, 0.1);
      border-left: 4px solid var(--secondary--color-5);
      padding: 1rem;
      margin: 1rem 0;
      border-radius: 4px;
    }

    div[data-testid="stError"] {
      background-color: rgba(255, 90, 101, 0.1);
      border-left: 4px solid var(--system--300);
      padding: 1rem;
      margin: 1rem 0;
      border-radius: 4px;
    }

    /* Ensure text in status elements is readable */
    div[data-testid="stInfo"] p,
    div[data-testid="stSuccess"] p,
    div[data-testid="stWarning"] p,
    div[data-testid="stError"] p,
    .info-card,
    .warning-card {
      color: var(--neutral--100) !important;
    }

    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
      gap: 8px;
    }

    .stTabs [data-baseweb="tab"] {
      height: 50px;
      white-space: pre-wrap;
      background-color: var(--secondary--color-1);
      border-radius: 8px 8px 0px 0px;
      padding: 10px;
      font-weight: 500;
    }

    .stTabs [aria-selected="true"] {
      background-color: var(--accent--primary-1);
      color: white;
    }

    /* DataFrames and Tables */
    div[data-testid="stTable"] table {
      border-radius: 12px;
      overflow: hidden;
      box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    }

    div[data-testid="stTable"] thead tr th {
      background-color: var(--secondary--color-1);
      color: var(--neutral--100);
      padding: 0.8rem;
      text-align: left;
      font-weight: 600;
      border-bottom: 1px solid var(--neutral--600);
    }

    div[data-testid="stTable"] tbody tr td {
      background-color: var(--secondary--color-1);
      color: var(--neutral--100);
      padding: 0.8rem;
      border-bottom: 1px solid var(--neutral--600);
    }

    div[data-testid="stTable"] tbody tr:nth-child(even) td {
      background-color: var(--secondary--color-4);
    }

    /* DataFrames */
    div[data-testid="stDataFrame"] table {
      color: var(--neutral--100) !important;
    }

    div[data-testid="stDataFrame"] th {
      color: var(--neutral--100) !important;
      background-color: var(--secondary--color-4) !important;
    }

    div[data-testid="stDataFrame"] td {
      color: var(--neutral--100) !important;
    }

    /* Charts and plots */
    div[data-testid="stChart"] {
      background-color: var(--secondary--color-1);
      border-radius: 12px;
      padding: 1rem;
      margin: 1rem 0;
      box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
      border: 0.6px solid var(--secondary--color-4);
    }

    /* Custom class for metric cards */
    .metric-container {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 20px;
      margin: 10px;
      border-radius: 15px;
      text-align: center;
      font-weight: bold;
      color: var(--neutral--100);
      box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
      background: linear-gradient(135deg, var(--secondary--color-1), var(--neutral--700));
      transition: transform 0.3s ease, box-shadow 0.3s ease;
      height: 180px;
      width: 100%;
    }

    .metric-title {
      font-size: 1rem !important;
      font-weight: 600 !important;
      margin-bottom: 10px !important;
      color: var(--neutral--100) !important;
    }

    .metric-value {
      font-size: 1.8rem !important;
      font-weight: 700 !important;
      margin-bottom: 10px !important;
      color: var(--neutral--100) !important;
    }

    .metric-subtitle {
      font-size: 0.8rem !important;
      color: var(--neutral--200) !important;
      font-weight: 400 !important;
    }

    .metric-container:hover {
      transform: scale(1.05);
      box-shadow: 0 0 20px rgba(0, 0, 0, 0.3);
    }

    /* Custom header styling */
    .main-header {
      font-size: 2.5rem;
      font-weight: 700;
      text-align: center;
      color: var(--accent--primary-1);
      margin: 1rem 0;
      padding-bottom: 1rem;
      border-bottom: 2px solid var(--secondary--color-4);
    }

    /* Subheader styling */
    .subheader {
      font-size: 1.8rem;
      font-weight: 600;
      color: var(--neutral--100);
      margin: 1.5rem 0 1rem 0;
      padding-bottom: 0.5rem;
      border-bottom: 1px solid var(--neutral--600);
    }

    /* Section title styling */
    .section-title {
      font-size: 1.5rem;
      font-weight: 600;
      color: var(--secondary--color-3);
      margin: 1rem 0;
    }

    /* Custom metric card colors - with fixed heights and consistent styling */
    .metric-secondary {
      background: linear-gradient(135deg, var(--secondary--color-2), var(--accent--primary-1));
      height: 180px; /* Fixed height */
    }

    .metric-accent {
      background: linear-gradient(135deg, var(--secondary--color-5), var(--secondary--color-3));
      height: 180px; /* Fixed height */
    }

    /* Ensure all KPI cards in the same row have equal height */
    div.row-widget.stRow {
      display: flex;
      flex-wrap: wrap;
    }

    div.row-widget.stRow > div {
      display: flex;
      flex: 1 1 0;
    }

    div.row-widget.stRow > div > div {
      width: 100%;
    }

    /* Footer styling */
    .footer {
      text-align: center;
      margin-top: 2rem;
      padding-top: 1rem;
      border-top: 1px solid var(--neutral--600);
      font-size: 0.9rem;
      color: var(--neutral--400);
    }

    /* Slider styling */
    div[data-testid="stSlider"] > div {
      color: var(--neutral--300);
    }

    div[data-testid="stSlider"] > div > div > div {
      background-color: var(--accent--primary-1);
    }

    /* Radio button styling */
    .st-bq {
      background-color: var(--secondary--color-1);
    }

    /* Checkbox styling */
    .st-cd, .st-ce {
      background-color: var(--accent--primary-1) !important;
    }

    /* Navigation bar styling */
    .navbar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 1rem 2rem;
      background: linear-gradient(90deg, var(--secondary--color-1), var(--neutral--800));
      border-bottom: 1px solid var(--neutral--600);
      box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
      border-radius: 0 0 10px 10px;
      margin-bottom: 20px;
    }

    .navbar-logo {
      font-size: 1.5rem;
      font-weight: bold;
    }

    .navbar-links {
      display: flex;
      gap: 1.5rem;
    }

    .nav-link {
      color: var(--neutral--400);
      text-decoration: none;
      font-weight: 500;
      padding: 0.5rem 1rem;
      border-radius: 6px;
      transition: all 0.3s ease;
    }

    .nav-link:hover {
      color: var(--neutral--100);
      background-color: rgba(108, 114, 255, 0.1);
    }

    .nav-link.active {
      color: var(--neutral--100);
      background-color: var(--accent--primary-1);
    }

    /* Styling for landing page */
    .hero-content {
      padding: 2rem 0;
    }

    .hero-title {
      font-size: 2.2rem;
      font-weight: 700;
      color: var(--accent--primary-1);
      margin-bottom: 1rem;
    }

    .hero-description {
      font-size: 1.2rem;
      color: var(--neutral--300);
      margin-bottom: 2rem;
      line-height: 1.5;
    }

    .hero-buttons {
      display: flex;
      gap: 1rem;
      margin-top: 2rem;
    }

    .hero-button {
      display: inline-block;
      padding: 0.8rem 1.5rem;
      border-radius: 8px;
      font-weight: 600;
      text-decoration: none;
      transition: all 0.3s ease;
    }

    .primary-button {
      background-color: var(--accent--primary-1);
      color: white;
    }

    .primary-button:hover {
      background-color: var(--secondary--color-2);
      transform: translateY(-3px);
    }

    .secondary-button {
      background-color: var(--secondary--color-4);
      color: var(--neutral--100);
    }

    .secondary-button:hover {
      background-color: var(--neutral--600);
      transform: translateY(-3px);
    }

    .placeholder-image {
      background: linear-gradient(135deg, var(--secondary--color-1), var(--neutral--700));
      height: 300px;
      width: 100%;
      border-radius: 16px;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      color: var(--neutral--100);
      font-size: 1.5rem;
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
    }

    .feature-card {
      background: linear-gradient(135deg, var(--secondary--color-1), var(--neutral--700));
      border-radius: 12px;
      padding: 1.5rem;
      height: 100%;
      min-height: 250px;
      box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
      margin-bottom: 1rem;
      transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    .feature-card:hover {
      transform: translateY(-5px);
      box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
    }

    .feature-icon {
      font-size: 3rem;
      margin-bottom: 1rem;
      color: var(--accent--primary-1);
    }

    .feature-card h3 {
      font-size: 1.5rem;
      font-weight: 600;
      color: var(--neutral--100);
      margin-bottom: 1rem;
    }

    .feature-card p {
      color: var(--neutral--300);
      line-height: 1.5;
    }

    .cta-section {
      background: linear-gradient(135deg, var(--secondary--color-1), var(--neutral--700));
      padding: 3rem 2rem;
      border-radius: 12px;
      text-align: center;
      margin: 3rem 0;
    }

    .cta-section h2 {
      font-size: 2rem;
      font-weight: 700;
      color: var(--neutral--100);
      margin-bottom: 1rem;
    }

    .cta-section p {
      font-size: 1.2rem;
      color: var(--neutral--300);
      margin-bottom: 2rem;
    }

    .cta-button {
      display: inline-block;
      padding: 1rem 2rem;
      background-color: var(--accent--primary-1);
      color: white;
      font-weight: 600;
      border-radius: 8px;
      text-decoration: none;
      transition: all 0.3s ease;
    }

    .cta-button:hover {
      background-color: var(--secondary--color-2);
      transform: translateY(-3px);
    }

    /* About page styling */
    .about-section {
      margin-bottom: 3rem;
    }

    .about-text {
      font-size: 1.1rem;
      line-height: 1.6;
      color: var(--neutral--200);
      margin-bottom: 1.5rem;
    }

    .team-card {
      background: linear-gradient(135deg, var(--secondary--color-1), var(--neutral--700));
      border-radius: 12px;
      padding: 2rem;
      text-align: center;
      height: 100%;
      min-height: 300px;
      margin-bottom: 1.5rem;
      transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    .team-card:hover {
      transform: translateY(-5px);
      box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
    }

    .team-avatar {
      font-size: 3rem;
      margin-bottom: 1rem;
    }

    .team-card h3 {
      font-size: 1.3rem;
      font-weight: 600;
      color: var(--neutral--100);
      margin-bottom: 0.5rem;
    }

    .team-title {
      color: var(--accent--primary-1);
      font-weight: 500;
      margin-bottom: 1rem;
    }

    .team-bio {
      color: var(--neutral--300);
      font-size: 0.9rem;
      line-height: 1.5;
    }

    .approach-card {
      background: linear-gradient(135deg, var(--neutral--700), var(--secondary--color-4));
      border-radius: 8px;
      padding: 1.5rem;
      height: 100%;
      margin-bottom: 1.5rem;
    }

    .approach-card h3 {
      color: var(--secondary--color-3);
      font-weight: 600;
      margin-bottom: 1rem;
    }

    .approach-card p {
      color: var(--neutral--300);
      line-height: 1.5;
    }

    .contact-section {
      background: linear-gradient(135deg, var(--secondary--color-1), var(--neutral--700));
      padding: 2rem;
      border-radius: 12px;
      margin: 3rem 0;
    }

    .contact-text {
      color: var(--neutral--300);
      margin-bottom: 1.5rem;
      line-height: 1.5;
    }

    .contact-info {
      display: flex;
      flex-direction: column;
      gap: 1rem;
    }

    .contact-item {
      display: flex;
      align-items: center;
      gap: 1rem;
    }

    .contact-icon {
      font-size: 1.5rem;
    }

    .contact-link {
      color: var(--accent--primary-1);
      text-decoration: none;
      transition: color 0.3s ease;
    }

    .contact-link:hover {
      color: var(--secondary--color-3);
      text-decoration: underline;
    }

    /* For mobile responsiveness */
    @media (max-width: 768px) {
      .main .block-container {
        padding: 1rem;
      }

      div[data-testid="stMetric"] {
        padding: 1rem;
      }

      .navbar {
        flex-direction: column;
        gap: 1rem;
        padding: 1rem;
      }

      .navbar-links {
        width: 100%;
        justify-content: space-between;
        flex-wrap: wrap;
      }

      .nav-link {
        padding: 0.3rem 0.7rem;
        font-size: 0.9rem;
      }

      .hero-title {
        font-size: 1.8rem;
      }

      .hero-description {
        font-size: 1rem;
      }

      .hero-buttons {
        flex-direction: column;
        gap: 1rem;
      }

      .contact-info {
        flex-direction: column;
      }

      .feature-card, .team-card {
        min-height: auto;
      }
    }
    """

    # Apply the CSS
    st.markdown(f"<style>{webflow_css}</style>", unsafe_allow_html=True)

    # Always return True since we don't have a dark mode toggle anymore
    # (dark mode is now the default in the Webflow theme)
    return True

# Custom components for enhanced UI
def render_metric_card(title, value, subtitle="", metric_type="primary"):
    """
    Render a custom metric card with Webflow styling

    Args:
        title (str): Card title
        value (str): Main value to display
        subtitle (str, optional): Subtitle or additional information
        metric_type (str, optional): Card style type - "primary", "secondary", or "accent"
    """
    class_name = f"metric-container {f'metric-{metric_type}' if metric_type != 'primary' else ''}"
    st.markdown(f"""
        <div class="{class_name}">
            <div class="metric-title">{title}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-subtitle">{subtitle}</div>
        </div>
    """, unsafe_allow_html=True)

def render_info_card(text, card_type="info"):
    """
    Render an information card (info, warning, etc.)

    Args:
        text (str): Card text content
        card_type (str, optional): Card type - "info", "warning", "success", or "error"
    """
    st.markdown(f"""
        <div class="{card_type}-card" style="color: var(--neutral--100);">
            {text}
        </div>
    """, unsafe_allow_html=True)

def render_header(text, header_type="main-header"):
    """
    Render a styled header

    Args:
        text (str): Header text
        header_type (str, optional): Header style class - "main-header", "subheader", or "section-title"
    """
    st.markdown(f"<h1 class='{header_type}'>{text}</h1>", unsafe_allow_html=True)

def render_navigation():
    """Render the navigation bar at the top of the page"""
    st.markdown("""
    <nav class="navbar">
        <div class="navbar-logo">
            <span style="color: #6c72ff; font-weight: 700;">BetterSave</span>
            <span style="color: #57c3ff; font-weight: 500;">Energy</span>
        </div>
        <div class="navbar-links">
            <a href="/" class="nav-link">Home</a>
            <a href="/dashboard" class="nav-link active">Dashboard</a>
            <a href="/prediction" class="nav-link">Prediction</a>
            <a href="/about" class="nav-link">About Us</a>
        </div>
    </nav>
    <div style="margin-bottom: 20px;"></div>
    """, unsafe_allow_html=True)

def render_footer():
    """Render the dashboard footer with Webflow styling"""
    st.markdown("---")
    st.markdown("""
        <div class='footer'>
            <div style="margin-bottom: 10px;">
                <span style="font-size: 1.2rem; color: #6c72ff;">BetterSave</span>
                <span style="font-size: 1.2rem; color: #aeb9e1;"> • Sustainable Energy Analytics</span>
            </div>
            <p>© 2025 BetterSave Energy • Making Energy Management Smarter</p>
        </div>
    """, unsafe_allow_html=True)

def render_logo():
    """Render the BetterSave logo in the sidebar"""
    st.markdown("""
        <div style="display: flex; justify-content: center; margin-bottom: 20px;">
            <div style="background: linear-gradient(135deg, #6c72ff, #57c3ff); width: 80px; height: 80px;
                  border-radius: 16px; display: flex; align-items: center; justify-content: center;
                  margin: 0 auto; box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);">
                <span style="color: white; font-size: 36px;">⚡</span>
            </div>
        </div>
        <h2 style="text-align: center; color: #aeb9e1; margin-bottom: 20px;">BetterSave Energy</h2>
    """, unsafe_allow_html=True)
