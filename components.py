"""
components.py
UI component functions for different dashboard sections
"""

import streamlit as st
import pandas as pd
import numpy as np

from styling import render_metric_card, render_info_card, render_header
from analysis import (
    analyze_energy_trends,
    identify_anomalies,
    prepare_trends_data,
    calculate_monthly_consumption,
    calculate_weekday_consumption,
    calculate_source_totals,
    prepare_source_time_series
)
from visualization import (
    create_trends_chart,
    add_anomalies_to_chart,
    create_monthly_barchart,
    create_weekday_barchart,
    create_ratio_chart,
    create_source_pie_chart,
    create_source_bar_chart,
    create_source_time_series
)

def render_sidebar(energy_generation, energy_consumption):
    """
    Render the sidebar with filters and controls without topbar navigation elements.

    Args:
        energy_generation (DataFrame): Energy generation data.
        energy_consumption (DataFrame): Energy consumption data.

    Returns:
        dict: Dictionary of selected filter values.
    """
    from data_loader import get_date_range_values, get_energy_sources

    with st.sidebar:
        st.markdown("### Dashboard Filters")

        if energy_generation.empty or energy_consumption.empty:
            st.error("Failed to load data. Please check the CSV files.")
            return {}

        # Date range filter
        min_year, max_year = get_date_range_values(energy_generation, energy_consumption)

        year_selection = st.slider(
            "Select Year Range:",
            min_year,
            max_year,
            (min_year, max_year)
        )

        months = {
            1: "January", 2: "February", 3: "March", 4: "April",
            5: "May", 6: "June", 7: "July", 8: "August",
            9: "September", 10: "October", 11: "November", 12: "December"
        }

        month_selection = st.multiselect(
            "Select Months:",
            options=list(months.keys()),
            default=list(months.keys()),
            format_func=lambda x: months[x]
        )

        # Additional filters
        view_type = st.radio("Data Resolution:", ["Daily", "Monthly", "Quarterly", "Yearly"])

        # Data source filter
        available_sources = get_energy_sources(energy_generation)

        selected_sources = st.multiselect(
            "Energy Sources:",
            options=available_sources,
            default=available_sources[:5] if len(available_sources) > 5 else available_sources
        )

        # Advanced options in an expander
        with st.expander("Advanced Options"):
            show_anomalies = st.checkbox("Detect Anomalies", False)
            show_forecast = st.checkbox("Show Forecast", False)
            forecast_periods = st.slider("Forecast Periods", 3, 24, 12) if show_forecast else 12
            enable_download = st.checkbox("Enable Data Export", False)

        st.markdown("---")
        st.markdown("<div class='footer'>BetterSave Energy Analytics Platform</div>", unsafe_allow_html=True)

        return {
            "year_selection": year_selection,
            "month_selection": month_selection,
            "view_type": view_type,
            "selected_sources": selected_sources,
            "show_anomalies": show_anomalies,
            "show_forecast": show_forecast,
            "forecast_periods": forecast_periods,
            "enable_download": enable_download
        }

def render_kpi_section(metrics):
    """
    Render the KPI metrics section

    Args:
        metrics (dict): Dictionary of calculated metrics
    """
    render_header("Key Performance Indicators", "subheader")

    row1_col1, row1_col2, row1_col3, row1_col4 = st.columns([1, 1, 1, 1])

    with row1_col1:
        render_metric_card(
            "Total Consumption",
            f"{metrics.get('total_consumption', 0):,.0f} MWh",
            f"Peak: {metrics.get('peak_consumption', 0):,.0f} MWh"
        )

    with row1_col2:
        render_metric_card(
            "Total Generation",
            f"{metrics.get('total_generation', 0):,.0f} MWh",
            f"YoY Growth: {metrics.get('yoy_growth', 0):.1f}%",
            "secondary"
        )

    with row1_col3:
        render_metric_card(
            "Generation/Consumption",
            f"{metrics.get('efficiency_ratio', 0):.1f}%",
            "Higher is better",
            "secondary"
        )

    with row1_col4:
        render_metric_card(
            "Renewable Energy",
            f"{metrics.get('renewable_percentage', 0):.1f}%",
            "Of total generation",
            "accent"
        )

def render_energy_trends_tab(filtered_energy_gen, filtered_energy_cons, selected_sources, view_type, show_anomalies):
    """
    Render the Energy Trends tab content

    Args:
        filtered_energy_gen (DataFrame): Filtered generation data
        filtered_energy_cons (DataFrame): Filtered consumption data
        selected_sources (list): List of selected energy sources
        view_type (str): Data resolution
        show_anomalies (bool): Whether to show anomalies
    """
    render_header("Energy Consumption vs. Generation Over Time", "section-title")

    # Prepare data for visualization
    trends_data = prepare_trends_data(filtered_energy_cons, filtered_energy_gen, selected_sources, view_type)

    # Create melted dataframe for Plotly
    trends_melted = trends_data.melt(id_vars=["Date"], var_name="Type", value_name="MWh")

    # Create the visualization
    fig = create_trends_chart(trends_melted, view_type)

    # Detect anomalies if enabled
    if show_anomalies:
        anomalies = identify_anomalies(
            trends_data,
            "Consumption",
            window=30 if view_type == "Daily" else 7 if view_type == "Monthly" else 3,
            threshold=2.5
        )

        if not anomalies.empty:
            fig = add_anomalies_to_chart(fig, anomalies)

            render_info_card(
                f"<b>Detected {len(anomalies)} anomalies</b> in consumption data. These points deviate significantly from expected patterns and may indicate measurement errors or unusual consumption events.",
                "warning"
            )

    st.plotly_chart(fig, use_container_width=True)

    # Additional insights
    col1, col2 = st.columns(2)

    with col1:
        render_header("Consumption by Month", "section-title")

        # Aggregate data by month
        monthly_consumption = calculate_monthly_consumption(filtered_energy_cons)

        # Create bar chart
        fig_month = create_monthly_barchart(monthly_consumption)

        st.plotly_chart(fig_month, use_container_width=True)

    with col2:
        render_header("Day of Week Patterns", "section-title")

        # Aggregate data by day of week
        weekday_consumption = calculate_weekday_consumption(filtered_energy_cons)

        # Create bar chart
        fig_weekday = create_weekday_barchart(weekday_consumption)

        st.plotly_chart(fig_weekday, use_container_width=True)

    # Consumption vs generation ratio over time
    render_header("Generation to Consumption Ratio", "section-title")

    if view_type in ["Monthly", "Quarterly", "Yearly"]:
        # Calculate ratio
        trends_data["Ratio"] = (trends_data["Generation"] / trends_data["Consumption"]) * 100

        # Create line chart
        fig_ratio = create_ratio_chart(trends_data)

        st.plotly_chart(fig_ratio, use_container_width=True)

        # Add insight
        if trends_data["Ratio"].mean() < 100:
            render_info_card(
                f"<b>Energy Deficit:</b> On average, generation covers only {trends_data['Ratio'].mean():.1f}% of consumption needs during the selected period. Consider expanding renewable sources to close this gap.",
                "warning"
            )
        else:
            render_info_card(
                f"<b>Energy Surplus:</b> On average, generation exceeds consumption by {trends_data['Ratio'].mean() - 100:.1f}% during the selected period. This surplus could be stored or sold to the grid.",
                "info"
            )

def render_energy_sources_tab(filtered_energy_gen, selected_sources, view_type):
    """
    Render the Energy Sources tab content

    Args:
        filtered_energy_gen (DataFrame): Filtered generation data
        selected_sources (list): List of selected energy sources
        view_type (str): Data resolution
    """
    render_header("Energy Source Contribution", "section-title")

    # Calculate source totals
    source_data = calculate_source_totals(filtered_energy_gen, selected_sources)

    # Create tabs for different visualizations
    source_tab1, source_tab2, source_tab3 = st.tabs(["Pie Chart", "Bar Chart", "Time Series"])

    with source_tab1:
        # Create pie chart
        fig_pie = create_source_pie_chart(source_data)

        st.plotly_chart(fig_pie, use_container_width=True)

    with source_tab2:
        # Create bar chart
        fig_bar = create_source_bar_chart(source_data)

        st.plotly_chart(fig_bar, use_container_width=True)

    with source_tab3:
        # Prepare time series data by source
        time_series_data = prepare_source_time_series(filtered_energy_gen, selected_sources, view_type)

        # Determine the x-axis column based on view type
        if view_type == "Daily":
            x_col = "Date"
        elif view_type == "Monthly":
            x_col = "Date"
        elif view_type == "Quarterly":
            x_col = "Label"
        else:  # Yearly
            x_col = "Year"

        if x_col in time_series_data.columns:
            # Create time series chart
            fig_time = create_source_time_series(time_series_data, x_col, selected_sources, view_type)

            st.plotly_chart(fig_time, use_container_width=True)
        else:
            st.info(f"Insufficient data for time series visualization with {view_type} resolution.")

    # Energy source mix over time
    render_header("Energy Mix Evolution", "section-title")

    if view_type != "Daily":  # Area chart works better for aggregated data
        # Use the same time_series_data from above for the area chart
        if x_col in time_series_data.columns:
            # Create area chart
            from visualization import create_source_area_chart
            fig_area = create_source_area_chart(time_series_data, x_col, selected_sources, view_type)

            st.plotly_chart(fig_area, use_container_width=True)

            # Calculate the percentage change in sources
            if len(time_series_data) > 1:
                # Get first and last period data
                first_period = time_series_data.iloc[0]
                last_period = time_series_data.iloc[-1]

                # Calculate changes
                source_changes = {}
                for source in selected_sources:
                    if first_period[source] > 0:
                        change_pct = ((last_period[source] - first_period[source]) / first_period[source]) * 100
                        source_changes[source] = change_pct

                # Create dataframe for changes
                change_data = pd.DataFrame({
                    "Source": list(source_changes.keys()),
                    "Change (%)": list(source_changes.values())
                })

                if not change_data.empty:
                    # Create a bar chart of changes
                    from visualization import create_source_change_chart
                    fig_change = create_source_change_chart(change_data)

                    st.plotly_chart(fig_change, use_container_width=True)

                    # Add insights
                    fastest_growing = change_data.loc[change_data["Change (%)"].idxmax()]
                    fastest_declining = change_data.loc[change_data["Change (%)"].idxmin()]

                    col1, col2 = st.columns(2)

                    with col1:
                        if fastest_growing["Change (%)"] > 0:
                            render_info_card(
                                f"<b>Fastest Growing:</b> {fastest_growing['Source']} increased by {fastest_growing['Change (%)']:.1f}% from the first to last period.",
                                "info"
                            )

                    with col2:
                        if fastest_declining["Change (%)"] < 0:
                            render_info_card(
                                f"<b>Fastest Declining:</b> {fastest_declining['Source']} decreased by {abs(fastest_declining['Change (%)']):.1f}% from the first to last period.",
                                "warning"
                            )
        else:
            st.info("Insufficient data to display energy mix evolution. Try selecting a different view type or date range.")

def render_forecasting_tab(filtered_energy_cons, forecast_periods, show_forecast):
    """
    Render the Forecasting tab content

    Args:
        filtered_energy_cons (DataFrame): Filtered consumption data
        forecast_periods (int): Number of periods to forecast
        show_forecast (bool): Whether to show forecast
    """
    render_header("Energy Consumption Forecast", "section-title")

    if show_forecast:
        from analysis import forecast_energy_trends
        from visualization import create_forecast_chart

        # Generate forecast
        historical_data, forecast_data = forecast_energy_trends(filtered_energy_cons, periods=forecast_periods)

        if historical_data is not None and forecast_data is not None:
            # Create forecast chart
            fig_forecast = create_forecast_chart(historical_data, forecast_data)

            st.plotly_chart(fig_forecast, use_container_width=True)

            # Show forecast data in a table
            with st.expander("View Forecast Data"):
                forecast_df = pd.DataFrame({
                    "Date": forecast_data.index,
                    "Forecasted Consumption (MWh)": forecast_data.values
                })

                st.dataframe(forecast_df, use_container_width=True)

            # Add insights
            avg_historical = historical_data.mean()
            avg_forecast = forecast_data.mean()
            change_pct = ((avg_forecast - avg_historical) / avg_historical) * 100

            if change_pct > 0:
                render_info_card(
                    f"<b>Forecast Insight:</b> Average energy consumption is projected to <b>increase by {change_pct:.1f}%</b> in the forecast period compared to historical data.",
                    "info" if change_pct < 5 else "warning"
                )
            else:
                render_info_card(
                    f"<b>Forecast Insight:</b> Average energy consumption is projected to <b>decrease by {abs(change_pct):.1f}%</b> in the forecast period compared to historical data.",
                    "info"
                )
        else:
            st.warning("Insufficient historical data for generating a reliable forecast. Try selecting a longer date range.")
    else:
        st.info("Enable the 'Show Forecast' option in the sidebar to view consumption forecasts.")

def render_data_explorer_tab(filtered_energy_gen, filtered_energy_cons, enable_download):
    """
    Render the Data Explorer tab content

    Args:
        filtered_energy_gen (DataFrame): Filtered generation data
        filtered_energy_cons (DataFrame): Filtered consumption data
        enable_download (bool): Whether to enable data download
    """
    render_header("Data Tables and Export", "section-title")

    data_tab1, data_tab2 = st.tabs(["Consumption Data", "Generation Data"])

    with data_tab1:
        st.write(f"Showing {len(filtered_energy_cons)} records of consumption data")

        # Display data
        st.dataframe(filtered_energy_cons, use_container_width=True)

        # Download option
        if enable_download:
            csv = filtered_energy_cons.to_csv(index=False).encode('utf-8')
            st.download_button(
                "Download Consumption Data",
                data=csv,
                file_name="energy_consumption_filtered.csv",
                mime="text/csv",
            )

    with data_tab2:
        st.write(f"Showing {len(filtered_energy_gen)} records of generation data")

        # Display data
        st.dataframe(filtered_energy_gen, use_container_width=True)

        # Download option
        if enable_download:
            csv = filtered_energy_gen.to_csv(index=False).encode('utf-8')
            st.download_button(
                "Download Generation Data",
                data=csv,
                file_name="energy_generation_filtered.csv",
                mime="text/csv",
            )

    # Data summary
    with st.expander("Data Summary Statistics"):
        col1, col2 = st.columns(2)

        with col1:
            render_header("Consumption Summary", "section-title")
            st.dataframe(filtered_energy_cons["Total (grid load) [MWh] Calculated resolutions"].describe(), use_container_width=True)

        with col2:
            render_header("Generation Summary", "section-title")

            # Get generation columns
            gen_columns = [col for col in filtered_energy_gen.columns if '[MWh]' in col]

            # Calculate total generation
            filtered_energy_gen["Total Generation"] = filtered_energy_gen[gen_columns].sum(axis=1)

            st.dataframe(filtered_energy_gen["Total Generation"].describe(), use_container_width=True)
