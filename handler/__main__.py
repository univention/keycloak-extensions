#!/usr/bin/python3
import time

from modules import keycloak_poller
from modules import delegation
from modules import conditions


if __name__ == "__main__":

    while True:
        # Should I keep the connection open instead of reopening on each iteration?
        kc_poller = keycloak_poller.KeycloakPoller()

        events, runDelegates = kc_poller.get_all_events()

        deleg = delegation.Delegation()

        if runDelegates:

            actions_required = deleg.evaluate_required_actions(events)

            delegations = deleg.get_delegations(actions_required)
            deleg.trigger_actions(delegations)

        deleg.cleanup_expired_actions()
        time.sleep(3)
