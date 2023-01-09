import time

from modules import keycloak_poller
from modules import action_maker
import database

# Import needed for table creation
from models import action


if __name__ == "__main__":

    database.Base.metadata.create_all(database.engine)

    keycloak = keycloak_poller.KeycloakPoller()
    action_maker = action_maker.ActionMaker()

    while True:
        events = keycloak.update_events()
        action_maker.remove_expired_actions()
        action_maker.take_actions(events)
        time.sleep(1)
