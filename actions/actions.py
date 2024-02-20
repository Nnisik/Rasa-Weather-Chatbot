# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, SessionStarted, ActionExecuted, EventType
import requests


class ActionWeather(Action):
    def name(self):
        return "Action Weather"
    
    def run(self, dispatcher, tracker, domain):
        city = tracker.get_slot("location")

        APIKEY = "ab23266f6d76498191b143316231912"
        APIURL = f"http://api.weatherapi.com/v1/forecast.json?key=${APIKEY}&q={city.capitalize()}&days=5&aqi=no&alerts=no"

        response = requests.get(APIURL)

        if not response:
            message = "Sorry, something went wrong. Please try again later."
            dispatcher.utter_message(message)
            return []

        data = response.json()

        locationData = data['location']
        weatherData = data['current']

        place = f"{locationData['name']}, {locationData['country']}"
        temp = round(weatherData['temp_c'])
        weather = weatherData['condition']['text']

        response = f"It's currently {weather}, {temp}'C in {place}."
        dispatcher.utter_message[response]

        return [SlotSet('location', city)]
