import json
from functools import cached_property
from os import environ

from bs4 import BeautifulSoup, ResultSet
from google.cloud import storage
from google.oauth2.service_account import Credentials
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

    @cached_property
    def all_names(self) -> list[str]:
        """Extracts all animal names are returns them as a list of strings, a convenience method

        :return: List of string animal names on the page
        """
        return [animal.name for animal in self.all_animals]


class SMSMessenger:

    def __init__(self):
        account_sid = environ[TWILIO_ACCOUNT_SID]
        auth_token = environ[TWILIO_AUTH_TOKEN]
        self.twilio = Client(account_sid, auth_token)
        self.twilio_phone_number = environ[TWILIO_PHONE_NUMBER]
        self.send_to_phone_numbers = environ[SEND_TO_PHONE_NUMBERS].split(",")

    def send_sms(self, message: str):
        """Sends an SMS message"""
        for phone_number in self.send_to_phone_numbers:
            self.twilio.messages.create(from_=self.twilio_phone_number, body=message, to=phone_number)


class GoogleCloudStorage:

    blob_name = "cats_last_seen.json"

    def __init__(self):
        self.__credentials = Credentials.from_service_account_info(json.loads(environ["GOOGLE_ACCOUNT_INFO"]))
        self.__client = storage.Client(credentials=self.__credentials)
        self.__bucket = self.__client.get_bucket(environ["GOOGLE_CLOUD_BUCKET"])

    def upload_cats_last_seen(self, cat_names_last_seen: list[str]):
        """
        Uploads the list of cat names last seen as a JSON blob in GCS.

        :param cat_names_last_seen: List of string cat names to store
        :return: None
        """
        json_data = json.dumps(cat_names_last_seen)

        blob = self.__bucket.blob(self.blob_name)
        blob.upload_from_string(json_data)

    def get_cats_last_seen(self) -> list[str]:
        """
        Returns the list of cat names from the GCS object

        :return cat_names: list of string cat names
        """
        cats_last_seen_blob = self.__bucket.get_blob(self.blob_name)
        if not cats_last_seen_blob:
            return []

        cats_last_seen = json.loads(cats_last_seen_blob.download_as_string())
        return cats_last_seen
