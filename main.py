from dotenv import load_dotenv
import os 
from twitchAPI.pubsub import PubSub
from twitchAPI.twitch import Twitch, AuthScope
from twitchAPI.oauth import UserAuthenticator

load_dotenv()
from pprint import pprint
from uuid import UUID
import time


def callback_channel_points(uuid: UUID, data: dict) -> None:
    qwerty_id = '5351fef3-198b-42e0-a10b-0f5ad879e345'

    print('got callback for UUID ' + str(uuid))
    reward_receive = data['data']['redemption']['reward']['id']

    if qwerty_id == reward_receive :
        os.system("~/prog/stream/xkbswitch-macosx/xkbswitch-arm -s com.apple.keylayout.ABC")  
        time.sleep(30)
        os.system("~/prog/stream/xkbswitch-macosx/xkbswitch-arm -s com.apple.keylayout.Colemak")  
 

CLIENT_ID = os.environ.get("CLIENT_ID")
SECRET = os.environ.get("SECRET")
target_scope = [AuthScope.CHANNEL_READ_REDEMPTIONS]
twitch = Twitch(CLIENT_ID, SECRET,target_app_auth_scope=target_scope)
auth = UserAuthenticator(twitch, target_scope, force_verify=True)


# this will open your default browser and prompt you with the twitch verification website
token, refresh_token = auth.authenticate()
# add User authentication
twitch.set_user_authentication(token, target_scope, refresh_token)


pubsub = PubSub(twitch)
pubsub.start()


uuid = pubsub.listen_channel_points('541628609', callback_channel_points)


