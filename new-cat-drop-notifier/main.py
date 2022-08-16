from os import getenv
from time import sleep

from interfaces import OHSAdoptPage, SMSMessenger
from models import AnimalAdoptionCard


def main():
    delay = getenv("DELAY", 15) * 60  # Delay is in minutes and we have to convert to seconds
    cats_last_seen: list[AnimalAdoptionCard] = []
    sms_messenger = SMSMessenger()

    while True:
        cat_adoption_page = OHSAdoptPage("cats")
        new_cats = list(set(cat_adoption_page.all_animals) - set(cats_last_seen))

        if new_cats:
            sms_messenger.send_sms(f"New cats! \n\n{new_cats}")

        cats_last_seen = cat_adoption_page.all_animals
        sleep(delay)


if __name__ == '__main__':
    main()
