from logging import getLogger, basicConfig, INFO

from interfaces import OHSAdoptPage, SMSMessenger, GoogleCloudStorage

basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=INFO)
logger = getLogger(__name__)


def main():
    cat_bucket = GoogleCloudStorage()
    last_cat_names: list[str] = cat_bucket.get_cats_last_seen() or [cat.name for cat in OHSAdoptPage("cats").all_animals]
    sms_messenger = SMSMessenger()

    logger.info("Checking for a cat drop...")
    cat_adoption_page = OHSAdoptPage("cats")
    current_cat_names = [cat.name for cat in cat_adoption_page.all_animals]
    new_cat_names = list(set(current_cat_names) - set(last_cat_names))

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

    cat_bucket.upload_cats_last_seen(current_cat_names)


if __name__ == '__main__':
    main()
