from logging import getLogger, basicConfig, INFO

from interfaces import OHSAdoptPage, SMSMessenger, GoogleCloudStorage

basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=INFO)
logger = getLogger(__name__)


def main():
    cat_bucket = GoogleCloudStorage()
    cat_adoption_page = OHSAdoptPage("cats")

    last_cat_names = cat_bucket.get_cats_last_seen() or cat_adoption_page.all_names
    sms_messenger = SMSMessenger()

    logger.info("Checking for a cat drop...")
    new_cat_names = list(set(cat_adoption_page.all_names) - set(last_cat_names))
    cat_bucket.upload_cats_last_seen(cat_adoption_page.all_names)

    if new_cat_names:
        logger.info(f"NEW CAT DROP! UOC (Units of Cat): {len(new_cat_names)}")
        message = "NEW CAT DROP!\n"
        for cat in [cat for cat in cat_adoption_page.all_animals if cat.name in new_cat_names]:
            if len(message + str(cat)) >= 1600:
                sms_messenger.send_sms(message)
                message = ""
            message += str(cat)
        sms_messenger.send_sms(message)
    else:
        logger.info("No cat drop!")


if __name__ == '__main__':
    main()
