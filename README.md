# New Cat Drop Notifier
Notifier that can send a text message when the Oregon Humane Society drops a new batch of cats available for adoption. Here, currently in Oregon, it is difficult to find a younger cat for adoption. I am intent on finding a cat the same age as my current cat. This is so I don't have to just refresh the site constantly; this is the example of "spending 5 hours automating a manual process that took less than 5 seconds".

This was designed to be run on a schedule from a Google Cloud Run job. It uses a bucket in Google Cloud Storage to persist a list of cats between runs to identify if there are new cats.

### Environment Variables (All must be defined)

- ``TWILIO_ACCOUNT_SID``: Twilio Account SID for SMS
- ``TWILIO_AUTH_TOKEN``: Twilio auth token to use for SMS
- ``TWILIO_PHONE_NUMBER``: Twilio phone number to send SMS messages from
- ``SEND_TO_PHONE_NUMBERS``: Comma-separated list of phone numbers like: `+1123456789,+1212313414`
- ``OOOGLE_ACCOUNT_INFO``: String JSON object of Google account info. Download from Google Cloud
- ``GOOGLE_CLOUD_BUCKET``: Bucket to store JSON last cats seen

THIS PROJECT IS COMPLETE:

behold! my new cat Sita:

<img width="207" alt="image" src="https://user-images.githubusercontent.com/56234568/210699375-b7c9738d-ff8c-4f78-9c1b-a2143d994328.png">
