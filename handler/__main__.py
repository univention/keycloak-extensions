#!/usr/bin/env python3

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

import argparse
from keycloak import KeycloakAdmin
import datetime
import time
import json

import conditions
import actions
import utils
import types

engine = create_engine("sqlite:///test.db")
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class ActiveDelegate(Base):
    __tablename__ = "active"

    classname = Column(String)
    created = Column(Integer)
    delete_after = Column(Integer)
    args = Column(String, primary_key=True)


def query_all_events(kc_admin):
    events_all = []
    events_uuids = {}
    counter = 1

    found_new = True
    run_delegates = False

    while found_new:

        found_new = False
        events = kc_admin.get_events(filter_date.update({"first": counter * 10}))
        counter += 1
        time.sleep(1)
        for e in events:
            event_uuid = e["time"]
            if not event_uuid:
                continue
            if event_uuid not in events_uuids:
                events_uuids.update({event_uuid: True})
                events_all.append(e)
                found_new = True
                run_delegates = True

    print("Got {} unique events in {} queries".format(len(events_all), counter))
    events_time_parsed = list(map(utils.parse_event_date, events_all))
    return (events_time_parsed, run_delegates)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Keycloak Events Handler')

    parser.add_argument("--realm", default="master")

    parser.add_argument("--kc-admin-user", default="kcadmin")
    parser.add_argument("--kc-admin-pass", default="kcadminpassword")
    parser.add_argument("--kc-admin-auth-url", required=True)
    parser.add_argument("--mail-user", default="keycloak")
    parser.add_argument("--mail-pass", required=True)
    parser.add_argument("--mail-server", required=True)
    parser.add_argument("--admin-mail", required=True)

    parser.add_argument("--kc-proxy", required=True)
    parser.add_argument("--udm-rest-base-url", required=True)
    parser.add_argument("--udm-rest-user", required=True)
    parser.add_argument("--udm-rest-password", required=True)

    args = types.SimpleNamespace(
        udm_rest_password = os.env.get("REALM") or "master",
        udm_rest_password = os.env.get("KC_ADMIN_USER") or "kcadmin",
        udm_rest_password = os.env.get("KC_ADMIN_PASS") or "kcadminpassword",
        udm_rest_password = os.env["KC_ADMIN_AUTH_URL"],
        udm_rest_password = os.env.get("MAIL_USER") or "keycloak",
        udm_rest_password = os.env["MAIL_PASS"],
        udm_rest_password = os.env["MAIL_SERVER"],
        udm_rest_password = os.env.get("ADMIN_MAIL_LIST") or [],
        udm_rest_password = os.env.get("DEBUG_KC_PROXY_OVERWRITE") or "proxy",
        udm_rest_password = os.env.get("UDM_REST_BASE_URL"),
        udm_rest_password = os.env.get("UDM_REST_USER"),
        udm_rest_password = os.env.get("UDM_REST_PASSWORD"),
    )

    Base.metadata.create_all(bind=engine)

    #logging.basicConfig(level=logging.DEBUG)

    while True:
        kc_admin = KeycloakAdmin(server_url=args.kc_admin_auth_url,
                                 username=args.kc_admin_user,
                                 password=args.kc_admin_pass,
                                 realm_name=args.realm,
                                 verify=True)

        start_date = datetime.datetime.now().strftime("%y-%d-%m")
        end_date = datetime.datetime.now().strftime("%y-%d-%m")
        filter_date = {"date_from": start_date, "date_to": end_date, "max": 11}

        events, run_delegates = query_all_events(kc_admin)

        print("Run Delegates?: ", run_delegates)

        if run_delegates:

            # check conditions #
            actions_required = []
            tdelta = datetime.timedelta(minutes=10)
            condition_field_limit5 = conditions.ConditionFieldSpecificLimit(events, 5, tdelta)

            actions_required += condition_field_limit5.check(field="ip_address")

            condition_field_limit3 = conditions.ConditionFieldSpecificLimit(events, 3, tdelta)
            actions_required += condition_field_limit3.check(field="code_id")

            print("====== ACTIONS REQUIRED ======")
            print(actions_required)

            # run actions #
            actions_delegates = [
                actions.ActionBlockIpProxy,
                actions.ActionSendMail
            ]

            delegations = []
            for event, count, condition in actions_required:
                for ad in actions_delegates:
                    delegations += [ad(event, args, count, condition)]

            for d in delegations:

                now = datetime.datetime.now()
                delete_after = now + datetime.timedelta(minutes=1)
                d.state.pop("time", None)

                save_state = ActiveDelegate(classname=d.__class__.__name__,
                                           created=now.timestamp(),
                                           delete_after=delete_after.timestamp(),
                                           args=json.dumps(d.state))

                query = session.query(ActiveDelegate)
                filter_query = query.filter(ActiveDelegate.args == save_state.args)
                exists = filter_query.first()
                if not exists or True:
                    d.trigger()
                    session.merge(save_state)
                    session.commit()

        # cleanup #
        # sqlachemly get save states relevant
        cleanup_list = session.query(ActiveDelegate).filter(
            ActiveDelegate.delete_after < datetime.datetime.now().timestamp()).all()

        print("Cleaning up..")
        for s in cleanup_list:
            d = getattr(actions, s.classname)(json.loads(s.args), args, 0, "ip_address")
            d.cleanup()
            da = getattr(actions, s.classname)(json.loads(s.args), args, 0, "code_id")
            da.cleanup()
