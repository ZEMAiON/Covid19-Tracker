# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from pip._vendor import requests

#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

class ActionCoronaTracker(Action):

    def name(self) -> Text:
        return "action_corona_tracker"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        entities = tracker.latest_message['entities']
        # print("Entity Info", entities)
        response = requests.get("https://api.covid19india.org/data.json").json()  
        message = ""
        state,condition = None,False
        for i in entities:
            if i['entity'] == "state_n_union_territories":
                state=i['value']
        # print(response["cases_time_series"][-1])
        for data in response["statewise"]:
            if data["state"] == state.title() or data["statecode"] == state.upper():
                # print(data)
                condition = True
                message = " All information related to " +data["state"] + "\n" + " \nCurrent Active Cases: " +data["active"] + " \nConfirmed Active Cases: " +data["confirmed"] + " \nConfirmed Death Count: " + data["deaths"] + " \nConfirmed Recovered Count: " + data["recovered"] + " \nUpdated Lastly On: " +data["lastupdatedtime"] + "\n\n"
        if condition is False:
            condition = True
            dispatcher.utter_message(text = " Overall Covid19 situation in India\n " + " \nTotal Confirmed Cases: " +response["cases_time_series"][-1]["totalconfirmed"] + 
            "\nTotal Recovered Cases: " +response["cases_time_series"][-1]["totalrecovered"] + " \nTotal Confirmed Death Count: " +response["cases_time_series"][-1]["totaldeceased"]
            + "\n" + " \nDaily Count\n " + " \nDaily Confirmed Cases: " +response["cases_time_series"][-1]["dailyconfirmed"] + " \nTotal Recovered Count: " +response["cases_time_series"][-1]["dailyrecovered"] + " \nDaily Death Count: " +response["cases_time_series"][-1]["dailydeceased"] 
            + "\nUpdated Lastly On: " +response["cases_time_series"][-1]["dateymd"])
        if condition:
            dispatcher.utter_message(text=message+"\n")
            dispatcher.utter_message(template="utter_did_that_help")
        elif condition is False:
            dispatcher.utter_message(template="utter_please_rephrase")
        return []
