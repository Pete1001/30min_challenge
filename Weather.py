import requests
import os
from dotenv import load_dotenv
import gradio as gr

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("API_KEY")

def get_weather(city_name):
    if not api_key:
        return "Error: API key is missing. Set it in your environment variables."
    
    base_url = "https://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}q={city_name}&appid={api_key}&units=imperial"

    try:
        response = requests.get(complete_url)
        response.raise_for_status()  # Raise exception for HTTP errors
        data = response.json()
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"

    if data.get("cod") != "404":
        main = data.get("main", {})
        weather = data.get("weather", [{}])[0]
        temperature = main.get("temp", "N/A")
        pressure = main.get("pressure", "N/A")
        humidity = main.get("humidity", "N/A")
        description = weather.get("description", "N/A")

        return (
            f"City: {city_name}\n"
            f"Temperature: {temperature}°F\n"
            f"Pressure: {pressure} hPa\n"
            f"Humidity: {humidity}%\n"
            f"Description: {description}"
        )
    else:
        return "City Not Found"

# Define Gradio interface
def weather_interface(city_name):
    return get_weather(city_name)

# Create the Gradio app
gradio_app = gr.Interface(
    fn=weather_interface,
    inputs="text",  # Input field for the city name
    outputs="text",  # Output the weather details as text
    title="Weather App",
    description="Enter the name of a city to get its current weather conditions.  eg.:  Denver or Denver, Colorado"
)

# Launch the app
if __name__ == "__main__":
    gradio_app.launch(share=True)
