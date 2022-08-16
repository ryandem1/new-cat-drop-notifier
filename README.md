# New Cat Drop Notifier
Notifier that can send a text message when the Oregon Humane Society drops a new batch of cats available for adoption.

### Environment Variables

- ``DELAY``: Time (in minutes) to wait before checking cat availability again
- ``TWILIO_ACCOUNT_SID``: Twilio Account SID for SMS
- ``TWILIO_AUTH_TOKEN``: Twilio auth token to use for SMS
- ``TWILIO_PHONE_NUMBER``: Twilio phone number to send SMS messages from
- ``SEND_TO_PHONE_NUMBERS``: Comma-separated list of phone numbers like: `+1123456789,+1212313414`
