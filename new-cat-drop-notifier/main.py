from logging import getLogger, basicConfig, INFO
from os import getenv
from time import sleep

from interfaces import OHSAdoptPage, SMSMessenger

basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=INFO)
logger = getLogger(__name__)


def main():
    delay = int(getenv("DELAY", 15)) * 60  # Delay is in minutes, and we have to convert to seconds
    cats_last_seen = OHSAdoptPage("cats").all_animals
    sms_messenger = SMSMessenger()

    while True:
        logger.info("Checking for a cat drop...")
        cat_adoption_page = OHSAdoptPage("cats")
        new_cats = list(set(cat_adoption_page.all_animals) - set(cats_last_seen))

        if new_cats:
            logger.info(f"NEW CAT DROP! UOC (Units of Cat): {len(new_cats)}")
            message = "NEW CAT DROP!\n"
            for cat in new_cats:
                if len(message + str(cat)) >= 1600:
                    sms_messenger.send_sms(message)
                    message = ""
                message += str(cat)
            sms_messenger.send_sms(message)
        else:
            logger.info("No cat drop!")

        cats_last_seen = cat_adoption_page.all_animals
        logger.info(f"Sleeping for {delay//60} minutes")
        sleep(delay)


if __name__ == '__main__':
    main()
