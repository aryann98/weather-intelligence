import requests as rt
from colorama import Fore, Style

geo_url = 'https://geocoding-api.open-meteo.com/v1/search'
weather_url = "https://api.open-meteo.com/v1/forecast"


# ─────────────────────────────────────────────
# CITY INPUT
# ─────────────────────────────────────────────

print()
print(Fore.CYAN + Style.BRIGHT)
print("╔══════════════════════════════════════════════╗")
print("║              WEATHER INTELLIGENCE            ║")
print("╚══════════════════════════════════════════════╝")
print(Style.RESET_ALL)

user_input = input(
    Fore.YELLOW + "Enter City Name: " + Style.RESET_ALL
)


# ─────────────────────────────────────────────
# GEOCODING
# ─────────────────────────────────────────────

geo_param = {
    'name': user_input
}

response = rt.get(
    geo_url,
    params=geo_param,
    timeout=5
)

geo_data = response.json()
geo_results = geo_data['results']

city_name = geo_results[0]['name']
city_longitude = geo_results[0]['longitude']
city_latitude = geo_results[0]['latitude']


# ─────────────────────────────────────────────
# WEATHER API
# ─────────────────────────────────────────────

weather_param = {
    "longitude": city_longitude,
    "latitude": city_latitude,
    "hourly": "temperature_2m,precipitation_probability"
}

weather_response = rt.get(
    weather_url,
    params=weather_param,
    timeout=5
)

weather_data = weather_response.json()

hourly_data = weather_data['hourly']

hourly_data_of_time = hourly_data['time']
hourly_data_of_temperature = hourly_data['temperature_2m']
hourly_data_of_probability = hourly_data['precipitation_probability']


# ─────────────────────────────────────────────
# CITY INFORMATION
# ─────────────────────────────────────────────

print()

print(Fore.CYAN + Style.BRIGHT)
print("┌──────────────────────────────────────────────┐")
print("│              CURRENT LOCATION                │")
print("└──────────────────────────────────────────────┘")
print(Style.RESET_ALL)

print(
    Fore.WHITE + Style.BRIGHT +
    "  City        : " +
    Fore.GREEN + city_name +
    Style.RESET_ALL
)

print(
    "  Longitude   : ",
    city_longitude
)

print(
    "  Latitude    : ",
    city_latitude
)


# ─────────────────────────────────────────────
# NEXT 6 HOURS
# ─────────────────────────────────────────────

print()

print(Fore.YELLOW + Style.BRIGHT)
print("  NEXT 6 HOURS")
print("  ─────────────────────────────────────────────")
print(Style.RESET_ALL)


for time, temp, prob in zip(
    hourly_data_of_time[:6],
    hourly_data_of_temperature[:6],
    hourly_data_of_probability[:6]
):

    hour = time.split("T")[1][:5]

    if prob < 30:
        rain_icon = "☀"
        rain_status = "Low"

    elif prob < 60:
        rain_icon = "🌦"
        rain_status = "Moderate"

    else:
        rain_icon = "☔"
        rain_status = "High"

    print(
        f"  {hour}   "
        f"{rain_icon}   "
        f"{temp:>5.1f}°C   "
        f"Rain: {prob:>3}%   "
        f"({rain_status})"
    )


# ─────────────────────────────────────────────
# WEATHER ADVISORY
# ─────────────────────────────────────────────

print()

print(Fore.MAGENTA + Style.BRIGHT)
print("  ⚠ WEATHER ADVISORY")
print("  ─────────────────────────────────────────────")
print(Style.RESET_ALL)


max_probability = max(
    hourly_data_of_probability[:6]
)

average_temperature = (
    sum(hourly_data_of_temperature[:6]) / 6
)


if max_probability >= 60:

    print(
        Fore.RED +
        "  ☔ High chance of rain in the next few hours"
        + Style.RESET_ALL
    )

elif max_probability >= 30:

    print(
        Fore.YELLOW +
        "  🌦 Some chance of rain — carry an umbrella"
        + Style.RESET_ALL
    )

else:

    print(
        Fore.GREEN +
        "  ☀ Low rain probability"
        + Style.RESET_ALL
    )


if average_temperature >= 35:

    print(
        Fore.RED +
        "  🥵 Temperature may feel uncomfortable"
        + Style.RESET_ALL
    )

elif average_temperature >= 30:

    print(
        Fore.YELLOW +
        "  🌡 Warm conditions expected"
        + Style.RESET_ALL
    )

else:

    print(
        Fore.GREEN +
        "  😌 Temperature looks comfortable"
        + Style.RESET_ALL
    )


# ─────────────────────────────────────────────
# OUTDOOR STATUS
# ─────────────────────────────────────────────

print()

print(Fore.CYAN + Style.BRIGHT)
print("  ┌──────────────────────────────────────────┐")
print("  │             OUTDOOR STATUS               │")
print("  └──────────────────────────────────────────┘")
print(Style.RESET_ALL)


if max_probability >= 60:

    print(
        Fore.RED +
        "  🌧 Outdoor activity: NOT RECOMMENDED"
        + Style.RESET_ALL
    )

elif average_temperature >= 35:

    print(
        Fore.YELLOW +
        "  🥵 Outdoor activity: AVOID PEAK HOURS"
        + Style.RESET_ALL
    )

else:

    print(
        Fore.GREEN +
        "  🚶 Outdoor activity: GOOD"
        + Style.RESET_ALL
    )


print()

print(
    Fore.CYAN +
    "  Weather Intelligence • Powered by Open-Meteo"
    + Style.RESET_ALL
)

print()