from os import getenv
from time import sleep

from interfaces import OHSAdoptPage, SMSMessenger


def main():
    delay = int(getenv("DELAY", 15)) * 60  # Delay is in minutes, and we have to convert to seconds
    cats_last_seen = OHSAdoptPage("cats").all_animals
    sms_messenger = SMSMessenger()

    while True:
        cat_adoption_page = OHSAdoptPage("cats")
        new_cats = list(set(cat_adoption_page.all_animals) - set(cats_last_seen))

        if new_cats:
            message = "New Cats!\n"
            for cat in new_cats:
                if len(message + str(cat)) >= 1600:
                    sms_messenger.send_sms(message)
                    message = ""
                message += str(cat)
            sms_messenger.send_sms(message)

        cats_last_seen = cat_adoption_page.all_animals
        sleep(delay)


if __name__ == '__main__':
    main()
