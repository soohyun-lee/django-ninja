from firebase_admin import (
    credentials,
    initialize_app,
    messaging
)
from viva_notice.settings import FIREBASE_CREDENTIAL_KEY
from .models import User

cred = credentials.Certificate(FIREBASE_CREDENTIAL_KEY)
fcm = initialize_app(cred)

def multi_send_fcm_message(notice):
    user_tokens = list(User.objects.exclude(fcm_token=None).values_list('fcm_token', flat=True))

    message = messaging.MulticastMessage(
        data = {
            'id' : notice.id,
            'content' : notice.content
        },
        tokens = user_tokens
    )
    response = messaging.send_multicast(message)

    return response