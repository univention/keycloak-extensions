import datetime
import os
import logging
import time
import sys

from utils import parse_event_date

from keycloak import KeycloakAdmin


class KeycloakPoller:

    def __init__(self):
        # Configure logging
        log_level = os.environ.get('LOG_LEVEL', 'INFO')
        logging.basicConfig(
            format='%(asctime)s %(levelname)s %(message)s',
            datefmt='%d/%m/%Y %I:%M:%S',
            level=log_level)
        self.logger = logging.getLogger(__name__)
        self.kc_admin = None

        # Connect to Keycloak admin interface
        try:
            self.kc_admin = KeycloakAdmin(
                server_url=os.environ.get("KC_AUTH_URL", None),
                username=os.environ.get("KC_USER", None),
                password=os.environ.get("KC_PASS", None),
                realm_name=os.environ.get("KC_REALM", None),
                verify=True
            )
        # FIXME: more fine granular exception handling
        except Exception as e:
            self.logger.error("Could not connect to Keycloak: %s", e)
            sys.exit(1)

    def get_all_events(self):
        filterDate = {
            "dateFrom": datetime.datetime.now().strftime("%y-%d-%m"),
            "dateTo": datetime.datetime.now().strftime("%y-%d-%m"),
            "max": 11
        }

        all_events = []
        events_uuids = []
        counter = 1
        found_new = True
        run_delegates = True

        while found_new:
            found_new = False
            events = self.kc_admin.get_events(
                filterDate.update({"first": counter * 10}))
            counter += 1
            for e in events:
                event_uuid = e["time"]
                if not event_uuid:
                    continue
                if event_uuid not in event_uuids:
                    events_uuids.append(event_uuid)
                    all_events.append(e)
                    found_new = True
                    run_delegates = True
            if found_new is False:
                break
            else:
                time.sleep(1)
        self.logger.debug(
            f"Found {len(all_events)} unique events in {counter} queries")
        self.logger.debug(f"Run delegates: {run_delegates}")
        events_time_parsed = [parse_event_date(event) for event in all_events]
        return (events_time_parsed, run_delegates)
