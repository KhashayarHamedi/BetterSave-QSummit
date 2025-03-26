"""
analysis.py
Data analysis and visualization functions for the BetterSave Energy Dashboard
"""

import pandas as pd
import numpy as np
from datetime import timedelta
import streamlit as st

def analyze_energy_trends(energy_gen, energy_cons):
    """
    Calculate key metrics and trends from the energy data
    
    Args:
        energy_gen (DataFrame): Energy generation data
        energy_cons (DataFrame): Energy consumption data
        
    Returns:
        dict: Dictionary of calculated metrics
    """
    try:
        # Ensure numeric values
        energy_cons_numeric = energy_cons.select_dtypes(include=['number'])
        energy_gen_numeric = energy_gen.iloc[:, 3:].apply(pd.to_numeric, errors='coerce')

        # Calculate totals
        total_consumption = energy_cons_numeric["Total (grid load) [MWh] Calculated resolutions"].sum()

        # Get only the generation columns (excluding metadata columns)
        gen_columns = [col for col in energy_gen.columns if '[MWh]' in col]
        total_generation = energy_gen[gen_columns].apply(pd.to_numeric, errors='coerce').sum().sum()

        # Calculate efficiency
        efficiency_ratio = (total_generation / total_consumption) * 100 if total_consumption > 0 else 0

        # Calculate year-over-year growth
        consumption_by_year = energy_cons.groupby("Year")["Total (grid load) [MWh] Calculated resolutions"].sum()
        if len(consumption_by_year) > 1:
            # Calculate year-over-year growth for the most recent years
            years = sorted(consumption_by_year.index)
            if len(years) >= 2:
                current_year = years[-1]
                previous_year = years[-2]
                yoy_growth = ((consumption_by_year[current_year] / consumption_by_year[previous_year]) - 1) * 100
            else:
                yoy_growth = 0
        else:
            yoy_growth = 0

        # Calculate peak consumption
        peak_consumption = energy_cons["Total (grid load) [MWh] Calculated resolutions"].max()
        peak_date = energy_cons.loc[energy_cons["Total (grid load) [MWh] Calculated resolutions"].idxmax(), "Start date"]

        # Calculate renewable percentage
        renewable_columns = [col for col in gen_columns if any(source in col.lower() for source in ['solar', 'wind', 'hydro', 'biomass', 'geothermal'])]
        if renewable_columns:
            renewable_generation = energy_gen[renewable_columns].apply(pd.to_numeric, errors='coerce').sum().sum()
            renewable_percentage = (renewable_generation / total_generation) * 100 if total_generation > 0 else 0
        else:
            renewable_percentage = 0

        # Calculate seasonal patterns
        seasonal_consumption = energy_cons.groupby("Quarter")["Total (grid load) [MWh] Calculated resolutions"].mean()
        highest_quarter = seasonal_consumption.idxmax() if not seasonal_consumption.empty else None

        # Return all calculated metrics
        return {
            "total_consumption": total_consumption,
            "total_generation": total_generation,
            "efficiency_ratio": efficiency_ratio,
            "yoy_growth": yoy_growth,
            "peak_consumption": peak_consumption,
            "peak_date": peak_date,
            "renewable_percentage": renewable_percentage,
            "highest_quarter": highest_quarter,
            "consumption_by_year": consumption_by_year,
        }
    except Exception as e:
        st.error(f"Error in trend analysis: {e}")
        return {}

def forecast_energy_trends(df, periods=12):
    """
    Simple time series forecasting for energy trends
    
    Args:
        df (DataFrame): Energy consumption data
        periods (int, optional): Number of periods to forecast
        
    Returns:
        tuple: (historical_data, forecast_data)
    """
    try:
        # Get the last few years of data
        monthly_data = df.groupby(["Year", "Month"])["Total (grid load) [MWh] Calculated resolutions"].sum().reset_index()

        # Create a date column for time series analysis
        monthly_data["Date"] = pd.to_datetime(monthly_data[["Year", "Month"]].assign(Day=1))
        monthly_data = monthly_data.set_index("Date")["Total (grid load) [MWh] Calculated resolutions"]

        # Simple forecasting using last year's seasonal pattern
        if len(monthly_data) >= 12:
            # Get the trend from the last 12 months
            last_12_months = monthly_data[-12:]

            # Simple forecast: repeat the last 12 months with a small growth factor
            growth_factor = 1.02  # 2% annual growth assumption

            # Create forecast dates
            last_date = monthly_data.index[-1]
            forecast_dates = [last_date + timedelta(days=30*i) for i in range(1, periods+1)]

            # Create forecast values
            forecast_values = []
            for i in range(periods):
                month_index = i % 12
                forecast_values.append(last_12_months.iloc[month_index] * (growth_factor ** (i//12 + 1)))

            # Create forecast dataframe
            forecast = pd.Series(forecast_values, index=forecast_dates)

            return monthly_data, forecast
        return None, None
    except Exception as e:
        st.error(f"Error in forecasting: {e}")
        return None, None

def identify_anomalies(df, column, window=30, threshold=2):
    """
    Identify anomalies in the time series data
    
    Args:
        df (DataFrame): Data to analyze
        column (str): Column name to check for anomalies
        window (int, optional): Rolling window size
        threshold (float, optional): Standard deviation threshold
        
    Returns:
        DataFrame: DataFrame containing only the anomalies
    """
    try:
        # Create a copy of the dataframe
        df_copy = df.copy()

        # Calculate rolling mean and standard deviation
        rolling_mean = df_copy[column].rolling(window=window).mean()
        rolling_std = df_copy[column].rolling(window=window).std()

        # Define upper and lower bounds
        upper_bound = rolling_mean + (rolling_std * threshold)
        lower_bound = rolling_mean - (rolling_std * threshold)

        # Identify anomalies
        df_copy['anomaly'] = ((df_copy[column] > upper_bound) | (df_copy[column] < lower_bound))

        # Get anomalies
        anomalies = df_copy[df_copy['anomaly']]

        return anomalies
    except Exception as e:
        st.error(f"Error in anomaly detection: {e}")
        return pd.DataFrame()

def prepare_trends_data(filtered_energy_cons, filtered_energy_gen, selected_sources, view_type):
    """
    Prepare data for trend visualization based on view type
    
    Args:
        filtered_energy_cons (DataFrame): Filtered consumption data
        filtered_energy_gen (DataFrame): Filtered generation data
        selected_sources (list): List of selected energy sources
        view_type (str): Data resolution - "Daily", "Monthly", "Quarterly", or "Yearly"
        
    Returns:
        DataFrame: Prepared data for visualization
    """
    if view_type == "Daily":
        trends_data = pd.DataFrame({
            "Date": filtered_energy_cons["Start date"],
            "Consumption": filtered_energy_cons["Total (grid load) [MWh] Calculated resolutions"],
        })

        # Add generation data from all sources
        gen_columns = [f"{source} [MWh] Calculated resolutions" for source in selected_sources]
        gen_data = filtered_energy_gen[gen_columns].apply(pd.to_numeric, errors='coerce').sum(axis=1)
        trends_data["Generation"] = gen_data.values if len(gen_data) == len(trends_data) else np.nan

    elif view_type == "Monthly":
        cons_monthly = filtered_energy_cons.groupby(["Year", "Month"]).agg({
            "Start date": "first",
            "Total (grid load) [MWh] Calculated resolutions": "sum"
        }).reset_index()

        gen_columns = [f"{source} [MWh] Calculated resolutions" for source in selected_sources]
        gen_monthly = filtered_energy_gen.groupby(["Year", "Month"]).agg({
            "Start date": "first",
            **{col: "sum" for col in gen_columns}
        }).reset_index()

        trends_data = pd.DataFrame({
            "Date": cons_monthly["Start date"],
            "Consumption": cons_monthly["Total (grid load) [MWh] Calculated resolutions"],
            "Generation": gen_monthly[gen_columns].sum(axis=1) if not gen_monthly.empty else np.nan
        })

    elif view_type == "Quarterly":
        cons_quarterly = filtered_energy_cons.groupby(["Year", "Quarter"]).agg({
            "Total (grid load) [MWh] Calculated resolutions": "sum"
        }).reset_index()

        gen_columns = [f"{source} [MWh] Calculated resolutions" for source in selected_sources]
        gen_quarterly = filtered_energy_gen.groupby(["Year", "Quarter"]).agg({
            **{col: "sum" for col in gen_columns}
        }).reset_index()

        # Create date labels for quarters
        cons_quarterly["Date"] = cons_quarterly.apply(lambda x: f"{int(x['Year'])} Q{int(x['Quarter'])}", axis=1)
        gen_quarterly["Date"] = gen_quarterly.apply(lambda x: f"{int(x['Year'])} Q{int(x['Quarter'])}", axis=1)

        # Merge dataframes
        trends_data = pd.DataFrame({
            "Date": cons_quarterly["Date"],
            "Consumption": cons_quarterly["Total (grid load) [MWh] Calculated resolutions"],
            "Generation": gen_quarterly[gen_columns].sum(axis=1) if not gen_quarterly.empty else np.nan
        })

    else:  # Yearly
        cons_yearly = filtered_energy_cons.groupby("Year").agg({
            "Total (grid load) [MWh] Calculated resolutions": "sum"
        }).reset_index()

        gen_columns = [f"{source} [MWh] Calculated resolutions" for source in selected_sources]
        gen_yearly = filtered_energy_gen.groupby("Year").agg({
            **{col: "sum" for col in gen_columns}
        }).reset_index()

        trends_data = pd.DataFrame({
            "Date": cons_yearly["Year"].astype(str),
            "Consumption": cons_yearly["Total (grid load) [MWh] Calculated resolutions"],
            "Generation": gen_yearly[gen_columns].sum(axis=1) if not gen_yearly.empty else np.nan
        })
        
    return trends_data

def calculate_monthly_consumption(filtered_energy_cons):
    """
    Calculate average consumption by month
    
    Args:
        filtered_energy_cons (DataFrame): Filtered consumption data
        
    Returns:
        DataFrame: Monthly consumption data
    """
    # Aggregate data by month
    monthly_consumption = filtered_energy_cons.groupby("Month").agg({
        "Total (grid load) [MWh] Calculated resolutions": "mean",
        "MonthName": "first"
    }).reset_index()

    # Sort by month
    monthly_consumption = monthly_consumption.sort_values("Month")
    
    return monthly_consumption

def calculate_weekday_consumption(filtered_energy_cons):
    """
    Calculate average consumption by day of week
    
    Args:
        filtered_energy_cons (DataFrame): Filtered consumption data
        
    Returns:
        DataFrame: Weekday consumption data
    """
    # Aggregate data by day of week
    weekday_consumption = filtered_energy_cons.groupby("WeekDay").agg({
        "Total (grid load) [MWh] Calculated resolutions": "mean"
    }).reset_index()

    # Define weekday order
    weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    # Sort by weekday
    weekday_consumption["WeekDay"] = pd.Categorical(
        weekday_consumption["WeekDay"],
        categories=weekday_order,
        ordered=True
    )
    weekday_consumption = weekday_consumption.sort_values("WeekDay")
    
    return weekday_consumption

def calculate_source_totals(filtered_energy_gen, selected_sources):
    """
    Calculate total generation by source
    
    Args:
        filtered_energy_gen (DataFrame): Filtered generation data
        selected_sources (list): List of selected energy sources
        
    Returns:
        DataFrame: Source totals data
    """
    # Get generation data for the selected sources
    gen_columns = [f"{source} [MWh] Calculated resolutions" for source in selected_sources]

    # Calculate total generation by source
    source_totals = filtered_energy_gen[gen_columns].apply(pd.to_numeric, errors='coerce').sum()
    source_totals.index = [idx.replace(" [MWh] Calculated resolutions", "") for idx in source_totals.index]

    # Create a DataFrame for plotting
    source_data = pd.DataFrame({
        "Source": source_totals.index,
        "Generation (MWh)": source_totals.values
    })
    
    return source_data

def prepare_source_time_series(filtered_energy_gen, selected_sources, view_type):
    """
    Prepare time series data by source
    
    Args:
        filtered_energy_gen (DataFrame): Filtered generation data
        selected_sources (list): List of selected energy sources
        view_type (str): Data resolution
        
    Returns:
        DataFrame: Time series data by source
    """
    # Create an empty DataFrame for the time series
    time_series_data = pd.DataFrame()

    if view_type == "Daily":
        # Group by date
        for source in selected_sources:
            column = f"{source} [MWh] Calculated resolutions"
            source_data = filtered_energy_gen.groupby("Start date")[column].sum()
            time_series_data[source] = source_data

        time_series_data = time_series_data.reset_index()
        time_series_data.rename(columns={"Start date": "Date"}, inplace=True)

    elif view_type == "Monthly":
        # Group by year and month
        for source in selected_sources:
            column = f"{source} [MWh] Calculated resolutions"
            source_data = filtered_energy_gen.groupby(["Year", "Month"])[column].sum().reset_index()
            source_data["Date"] = pd.to_datetime(source_data[["Year", "Month"]].assign(Day=1))

            if "Date" not in time_series_data.columns:
                time_series_data["Date"] = source_data["Date"]

            time_series_data[source] = source_data[column].values

    elif view_type == "Quarterly":
        # Group by year and quarter
        for source in selected_sources:
            column = f"{source} [MWh] Calculated resolutions"
            source_data = filtered_energy_gen.groupby(["Year", "Quarter"])[column].sum().reset_index()
            source_data["Label"] = source_data.apply(lambda x: f"{int(x['Year'])} Q{int(x['Quarter'])}", axis=1)

            if "Label" not in time_series_data.columns:
                time_series_data["Label"] = source_data["Label"]

            time_series_data[source] = source_data[column].values

    else:  # Yearly
        # Group by year
        for source in selected_sources:
            column = f"{source} [MWh] Calculated resolutions"
            source_data = filtered_energy_gen.groupby("Year")[column].sum().reset_index()

            if "Year" not in time_series_data.columns:
                time_series_data["Year"] = source_data["Year"]

            time_series_data[source] = source_data[column].values
    
    return time_series_data
