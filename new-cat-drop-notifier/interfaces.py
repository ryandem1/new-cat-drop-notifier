from functools import cached_property
from os import environ

from bs4 import BeautifulSoup, ResultSet
from requests import RequestException, Session
from twilio.rest import Client

from consts import ADOPT_ENDPOINT, RESULT_ITEM_CLASS, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER, \
    SEND_TO_PHONE_NUMBERS
from models import AnimalType, AnimalAdoptionCard


class OHSAdoptPage:
    """Serves as an HTTP client to get the OHS data, as well as a parser for that data"""

    def __init__(self, animal_type: AnimalType):
        """Starts a new interface to the OHS adopt page and a parser to get data for that page.

        :param animal_type: Define which animal type you would like to get the adopt page for
        """
        self.animal_type = animal_type
        self._client = Session()
        self._parser = BeautifulSoup(self._raw_adopt_page, "html.parser")

    @cached_property
    def _raw_adopt_page(self) -> str:
        """
        Sends a GET to the adopt endpoint to get the HTML search results for an animal_type.

        :return: Raw HTML doc in a string
        """
        response = self._client.get(url=ADOPT_ENDPOINT, params={"type": self.animal_type})
        if not response.ok:
            raise RequestException(f"Could not get adopt page for animal type: {self.animal_type}")

        return response.text

    @cached_property
    def _raw_adoption_items(self) -> ResultSet:
        """Extracts the raw HTML results from the adopt page and returns as a string

        :return raw_results: String raw HTML adoption item results
        """
        raw_results = self._parser.find_all("div", {"class": RESULT_ITEM_CLASS})
        return raw_results

    @cached_property
    def all_animals(self) -> list[AnimalAdoptionCard]:
        """Extracts all animal adoption items from the raw_adoption_items

        :return names: List of string animal names on current adoption page
        """
        return [AnimalAdoptionCard.from_raw_result_item(result_item) for result_item in self._raw_adoption_items]


class SMSMessenger:

    def __init__(self):
        account_sid = environ[TWILIO_ACCOUNT_SID]
        auth_token = environ[TWILIO_AUTH_TOKEN]
        self.twilio = Client(account_sid, auth_token)
        self.twilio_phone_number = environ[TWILIO_PHONE_NUMBER]
        self.send_to_phone_numbers = environ[SEND_TO_PHONE_NUMBERS]

    def send_sms(self, message: str):
        """Sends an SMS message"""
        for phone_number in self.send_to_phone_numbers:
            self.twilio.messages.create(from_=self.twilio_phone_number, body=message, to=phone_number)
