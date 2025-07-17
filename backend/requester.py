import os
import requests

class Requester:
    """
        This class is encapsulation of GET and POST requests logic.\n
        auth_token = API token from prom.ua or it´s partner.\n
        host = instance name of where the shop is located.
    """
    def __init__(self):
        self.auth_token = os.getenv("AUTH_TOKEN") # Token from .env
        self.host = os.getenv("HOST") # Host like my.prom.ua
        self.headers = {'Authorization': f'Bearer {self.auth_token}', 'Content-Type': 'application/json'}

        if not(self.auth_token) or not (self.host):
            raise ValueError("Authorization Token or Host are false! Please check .env file!")
        
    def get_request(self):
        """
        Sends a GET request to the `/products/list` endpoint to retrieve a list of products.

        Fetches product data including multilingual fields, pricing, inventory, and other attributes.
        Returns the response JSON if the request is successful.

        Raises
        ------
        ConnectionError
            If the server does not respond with status code 200 or the request fails.

        Returns
        -------
        dict or None
            The response JSON containing product information, or None if the request failed.

        """
        url = f"https://{self.host}/api/v1/products/list"
        try:
            response = requests.get(url=url, headers=self.headers)
            if response.status_code != 200:
                raise ConnectionError(f"GET request was not successful. Connection to {self.host} failed.")
            return response.json()
        except Exception as e:
            print(f"Following error was caught while connecting to server to make a GET request: {e}")
            return None
    
    def post_request(self, json_body: list):
        """
        Sends a POST request to the `/products/edit` endpoint to update product data.

        Sends a list of product dictionaries containing multilingual fields, pricing,
        inventory, and other attributes. Returns the HTTP status code if the request
        is successful or handled with an expected rejection. Returns None in case of
        unexpected connection or runtime errors.

        Parameters
        ----------
        json_body : list
            A list of product dictionaries to be sent in the request body.

        Raises
        ------
        ConnectionError
            If the server responds with a non-200 status code.

        Returns
        -------
        int or None
            The HTTP status code from the response if the request completes.
            Returns None if an unexpected error occurs before a response is received.
        """
        url = f"https://{self.host}/api/v1/products/edit"
        try:
            response = requests.post(url=url, headers=self.headers, json=json_body)
            if response.status_code != 200:
                raise ConnectionError(f"POST request was not successful. Connection to {self.host} failed.")
            return response.status_code
        except Exception as e: 
            print(f"Following error was caught while connecting to server to make a POST request: {e}")
            return None
        
    def translate_product(self, json_body: dict):
        """
        Sends a PUT request to the `/products/translation` endpoint to update multilingual product data.

        Sends a dictionary containing product translation fields (e.g. names, descriptions)
        in different languages. Returns the HTTP status code if the request is successful.
        Returns None in case of an unexpected error.

        Parameters
        ----------
        json_body : dict
            A dictionary containing multilingual product fields to be updated.

        Raises
        ------
        ConnectionError
            If the server responds with a non-200 status code.

        Returns
        -------
        int or None
            The HTTP status code from the response if the request completes.
            Returns None if an unexpected error occurs before a response is received.
        """
        url = f"https://{self.host}/api/v1/products/translation"
        try:
            response = requests.put(url=url, headers=self.headers, json=json_body)
            if response.status_code != 200:
                raise ConnectionError(f"PUT request was not successful. Connection to {self.host} failed.")
            return response.status_code
        except Exception as e: 
            print(f"Following error was caught while connecting to server to make a PUT request: {e}")
            return None