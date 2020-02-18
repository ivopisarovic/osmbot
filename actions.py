# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import Restarted
from rasa_sdk.executor import CollectingDispatcher
from SPARQLWrapper import SPARQLWrapper, JSON


class ActionFindMostPopulousCity(Action):

    def name(self) -> Text:
        return "action_find_most_populous_city"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # get country entity from the user's question via a slot
        country = tracker.get_slot('country')

        # search for a city in the given country
        sparql = SPARQLWrapper("https://query.wikidata.org/sparql", agent='Rasabot agent')
        sparql.setQuery("""
            PREFIX wikibase: <http://wikiba.se/ontology#>
            PREFIX wd: <http://www.wikidata.org/entity/>
            PREFIX wdt: <http://www.wikidata.org/prop/direct/>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX bd: <http://www.bigdata.com/rdf#>

            SELECT ?itemLabel
            WHERE
            {
              # city:
              ?item wdt:P31 wd:Q1549591 .  # item is instance of city
            
              # population:
              ?item wdt:P1082 ?population . # city has some population, extract it to 'population'
            
              # country:
              ?item wdt:P17 ?country. # get the country to which the city belongs to
              ?country rdfs:label ?label . # extract the country label
              FILTER(LANG(?label) = "en"). # only english labels
              FILTER(REGEX(?label, "^%s$", "i")). # country name is equal to the given country
            
              SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
            }
            ORDER BY desc(?population) # biggest cities first
            LIMIT 1
        """ % country)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        bindings = results['results']['bindings']

        # send back an answer to the user
        if len(bindings) == 0:
            dispatcher.utter_message(text="Country " + country + " not found!")
        else:
            biggest_city = bindings[0]['itemLabel']['value']  # get country name from the first result
            dispatcher.utter_message(text="It is " + biggest_city + "!")

        # finish the dialogue and start over (it empties slots)
        return [Restarted()]
