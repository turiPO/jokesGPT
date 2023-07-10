import os
import requests
import json

class ChuckNorris:
    HEADERS = {
        "accept": "application/json",
        "X-RapidAPI-Key": os.getenv("RapidAPI_Key"),
        "X-RapidAPI-Host": "matchilling-chuck-norris-jokes-v1.p.rapidapi.com"
    }

    URL = "https://matchilling-chuck-norris-jokes-v1.p.rapidapi.com"

    def search_chunknorris_jokes(self, query: str, amount: int = 3) -> str:
        suffix = "/jokes/search?query=" + query
        results = self._req(suffix)['result']
        return [result['value'] for result in results][:min(amount, 5)]

    @property
    def available_functions(self):
        return {
            "search_chunknorris_jokes": self.search_chunknorris_jokes,
            "get_chunknorris_random_joke": self.get_chunknorris_random_joke,
        }
    
    def executioner(self, function_call):
        function_name = function_call["name"]
        fuction_to_call = self.available_functions[function_name]
        function_args = json.loads(function_call["arguments"])
        function_response = fuction_to_call(
            **function_args
        )
        return function_response

    @property
    def class_functions(self):
        return [self.get_chunknorris_random_joke_id, self.search_chunknorris_jokes_id]
        
    @property
    def search_chunknorris_jokes_id(self) -> dict:
        return {
            "name": "search_chunknorris_jokes",
            "description": "Used to search for jokes about Chuck Norris",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The query to search for in the jokes db"
                    },
                    "amount": {
                        "type": "integer",
                        "description": "The amount of jokes to return"
                    },
                },
                "required": ["query"],
            }
        }
    
    @property
    def get_chunknorris_random_joke_id(self) -> dict:
        return {
            "name": "get_chunknorris_random_joke",
            "description": "Used to get a random joke about Chuck Norris",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }

    def get_chunknorris_random_joke(self) -> str:
        suffix = "/jokes/random"
        return self._req(suffix)["value"]

    def _req(self, suffix):
        url = self.URL + suffix

        response = requests.get(url, headers=self.HEADERS)
        return response.json()
