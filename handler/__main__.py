import time

from modules import keycloak_poller
from modules import action_maker
from modules import notifier
import database

# Import needed for table creation
from models import action
from models import device


if __name__ == "__main__":

    database.Base.metadata.create_all(database.engine)

    keycloak = keycloak_poller.KeycloakPoller()
    action_maker = action_maker.ActionMaker()
    notif = notifier.Notifier(keycloak)

    while True:
        events = keycloak.update_events()
        failed_login_events = [e for e in events if e["type"] == "LOGIN_ERROR"]
        action_maker.remove_expired_actions()
        action_maker.take_actions(failed_login_events)
        notif.notify_new_logins()
        time.sleep(1)
