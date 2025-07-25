# wetbulbasaur

> A wet bulb is a thermometer in which the bulb is wrapped in a wet cloth. It can be used to measure the lowest temperature to which air can be cooled by evaporating water at constant pressure. Basically, it is a metaphor for human sweat and it will tell you how the human body would feel in direct sunlight.
>
> Quite comfortable wet-bulb temperature is around 70 °F (22 °C), but no more than 86 °F (30 °C). Above this temperature, physical labor becomes impossible. The higher the wet-bulb temperature, the higher the risk of severe heat stress.
> 
> A wet-bulb temperature of 35°C (95°F) is considered the theoretical threshold for human survival, as it represents the point where the body can no longer effectively cool itself through sweating. However, recent research suggests this limit may be lower, with some studies indicating that a wet-bulb temperature of 31°C (88°F) can be dangerous even for young, healthy individuals. 

<table>
  <tr>
    <td><img width="3000" height="1500" alt="image" src="https://github.com/user-attachments/assets/8a70e5db-42ca-4189-bdd6-01d2f3106cef" /></td>
    <td><img width="3000" height="1500" alt="image" src="https://github.com/user-attachments/assets/05f8c540-c9c5-419c-9851-5b5f5cf539ee" /></td>
  </tr>
</table>

## Formula
``` math
\begin{align*}
T_w&=T\,\tan^{-1}(0.151977\sqrt{H_r+8.313659})\\
&+0.00391838\,\sqrt{H_r}^3 \,\tan^{-1}(0.023101H_r)\\
&−\tan^{-1}(H_r−1.676331)\\
&+\tan^{-1}(T+H_r)\\
&−4.686035
\end{align*}
```
where $T_w$, $T$, and $H_r$ are wet-bulb temperature, temperature, and relative humidity respectively.

## Questions we want to answer
- How many days of the year have a dangerous/lethal wetbulb temperature? (How has this changed over time?)
- What is the average duration of periods above dangerous/lethal temperatures? Is this duration increasing?

## Usage
### Data Extraction (BigQuery)
```sql 
SELECT
  station_id AS station_id,
  timestamp AS event_time,
  temp_out AS outdoor_temperature,
  humidity AS outdoor_humidity,
FROM
  `manglaria`.`manglaria_lakehouse_ds`.`davis_weather_combined`
```

### Analysis and Plotting
```console
python analysis.py [OPTIONS] [FILENAME]

Options:
  --plot   Plot the data for each station after analysis.
  --write  Write wetbulb data to CSV file after analysis.
  --help   Show this message and exit.
```

Dependencies:
```console
pip install matplotlib pandas click numpy
```
