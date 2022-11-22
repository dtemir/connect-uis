import os
from dotenv import load_dotenv
from twilio.rest import Client


load_dotenv()

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = os.environ["ACCOUNT_SID"]
auth_token = os.environ["AUTH_TOKEN"]
client = Client(account_sid, auth_token)

verify_services = os.environ["VERIFY_SERVICES"]

def send_verification(email):
    """
    Sends a verification code to email provided
    """
    verification = client.verify \
                    .v2 \
                    .services(str(verify_services)) \
                    .verifications \
                    .create(to=str(email), channel='email')

    is_pending = verification.status == 'pending'
    return is_pending
    
    
def check_verification(email, code):
    """
    Confirms if the verification code is correct
    """
    verification_check = client.verify \
                        .v2 \
                        .services(str(verify_services)) \
                        .verification_checks \
                        .create(to=str(email), code=str(code))
    
    is_approved = verification_check.status == 'approved'
    return is_approved