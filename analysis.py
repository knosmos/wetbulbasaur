import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager


def calculate_wetbulb(
    temp: np.ndarray, humidity: np.ndarray
) -> np.ndarray:
    """
    Calculates the wet bulb temperature.
    Parameters:
        temp (np.ndarray): Array of air temperatures in degrees Celsius.
        humidity (np.ndarray): Array of humidity percentages
        dew_point (np.ndarray): Array of dew point temperatures in degrees Celsius.
    """

    # assume humidity is relative humidity in percentage
    if not (
        isinstance(temp, np.ndarray)
        and isinstance(humidity, np.ndarray)
        #and isinstance(dew_point, np.ndarray)
    ):
        raise ValueError("Input parameters must be numpy arrays.")
    if temp.shape != humidity.shape:# or temp.shape != dew_point.shape:
        raise ValueError("Input arrays must have the same shape.")

    Tw = (
        temp * np.arctan(0.151977 * np.sqrt(humidity + 8.313659))
        + 0.00391838 * np.sqrt(humidity) ** 3 * np.arctan(0.023101 * humidity)
        - np.arctan(humidity - 1.676331)
        + np.arctan(temp + humidity)
        - 4.686035
    )
    return Tw


def run_wetbulb_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """
    Runs the wet bulb temperature analysis on the DataFrame.

    Parameters:
        df (DataFrame): The DataFrame containing the data.

    Returns:
        DataFrame: The DataFrame with an additional column for wet bulb temperature.
    """
    if (
        "outdoor_temperature" not in df.columns
        or "outdoor_humidity" not in df.columns
    ):
        raise ValueError(
            "DataFrame must contain 'outdoor_temperature', 'outdoor_humidity', and 'dew_point' columns."
        )

    # some of the temperature data seems to be in Fahrenheit, convert to Celsius
    df["outdoor_temperature"] = np.where(
        df["outdoor_temperature"] > 50,
        (df["outdoor_temperature"] - 32) * 5 / 9,
        df["outdoor_temperature"],
    )

    df["wet_bulb"] = calculate_wetbulb(
        df["outdoor_temperature"].values,
        df["outdoor_humidity"].values,
        #df["dew_point"].values,
    )
    return df


def plot_data(df, station_id) -> None:
    """
    Plots the data for a specific station.

    Parameters:
        df (DataFrame): The DataFrame containing the data.
        station_id (str): The ID of the station to plot.

    Returns:
        None
    """
    station_data = df[df["station_id"] == station_id]

    if station_data.empty:
        print(f"No data found for station ID: {station_id}")
        return


    font_path = "WWF.otf"
    font_manager.fontManager.addfont(font_path)
    prop = font_manager.FontProperties(fname=font_path)

    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.sans-serif"] = prop.get_name()

    plt.figure(figsize=(10, 5))
    plt.style.use('https://github.com/dhaitz/matplotlib-stylesheets/raw/master/pitayasmoothie-light.mplstyle')
    plt.rcParams.update({"font.family": "Segoe UI", "font.size": 10})
    plt.axhline(y=30,  linewidth=1, linestyle="--")
    plt.axhline(y=35,  linewidth=1, linestyle="--")

    station_data["event_time"] = pd.to_datetime(
        station_data["event_time"], utc=True, yearfirst=True, format="%Y-%m-%d %H:%M:%S UTC"
    )
    station_data = station_data.sort_values(by="event_time")

    # collapse into daily stats
    daily_stats = station_data.groupby(station_data["event_time"].dt.date).agg(
        {
            "wet_bulb": ["mean", "min", "max"],
            "outdoor_temperature": ["mean", "min", "max"],
            "outdoor_humidity": ["mean", "min", "max"],
        }
    )
    daily_stats.columns = [
        "wet_bulb_mean",
        "wet_bulb_min",
        "wet_bulb_max",
        "outdoor_temperature_mean",
        "outdoor_temperature_min",
        "outdoor_temperature_max",
        "outdoor_humidity_mean",
        "outdoor_humidity_min",
        "outdoor_humidity_max",
    ]
    daily_stats = daily_stats.reset_index()
    plt.plot(
        daily_stats["event_time"],
        daily_stats["wet_bulb_mean"],
        label="Wet Bulb Mean",
        linewidth=1,
        #   color="#0081a7",
    )
    plt.fill_between(
        daily_stats["event_time"],
        daily_stats["wet_bulb_min"],
        daily_stats["wet_bulb_max"],
        #color="#00afb9",
        alpha=0.3,
    )

    #plt.scatter(times, station_data["wet_bulb"])
    print(f"Station {station_id}: {len(station_data)}")
    plt.title(f"Station {station_id}".upper(), fontfamily=prop.get_name(), fontsize=20)
    plt.xlabel("Timestamp")
    plt.ylabel("Wet Bulb Temperature (°C)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"plots/station_{station_id}.png", dpi=300)
    # plt.show()


def plot_datas(df) -> None:
    plt.style.use("ggplot")
    plt.rcParams.update({"font.family": "Segoe UI", "font.size": 6})
    fig, axs = plt.subplots(5, 5, figsize=(40, 35), constrained_layout=True)
    for i, station_id in enumerate(df["station_id"].unique()):
        ax = axs[i // 5, i % 5]
        station_data = df[df["station_id"] == station_id]
        if not station_data.empty:
            times = pd.to_datetime(station_data["event_time"])
            station_data["event_time"] = pd.to_datetime(station_data["event_time"])
            station_data = station_data.sort_values(by="event_time")
            ax.plot(
                times,
                station_data["wet_bulb"],
                label=f"Station {station_id}",
                linewidth=0.5,
                color="darkblue",
            )
            ax.tick_params(axis="x", rotation=45)
            ax.set_ylim(0, 40)
            ax.axhline(y=30, color="black", linewidth=0.5, linestyle="--")
            ax.axhline(y=35, color="red", linewidth=0.5, linestyle="--")
            ax.set_title(f"Station {station_id}")
            ax.set_xlabel("Timestamp")
            ax.set_ylabel("Wet Bulb Temperature (°C)")
        else:
            ax.set_title(f"Station {station_id} - No Data")
    # plt.tight_layout(pad=2.0)
    plt.show()


if __name__ == "__main__":
    DATA_FILE = "data_full.csv"
    df = pd.read_csv(DATA_FILE)
    df = run_wetbulb_analysis(df)
    print(max(df["wet_bulb"]))
    print(df["station_id"].nunique())  # Print the number of unique stations
    # number of unique stations
    for station_id in df["station_id"].unique():
        print(f"Station {station_id}: {len(df[df['station_id'] == station_id])} records")
        plot_data(df, station_id)
    #plot_datas(df)
