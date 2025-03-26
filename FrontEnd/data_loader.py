"""
data_loader.py
Functions for loading and processing data for the BetterSave Energy Dashboard
"""

import os
import pandas as pd
import streamlit as st

# Load Data with improved error handling and flexible path resolution
@st.cache_data(ttl=3600)
def load_data():
    """
    Load and preprocess energy generation and consumption data

    Returns:
        tuple: (energy_generation_df, energy_consumption_df)
    """
    try:
        # Get the current script directory
        script_dir = os.path.dirname(__file__)

        # Try multiple possible locations for the data files
        possible_locations = [
            script_dir,                      # Same directory as script
            os.path.join(script_dir, '..'),  # Parent directory
            os.path.join(script_dir, 'data'), # data subdirectory
            os.path.join(script_dir, '..', 'data'), # data directory at parent level
            os.path.join(script_dir, '..', '..', 'data'), # data directory two levels up
        ]

        gen_file_name = "energy_generation_preprocessed.csv"
        cons_file_name = "energy_consumption_preprocessed.csv"

        gen_file_path = None
        cons_file_path = None

        # Find the data files
        for loc in possible_locations:
            gen_path = os.path.join(loc, gen_file_name)
            cons_path = os.path.join(loc, cons_file_name)

            if os.path.exists(gen_path):
                gen_file_path = gen_path

            if os.path.exists(cons_path):
                cons_file_path = cons_path

            # If both files found, break the loop
            if gen_file_path and cons_file_path:
                break

        # If files not found, raise an error
        if not gen_file_path:
            raise FileNotFoundError(f"Could not find {gen_file_name} in any of the expected locations")
        if not cons_file_path:
            raise FileNotFoundError(f"Could not find {cons_file_name} in any of the expected locations")

        # Load the data
        energy_gen = pd.read_csv(gen_file_path)
        energy_cons = pd.read_csv(cons_file_path)

        # Convert dates and handle errors
        energy_gen["Start date"] = pd.to_datetime(energy_gen["Start date"], errors="coerce")
        energy_gen["End date"] = pd.to_datetime(energy_gen["End date"], errors="coerce")
        energy_cons["Start date"] = pd.to_datetime(energy_cons["Start date"], errors="coerce")

        # Add datetime components for more granular analysis
        for df in [energy_gen, energy_cons]:
            df["Year"] = df["Start date"].dt.year
            df["Month"] = df["Start date"].dt.month
            df["Day"] = df["Start date"].dt.day
            df["WeekDay"] = df["Start date"].dt.day_name()
            df["Quarter"] = df["Start date"].dt.quarter
            df["MonthName"] = df["Start date"].dt.month_name()

            # Create a unique ID for each record
            df.insert(0, "ID", range(1, len(df) + 1))

        st.success(f"Successfully loaded data from {os.path.dirname(gen_file_path)}")
        return energy_gen, energy_cons
    except Exception as e:
        st.error(f"Error loading data: {e}")
        # Print out the directories that were checked
        for loc in possible_locations:
            st.info(f"Checked location: {loc}")
        return pd.DataFrame(), pd.DataFrame()

@st.cache_data(ttl=3600)
def load_prediction_data():
    """
    Load and preprocess energy prediction data from CSV

    Returns:
        DataFrame: Energy prediction dataframe
    """
    try:
        # Get the current script directory
        script_dir = os.path.dirname(__file__)

        # Try multiple possible locations for the prediction file
        possible_locations = [
            script_dir,                      # Same directory as script
            os.path.join(script_dir, '..'),  # Parent directory
            os.path.join(script_dir, 'data'), # data subdirectory
            os.path.join(script_dir, '..', 'data'), # data directory at parent level
            os.path.join(script_dir, '..', '..', 'data'), # data directory two levels up
        ]

        pred_file_name = "365_day_predictions.csv"
        pred_file_path = None

        # Find the prediction file
        for loc in possible_locations:
            path = os.path.join(loc, pred_file_name)
            if os.path.exists(path):
                pred_file_path = path
                break

        # If file not found, raise an error
        if not pred_file_path:
            # List all files in the script directory to help debugging
            files_in_script_dir = os.listdir(script_dir)
            raise FileNotFoundError(f"Could not find {pred_file_name}. Files in script dir: {files_in_script_dir}")

        # Load the prediction data
        energy_pred = pd.read_csv(pred_file_path)

        # Process dates if they exist
        if "Date" in energy_pred.columns:
            energy_pred["Date"] = pd.to_datetime(energy_pred["Date"], errors="coerce")
            # Add datetime components if needed
            energy_pred["Year"] = energy_pred["Date"].dt.year
            energy_pred["Month"] = energy_pred["Date"].dt.month
            energy_pred["MonthName"] = energy_pred["Date"].dt.strftime('%b')
        else:
            # If no date column, create one
            energy_pred["Date"] = pd.date_range(start="2020-01-01", periods=len(energy_pred), freq="D")
            energy_pred["Year"] = energy_pred["Date"].dt.year
            energy_pred["Month"] = energy_pred["Date"].dt.month
            energy_pred["MonthName"] = energy_pred["Date"].dt.strftime('%b')

        # Ensure forecast column exists with a standard name
        if "forecast" in energy_pred.columns:
            pass
        elif "Residual load" in energy_pred.columns:
            energy_pred["forecast"] = energy_pred["Residual load"]
        elif "prediction" in energy_pred.columns:
            energy_pred["forecast"] = energy_pred["prediction"]
        elif energy_pred.shape[1] >= 2:  # If there are at least 2 columns
            # Assume the second column contains the prediction values
            forecast_col = energy_pred.columns[1]
            energy_pred["forecast"] = energy_pred[forecast_col]
            st.info(f"Using column '{forecast_col}' as forecast values")

        # Add model identifier
        energy_pred["model"] = "CSV Model"

        st.success(f"Successfully loaded prediction data from {pred_file_path}")
        return energy_pred
    except Exception as e:
        st.error(f"Error loading prediction data: {e}")
        return pd.DataFrame()

def filter_data(energy_generation, energy_consumption, year_selection, month_selection, selected_sources):
    """
    Filter data based on year and month selections

    Args:
        energy_generation (DataFrame): Energy generation data
        energy_consumption (DataFrame): Energy consumption data
        year_selection (tuple): (min_year, max_year)
        month_selection (list): List of selected months
        selected_sources (list): List of selected energy sources

    Returns:
        tuple: (filtered_energy_generation, filtered_energy_consumption)
    """
    filtered_energy_gen = energy_generation[
        (energy_generation["Year"] >= year_selection[0]) &
        (energy_generation["Year"] <= year_selection[1]) &
        (energy_generation["Month"].isin(month_selection))
    ]

    filtered_energy_cons = energy_consumption[
        (energy_consumption["Year"] >= year_selection[0]) &
        (energy_consumption["Year"] <= year_selection[1]) &
        (energy_consumption["Month"].isin(month_selection))
    ]

    return filtered_energy_gen, filtered_energy_cons

def get_date_range_values(energy_generation, energy_consumption):
    """
    Get minimum and maximum years from the data

    Returns:
        tuple: (min_year, max_year)
    """
    min_year = int(min(energy_consumption["Year"].min(), energy_generation["Year"].min()))
    max_year = int(max(energy_consumption["Year"].max(), energy_generation["Year"].max()))

    return min_year, max_year

def get_energy_sources(energy_generation):
    """
    Extract available energy sources from the generation data

    Returns:
        list: List of energy source names
    """
    available_sources = [col.replace(" [MWh] Calculated resolutions", "")
                        for col in energy_generation.columns if "[MWh]" in col]

    return available_sources
    
def filter_data(energy_generation, energy_consumption, year_selection, month_selection, selected_sources):
    """
    Filter the energy generation and consumption data based on the selected year range and months.

    Args:
        energy_generation (DataFrame): The energy generation data.
        energy_consumption (DataFrame): The energy consumption data.
        year_selection (tuple): A tuple of (min_year, max_year) for filtering.
        month_selection (list): A list of month numbers to include.
        selected_sources (list): List of selected energy sources (not used for filtering here).

    Returns:
        tuple: (filtered_energy_generation, filtered_energy_consumption)
    """
    filtered_energy_cons = energy_consumption[
        (energy_consumption["Year"] >= year_selection[0]) &
        (energy_consumption["Year"] <= year_selection[1]) &
        (energy_consumption["Month"].isin(month_selection))
    ]

    filtered_energy_gen = energy_generation[
        (energy_generation["Year"] >= year_selection[0]) &
        (energy_generation["Year"] <= year_selection[1]) &
        (energy_generation["Month"].isin(month_selection))
    ]

    return filtered_energy_gen, filtered_energy_cons
