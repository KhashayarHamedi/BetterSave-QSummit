"""
Dashboard.py
Main entry point for the BetterSave Energy Dashboard application
"""


import streamlit as st

# Import modules
from imports_config import configure_page
from data_loader import load_data, filter_data
from styling import apply_webflow_theme, render_header, render_footer, render_navigation
from analysis import analyze_energy_trends
from components import (
    render_sidebar,
    render_kpi_section,
    render_energy_trends_tab,
    render_energy_sources_tab,
    render_forecasting_tab,
    render_data_explorer_tab
)

def main():
    """Main application entry point"""
    # Configure the page
    configure_page()

    # Apply the Webflow theme
    apply_webflow_theme()

    # Load data
    energy_generation, energy_consumption = load_data()

    # Render sidebar and get filter selections
    filters = render_sidebar(energy_generation, energy_consumption)

    # Check if data loaded successfully
    if energy_generation.empty or energy_consumption.empty or not filters:
        st.error("Failed to load data. Please check the CSV files.")
        return

    # Extract filters
    year_selection = filters["year_selection"]
    month_selection = filters["month_selection"]
    view_type = filters["view_type"]
    selected_sources = filters["selected_sources"]
    show_anomalies = filters["show_anomalies"]

    enable_download = filters["enable_download"]

    # Filter data based on selections
    filtered_energy_gen, filtered_energy_cons = filter_data(
        energy_generation,
        energy_consumption,
        year_selection,
        month_selection,
        selected_sources
    )

    # Calculate key metrics from filtered data
    metrics = analyze_energy_trends(filtered_energy_gen, filtered_energy_cons)


    # Main Dashboard
    render_header("BetterSave Energy Dashboard", "main-header")

    # Key Metrics Row
    render_kpi_section(metrics)

    # Main Dashboard Tabs
    tab1, tab2, tab3 = st.tabs([
        "📊 Energy Trends",
        "🔍 Energy Sources",
        "📋 Data Explorer"
    ])

    # Tab 1: Energy Trends
    with tab1:
        render_energy_trends_tab(
            filtered_energy_gen,
            filtered_energy_cons,
            selected_sources,
            view_type,
            show_anomalies
        )

    # Tab 2: Energy Sources
    with tab2:
        render_energy_sources_tab(
            filtered_energy_gen,
            selected_sources,
            view_type
        )


    # Tab 3: Data Explorer
    with tab3:
        render_data_explorer_tab(
            filtered_energy_gen,
            filtered_energy_cons,
            enable_download
        )

    # Footer
    render_footer()

if __name__ == "__main__":
    main()
