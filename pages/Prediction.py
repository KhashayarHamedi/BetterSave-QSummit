"""
Prediction.py
Energy prediction page for BetterSave Energy application
"""

import streamlit as st
import pandas as pd
import requests
import os
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px

from imports_config import configure_page
from data_loader import load_data, load_prediction_data
from styling import apply_webflow_theme, render_navigation, render_footer, render_header, render_info_card
from analysis import forecast_energy_trends
from visualization import default_layout, COLORS

# Add improved styles for the prediction page
def add_prediction_styles():
    st.markdown("""
    <style>
    /* Clean, professional text styling */
    .highlight-text {
        text-align: center;
        font-size: 18px;
        font-weight: 500;
        color: #6c72ff;
        margin-bottom: 15px;
    }

    .center-text {
        text-align: center;
        font-size: 18px;
        font-weight: bold;
    }

    /* Metric cards */
    .metric-row {
        display: flex;
        flex-wrap: wrap;
        justify-content: space-between;
        margin-bottom: 20px;
    }

    .metric-card {
        background: linear-gradient(135deg, #101935, #212c4d);
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        text-align: center;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
    }

    .metric-label {
        font-size: 16px;
        color: #aeb9e1;
        margin-bottom: 8px;
    }

    .metric-value {
        font-size: 28px;
        font-weight: bold;
        color: white;
        margin-bottom: 5px;
    }

    .metric-unit {
        font-size: 14px;
        color: #7e89ac;
    }

    /* Model selector */
    .model-selector {
        background-color: #101935;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 20px;
        border: 1px solid #37446b;
    }

    /* Impact section */
    .impact-section {
        background: linear-gradient(135deg, #101935, #212c4d);
        border-radius: 12px;
        padding: 20px;
        margin: 25px 0;
        border: 1px solid #37446b;
    }

    .impact-section h2 {
        text-align: center;
        color: #57c3ff;
        margin-bottom: 20px;
    }

    /* Data table styling */
    .data-table-section {
        background-color: #101935;
        border-radius: 12px;
        padding: 20px;
        margin: 25px 0;
        border: 1px solid #37446b;
    }

    /* Section titles */
    .section-title {
        color: #57c3ff;
        font-size: 20px;
        font-weight: 600;
        margin: 20px 0 15px 0;
        border-bottom: 1px solid #37446b;
        padding-bottom: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

# API endpoint for prediction service
API_URL = "https://bettersave-296473938693.europe-west10.run.app/predict"

@st.cache_data(ttl=3600)
def fetch_prediction(steps):
    """Fetch prediction data from API"""
    params = {"steps": steps}
    try:
        response = requests.get(API_URL, params=params)
        if response.status_code == 200:
            try:
                data = response.json()
                if "confidence_interval" in data:
                    data["lower"] = data["confidence_interval"]["lower Residual load"]
                    data["upper"] = data["confidence_interval"]["upper Residual load"]
                    data.pop("confidence_interval", None)
                df = pd.DataFrame(data)
                if "Date" not in df.columns:
                    df["Date"] = pd.date_range(start="2020-01-01", periods=len(df), freq="D")
                df["model"] = "API Model"
                return df
            except Exception as e:
                st.error(f"Error processing API data: {e}")
                return None
        else:
            st.error("Failed to fetch prediction data")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"API connection error: {e}")
        return None

@st.cache_data(ttl=3600)
def load_csv_prediction():
    """Load prediction data from CSV file"""
    try:
        script_dir = os.path.dirname(__file__)
        parent_dir = os.path.join(script_dir, '..')
        csv_path = os.path.join(parent_dir, "365_day_predictions.csv")

        df = pd.read_csv(csv_path)

        # Ensure the dataframe has the expected columns
        if "Date" not in df.columns:
            # If date column doesn't exist, create it
            df["Date"] = pd.date_range(start="2020-01-01", periods=len(df), freq="D")
        else:
            # Ensure Date is in datetime format
            df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

        # For consistency with API format, rename main prediction column if needed
        if "forecast" in df.columns and "Residual load" not in df.columns:
            df["Residual load"] = df["forecast"]
        elif "Residual load" in df.columns and "forecast" not in df.columns:
            df["forecast"] = df["Residual load"]

        # Add model identifier
        df["model"] = "CSV Model"

        return df
    except Exception as e:
        st.error(f"Error loading CSV prediction data: {e}")
        return None

def render_metric_card(label, value, unit=""):
    """Render a custom metric card with hover effect"""
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-unit">{unit}</div>
        </div>
    """, unsafe_allow_html=True)

def main():
    """Main prediction page entry point"""
    # Configure the page
    configure_page()

    # Apply the Webflow theme
    apply_webflow_theme()

    # Add custom prediction styles
    add_prediction_styles()



    # Page header with clean styling
    render_header("Energy Prediction Dashboard", "main-header")

    # Main content container with better spacing
    st.markdown("""
        <div style='max-width: 1200px; margin: 0 auto; padding: 0 20px;'>
            <h3 class='section-title'>Energy Surplus Prediction</h3>
        </div>
    """, unsafe_allow_html=True)

    # Model selection
    with st.container():
        st.markdown("<div class='model-selector'>", unsafe_allow_html=True)
        col1, col2 = st.columns([2, 3])

        with col1:
            prediction_model = st.selectbox(
                "Select Prediction Model",
                options=["API Model", "CSV Model"],
                index=1,  # Default to CSV since API might not be available
                help="Choose which prediction model to use"
            )

        with col2:
            number_of_days = st.slider(
                "Prediction Horizon (Days)",
                min_value=7,
                max_value=365,
                value=30,
                step=7,
                help="Select number of days to predict"
            )
        st.markdown("</div>", unsafe_allow_html=True)

    # Load data for potential fallback
    energy_generation, energy_consumption = load_data()

    # Initialize session state for data if not exists
    if "prediction_data" not in st.session_state:
        st.session_state.prediction_data = None
        st.session_state.last_model = None
        st.session_state.last_days = None

    # Check if we need to fetch new data (model changed or days changed)
    model_changed = (st.session_state.last_model != prediction_model)
    days_changed = (st.session_state.last_days != number_of_days)

    if model_changed or days_changed or st.session_state.prediction_data is None:
        with st.spinner(f"Loading prediction data from {prediction_model}..."):
            if prediction_model == "API Model":
                # Fetch from API
                prediction_data = fetch_prediction(number_of_days)
            else:
                # Load from CSV using our new function
                prediction_data = load_prediction_data()

                # If CSV loaded successfully, filter to requested number of days
                if prediction_data is not None and not prediction_data.empty:
                    prediction_data = prediction_data.head(number_of_days)
                else:
                    st.error("Failed to load CSV prediction data. Using fallback method.")
                    # Fallback to simple forecasting if CSV fails
                    if not energy_consumption.empty:
                        st.warning("Using local forecasting method instead.")
                        historical_data, forecast_data = forecast_energy_trends(energy_consumption, periods=number_of_days)
                        if historical_data is not None and forecast_data is not None:
                            combined_data = pd.DataFrame({
                                "Date": forecast_data.index,
                                "forecast": forecast_data.values,
                                "lower": forecast_data.values * 0.9,
                                "upper": forecast_data.values * 1.1,
                                "model": "Fallback Model"
                            })
                            prediction_data = combined_data

            # Update session state
            st.session_state.prediction_data = prediction_data
            st.session_state.last_model = prediction_model
            st.session_state.last_days = number_of_days

    # Display prediction data and visualizations
    if st.session_state.prediction_data is not None:
        data = st.session_state.prediction_data

        # Ensure date column is datetime
        if "Date" in data.columns:
            data["Date"] = pd.to_datetime(data["Date"], errors='coerce')
            data = data.dropna(subset=["Date"])
            if "Year" not in data.columns:
                data["Year"] = data["Date"].dt.year
            if "Month" not in data.columns:
                data["Month"] = data["Date"].dt.strftime('%b')

            # Determine the column that contains the forecast values
            forecast_col = None
            for col_name in ["Residual load", "forecast", "prediction"]:
                if col_name in data.columns:
                    forecast_col = col_name
                    break

            if forecast_col is None:
                st.error("Could not find prediction values in the data.")
                return

            # Create the visualization
            fig = go.Figure()

            # Add the main prediction line
            fig.add_trace(go.Scatter(
                x=data["Date"],
                y=data[forecast_col],
                mode="lines",
                name="Energy Surplus Prediction",
                line=dict(color="#57c3ff", width=3)
            ))

            # Add confidence intervals if available
            if "lower" in data.columns and "upper" in data.columns:
                fig.add_trace(go.Scatter(
                    x=data["Date"].tolist() + data["Date"].tolist()[::-1],
                    y=data["upper"].tolist() + data["lower"].tolist()[::-1],
                    fill='toself',
                    fillcolor='rgba(87, 195, 255, 0.2)',
                    line=dict(color='rgba(255,255,255,0)'),
                    name="Confidence Interval"
                ))

            # Customize the figure
            fig.update_layout(
                title=f"Energy Surplus Prediction ({prediction_model})",
                xaxis_title="Date",
                yaxis_title="Energy (MWh)",
                template="plotly_dark",
                plot_bgcolor="#101935",
                paper_bgcolor="rgba(16, 25, 53, 0)",
                font=dict(color="#aeb9e1"),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="center",
                    x=0.5
                ),
                margin=dict(l=20, r=20, t=60, b=20),
                height=500
            )

            # Show the chart
            st.plotly_chart(fig, use_container_width=True)

            # Display key metrics in a more appealing way
            st.markdown("<div class='section-title'>Key Metrics</div>", unsafe_allow_html=True)

            col1, col2, col3 = st.columns(3)

            # Calculate metrics
            total_surplus = data[forecast_col].sum()
            avg_daily_surplus = data[forecast_col].mean()
            peak_surplus = data[forecast_col].max()
            peak_date = data.loc[data[forecast_col].idxmax(), "Date"]
            peak_date_str = peak_date.strftime('%b %d, %Y') if isinstance(peak_date, pd.Timestamp) else str(peak_date)

            with col1:
                render_metric_card(
                    "Total Energy Surplus",
                    f"{total_surplus:,.1f}",
                    "MWh"
                )

            with col2:
                render_metric_card(
                    "Average Daily Surplus",
                    f"{avg_daily_surplus:,.1f}",
                    "MWh/day"
                )

            with col3:
                render_metric_card(
                    "Peak Surplus",
                    f"{peak_surplus:,.1f}",
                    f"MWh on {peak_date_str}"
                )

            # Impact visualization section
            st.markdown("<div class='impact-section'>", unsafe_allow_html=True)
            st.markdown("<h2>Energy Impact Calculator</h2>", unsafe_allow_html=True)

            impact_tabs = st.tabs(["EV Charging", "Home Power", "CO₂ Reduction"])

            with impact_tabs[0]:
                col1, col2 = st.columns([2, 1])

                with col1:
                    # EV selection
                    ev_options = {
                        "Audi e-tron 55 quattro": 95,
                        "Tesla Model 3": 60,
                        "Nissan Leaf": 40,
                        "BMW i3": 42.2,
                        "Volkswagen ID.4": 77
                    }

                    selected_ev = st.selectbox(
                        "Select Electric Vehicle Model",
                        options=list(ev_options.keys()),
                        index=0
                    )

                    battery_capacity_kwh = ev_options[selected_ev]
                    total_charges = int((total_surplus * 1000) / battery_capacity_kwh)

                    st.markdown(f"""
                        <div class="highlight-text">
                        With {total_surplus:,.1f} MWh of surplus energy, we could fully charge:
                        </div>
                    """, unsafe_allow_html=True)

                    st.markdown(f"<div style='text-align: center; font-size: 48px; font-weight: bold; color: #57c3ff;'>{total_charges:,}</div>", unsafe_allow_html=True)

                    st.markdown(f"<div class='center-text'>{selected_ev} vehicles</div>", unsafe_allow_html=True)

                with col2:
                    # Add an EV icon or small visualization
                    st.markdown("""
                        <div style="display: flex; align-items: center; justify-content: center; height: 100%;">
                            <span style="font-size: 80px;">🚗⚡</span>
                        </div>
                    """, unsafe_allow_html=True)

            with impact_tabs[1]:
                # Homes powered calculation
                avg_home_annual_consumption_mwh = 3.5  # Average German household yearly consumption in MWh

                # Convert to monthly
                avg_home_monthly_consumption_mwh = avg_home_annual_consumption_mwh / 12

                # Calculate how many months of data we have
                if len(data) > 30:
                    months_of_data = len(data) / 30  # Approximate
                else:
                    months_of_data = 1

                # Calculate homes that could be powered
                homes_powered = int(total_surplus / (avg_home_monthly_consumption_mwh * months_of_data))

                col1, col2 = st.columns([3, 1])

                with col1:
                    st.markdown(f"""
                        <div class="highlight-text">
                        This energy surplus could power approximately:
                        </div>
                    """, unsafe_allow_html=True)

                    st.markdown(f"<div style='text-align: center; font-size: 48px; font-weight: bold; color: #57c3ff;'>{homes_powered:,}</div>", unsafe_allow_html=True)

                    st.markdown(f"<div class='center-text'>German homes for {months_of_data:.1f} months</div>", unsafe_allow_html=True)

                    # Progress bar showing impact
                    max_homes = 5000  # For scale
                    progress_percentage = min(1.0, homes_powered / max_homes)
                    st.progress(progress_percentage)
                    st.caption(f"Impact scale: {homes_powered:,} out of {max_homes:,} homes")

                with col2:
                    # Add a home icon
                    st.markdown("""
                        <div style="display: flex; align-items: center; justify-content: center; height: 100%;">
                            <span style="font-size: 80px;">🏡💡</span>
                        </div>
                    """, unsafe_allow_html=True)

            with impact_tabs[2]:
                # CO2 reduction calculation
                co2_per_mwh_coal = 1000  # kg CO2 per MWh from coal
                co2_saved = total_surplus * co2_per_mwh_coal / 1000  # Convert to metric tons

                col1, col2 = st.columns([3, 1])

                with col1:
                    st.markdown(f"""
                        <div class="highlight-text">
                        By using this renewable energy surplus instead of coal power, we could avoid:
                        </div>
                    """, unsafe_allow_html=True)

                    st.markdown(f"<div style='text-align: center; font-size: 48px; font-weight: bold; color: #57c3ff;'>{co2_saved:,.1f}</div>", unsafe_allow_html=True)

                    st.markdown(f"<div class='center-text'>Metric tons of CO₂ emissions</div>", unsafe_allow_html=True)

                    # Add equivalence
                    trees_equivalent = int(co2_saved * 45)  # Approx. 45 trees absorb 1 ton of CO2
                    st.markdown(f"""
                        <div class="highlight-text" style="margin-top: 20px;">
                        This is equivalent to planting {trees_equivalent:,} trees!
                        </div>
                    """, unsafe_allow_html=True)

                with col2:
                    # Add an environment icon
                    st.markdown("""
                        <div style="display: flex; align-items: center; justify-content: center; height: 100%;">
                            <span style="font-size: 80px;">🌍♻️</span>
                        </div>
                    """, unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

            # Data table section with better styling
            st.markdown("<div class='data-table-section'>", unsafe_allow_html=True)
            st.markdown("<div class='section-title'>Prediction Data</div>", unsafe_allow_html=True)

            # Display columns
            display_cols = ["Date", forecast_col]
            if "lower" in data.columns:
                display_cols.append("lower")
            if "upper" in data.columns:
                display_cols.append("upper")

            # Format the dataframe for display
            display_df = data[display_cols].copy()
            if isinstance(display_df["Date"].iloc[0], pd.Timestamp):
                display_df["Date"] = display_df["Date"].dt.strftime('%Y-%m-%d')

            # Add pagination to the dataframe
            def paginate_df(df, page_size=10):
                total_pages = len(df) // page_size + (1 if len(df) % page_size > 0 else 0)
                page_number = st.slider("Page", 1, max(1, total_pages), 1)
                start_idx = (page_number - 1) * page_size
                end_idx = min(start_idx + page_size, len(df))
                return df.iloc[start_idx:end_idx], page_number, total_pages

            paginated_df, page, total_pages = paginate_df(display_df, 10)
            st.dataframe(paginated_df, use_container_width=True)
            st.caption(f"Page {page} of {total_pages}")

            # Download options
            col1, col2 = st.columns(2)

            with col1:
                st.download_button(
                    label="Download as CSV",
                    data=display_df.to_csv(index=False),
                    file_name=f"energy_prediction_{prediction_model.replace(' ', '_').lower()}.csv",
                    mime="text/csv"
                )

            with col2:
                st.download_button(
                    label="Download as JSON",
                    data=display_df.to_json(orient="records"),
                    file_name=f"energy_prediction_{prediction_model.replace(' ', '_').lower()}.json",
                    mime="application/json"
                )

            st.markdown("</div>", unsafe_allow_html=True)
    else:
        # No data available yet
        st.warning("No prediction data available. Please check that both the API and CSV data sources are accessible.")

    # Footer
    render_footer()

if __name__ == "__main__":
    main()
