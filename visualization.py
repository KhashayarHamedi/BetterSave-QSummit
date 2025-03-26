"""
visualization.py
Visualization functions for the BetterSave Energy Dashboard using Plotly
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Webflow theme color palette
COLORS = {
    "primary": "#6c72ff",      # --accent--primary-1
    "secondary": "#57c3ff",    # --secondary--color-3
    "tertiary": "#9a91fb",     # --secondary--color-2
    "accent": "#fdb52a",       # --secondary--color-5
    "neutral": "#343b4f",      # --secondary--color-4
    "bg_primary": "#101935",   # --secondary--color-1
    "bg_transparent": "rgba(16, 25, 53, 0)",  # Transparent version of --secondary--color-1
    "text": "#aeb9e1",         # --neutral--400
    "grid": "rgba(55, 68, 107, 0.5)",  # --neutral--600 with transparency
    "green": "#14ca74",        # --system--green-300
    "red": "#ff5a65"           # --system--300
}

# Default plot settings to match Webflow theme
def default_layout(fig, title="", x_title="", y_title="", height=500):
    """
    Apply default Webflow theme styling to a Plotly figure
    
    Args:
        fig (Figure): Plotly figure to style
        title (str, optional): Chart title
        x_title (str, optional): X-axis title
        y_title (str, optional): Y-axis title
        height (int, optional): Chart height
        
    Returns:
        Figure: Styled Plotly figure
    """
    fig.update_layout(
        title=title,
        xaxis_title=x_title,
        yaxis_title=y_title,
        height=height,
        template="plotly_dark",
        plot_bgcolor=COLORS["bg_primary"],
        paper_bgcolor=COLORS["bg_transparent"],
        font=dict(color=COLORS["text"]),
        xaxis=dict(gridcolor=COLORS["grid"]),
        yaxis=dict(gridcolor=COLORS["grid"]),
        hovermode="x unified"
    )
    return fig

def create_trends_chart(trends_melted, view_type):
    """
    Create a line chart for energy trends
    
    Args:
        trends_melted (DataFrame): Melted dataframe for plotting
        view_type (str): Data resolution
        
    Returns:
        Figure: Plotly figure
    """
    fig = px.line(
        trends_melted,
        x="Date",
        y="MWh",
        color="Type",
        title=f"{view_type} Energy Trends",
        markers=True,
        template="plotly_dark",
        color_discrete_map={
            "Consumption": COLORS["secondary"],
            "Generation": COLORS["primary"]
        }
    )
    
    fig = default_layout(
        fig,
        x_title="Time Period",
        y_title="Energy (MWh)",
        height=500
    )
    
    # If using daily or monthly view, format x-axis
    if view_type in ["Daily", "Monthly"]:
        fig.update_xaxes(
            tickformat="%b %Y" if view_type == "Monthly" else "%d %b %Y",
            tickangle=45
        )
    
    return fig

def add_anomalies_to_chart(fig, anomalies):
    """
    Add anomaly markers to an existing chart
    
    Args:
        fig (Figure): Existing Plotly figure
        anomalies (DataFrame): DataFrame containing anomalies
        
    Returns:
        Figure: Updated Plotly figure with anomalies
    """
    fig.add_trace(
        go.Scatter(
            x=anomalies["Date"],
            y=anomalies["Consumption"],
            mode="markers",
            marker=dict(
                symbol="circle",
                size=12,
                color=COLORS["red"],
                line=dict(width=2, color=COLORS["red"])
            ),
            name="Anomalies"
        )
    )
    return fig

def create_monthly_barchart(monthly_consumption):
    """
    Create a bar chart for monthly consumption
    
    Args:
        monthly_consumption (DataFrame): Monthly consumption data
        
    Returns:
        Figure: Plotly figure
    """
    fig = px.bar(
        monthly_consumption,
        x="MonthName",
        y="Total (grid load) [MWh] Calculated resolutions",
        title="Average Consumption by Month",
        template="plotly_dark",
        color="Total (grid load) [MWh] Calculated resolutions",
        color_continuous_scale=[COLORS["neutral"], COLORS["secondary"]]
    )
    
    fig = default_layout(
        fig,
        x_title="Month",
        y_title="Average Consumption (MWh)"
    )
    
    fig.update_layout(coloraxis_showscale=False)
    
    return fig

def create_weekday_barchart(weekday_consumption):
    """
    Create a bar chart for weekday consumption
    
    Args:
        weekday_consumption (DataFrame): Weekday consumption data
        
    Returns:
        Figure: Plotly figure
    """
    fig = px.bar(
        weekday_consumption,
        x="WeekDay",
        y="Total (grid load) [MWh] Calculated resolutions",
        title="Average Consumption by Day of Week",
        template="plotly_dark",
        color="Total (grid load) [MWh] Calculated resolutions",
        color_continuous_scale=[COLORS["primary"], COLORS["tertiary"]]
    )
    
    fig = default_layout(
        fig, 
        x_title="Day of Week",
        y_title="Average Consumption (MWh)"
    )
    
    fig.update_layout(coloraxis_showscale=False)
    
    return fig

def create_ratio_chart(trends_data):
    """
    Create a line chart for generation to consumption ratio
    
    Args:
        trends_data (DataFrame): Trends data with ratio column
        
    Returns:
        Figure: Plotly figure
    """
    fig = px.line(
        trends_data,
        x="Date",
        y="Ratio",
        title="Generation to Consumption Ratio (%)",
        template="plotly_dark",
        markers=True,
        color_discrete_sequence=[COLORS["accent"]]
    )
    
    # Add a reference line at 100%
    fig.add_hline(
        y=100,
        line_dash="dash",
        line_color=COLORS["green"],
        annotation_text="100% (Generation equals Consumption)",
        annotation_position="bottom right"
    )
    
    fig = default_layout(
        fig,
        x_title="Time Period",
        y_title="Ratio (%)",
        height=400
    )
    
    return fig

def create_source_pie_chart(source_data):
    """
    Create a pie chart for energy generation by source
    
    Args:
        source_data (DataFrame): Source totals data
        
    Returns:
        Figure: Plotly figure
    """
    fig = px.pie(
        source_data,
        names="Source",
        values="Generation (MWh)",
        title="Total Energy Generation by Source",
        template="plotly_dark",
        hole=0.4,
        color_discrete_sequence=[
            COLORS["primary"], 
            COLORS["secondary"], 
            COLORS["tertiary"], 
            COLORS["accent"], 
            COLORS["neutral"]
        ]
    )
    
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        marker=dict(line=dict(color=COLORS["bg_primary"], width=1))
    )
    
    fig.update_layout(
        height=500,
        paper_bgcolor=COLORS["bg_transparent"],
        font=dict(color=COLORS["text"])
    )
    
    return fig

def create_source_bar_chart(source_data):
    """
    Create a bar chart for energy generation by source
    
    Args:
        source_data (DataFrame): Source totals data
        
    Returns:
        Figure: Plotly figure
    """
    fig = px.bar(
        source_data.sort_values("Generation (MWh)", ascending=False),
        x="Source",
        y="Generation (MWh)",
        title="Energy Generation by Source",
        template="plotly_dark",
        color="Source",
        color_discrete_sequence=[
            COLORS["primary"], 
            COLORS["secondary"], 
            COLORS["tertiary"], 
            COLORS["accent"], 
            COLORS["neutral"]
        ]
    )
    
    fig = default_layout(
        fig,
        x_title="Energy Source",
        y_title="Total Generation (MWh)",
        height=500
    )
    
    return fig

def create_source_time_series(time_series_data, x_col, selected_sources, view_type):
    """
    Create a line chart for time series by source
    
    Args:
        time_series_data (DataFrame): Time series data
        x_col (str): Column to use for x-axis
        selected_sources (list): List of selected sources
        view_type (str): Data resolution
        
    Returns:
        Figure: Plotly figure
    """
    fig = px.line(
        time_series_data,
        x=x_col,
        y=selected_sources,
        title=f"{view_type} Generation by Source",
        template="plotly_dark",
        markers=True,
        color_discrete_sequence=[
            COLORS["primary"], 
            COLORS["secondary"], 
            COLORS["tertiary"], 
            COLORS["accent"], 
            COLORS["neutral"]
        ]
    )
    
    # Format x-axis for date types
    if x_col == "Date":
        fig.update_xaxes(
            tickformat="%b %Y",
            tickangle=45
        )
    elif x_col == "Start date":
        fig.update_xaxes(
            tickformat="%d %b %Y",
            tickangle=45
        )
    
    fig = default_layout(
        fig,
        x_title="Time Period",
        y_title="Generation (MWh)",
        height=500
    )
    
    fig.update_layout(legend_title="Energy Source")
    
    return fig

def create_source_area_chart(area_data, x_col, selected_sources, view_type):
    """
    Create an area chart for energy source mix evolution
    
    Args:
        area_data (DataFrame): Data for area chart
        x_col (str): Column to use for x-axis
        selected_sources (list): List of selected sources
        view_type (str): Data resolution
        
    Returns:
        Figure: Plotly figure
    """
    fig = px.area(
        area_data,
        x=x_col,
        y=selected_sources,
        title=f"Energy Source Mix Evolution ({view_type})",
        template="plotly_dark",
        color_discrete_sequence=[
            COLORS["primary"], 
            COLORS["secondary"], 
            COLORS["tertiary"], 
            COLORS["accent"], 
            COLORS["neutral"]
        ]
    )
    
    # Format x-axis for date types
    if x_col == "Date":
        fig.update_xaxes(
            tickformat="%b %Y",
            tickangle=45
        )
    
    fig = default_layout(
        fig,
        x_title="Time Period",
        y_title="Generation (MWh)",
        height=500
    )
    
    fig.update_layout(legend_title="Energy Source")
    
    return fig

def create_source_change_chart(change_data):
    """
    Create a bar chart for source growth rates
    
    Args:
        change_data (DataFrame): Source change data
        
    Returns:
        Figure: Plotly figure
    """
    fig = px.bar(
        change_data.sort_values("Change (%)", ascending=False),
        x="Source",
        y="Change (%)",
        title="Source Growth: First to Last Period",
        template="plotly_dark",
        color="Change (%)",
        color_continuous_scale=[COLORS["red"], COLORS["text"], COLORS["green"]],
        color_continuous_midpoint=0
    )
    
    fig = default_layout(
        fig,
        x_title="Energy Source",
        y_title="Change (%)",
        height=400
    )
    
    return fig

def create_forecast_chart(historical_data, forecast_data, title="Energy Consumption Forecast"):
    """
    Create a chart with historical data and forecast
    
    Args:
        historical_data (Series): Historical time series data
        forecast_data (Series): Forecast time series data
        title (str, optional): Chart title
        
    Returns:
        Figure: Plotly figure
    """
    fig = go.Figure()
    
    # Add historical data
    fig.add_trace(
        go.Scatter(
            x=historical_data.index,
            y=historical_data.values,
            mode='lines+markers',
            name='Historical Data',
            line=dict(color=COLORS["secondary"], width=2)
        )
    )
    
    # Add forecast data
    fig.add_trace(
        go.Scatter(
            x=forecast_data.index,
            y=forecast_data.values,
            mode='lines+markers',
            name='Forecast',
            line=dict(
                color=COLORS["accent"],
                width=2,
                dash='dash'
            )
        )
    )
    
    # Add vertical line at the split between historical and forecast
    split_date = historical_data.index[-1]
    fig.add_vline(
        x=split_date, 
        line_width=1, 
        line_dash="dash", 
        line_color=COLORS["text"],
        annotation_text="Forecast Start", 
        annotation_position="top right"
    )
    
    fig = default_layout(
        fig,
        title=title,
        x_title="Date",
        y_title="Energy (MWh)",
        height=500
    )
    
    fig.update_xaxes(
        tickformat="%b %Y",
        tickangle=45
    )
    
    return fig
