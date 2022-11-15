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

engine = create_engine("sqlite:///test.db")
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class ActiveDelegate(Base):
    __tablename__ = "active"

    classname = Column(String)
    created = Column(Integer)
    deleteAfter = Column(Integer)
    args = Column(String, primary_key=True)


def queryAllEvents(kc_admin):

    eventsAll = []
    eventsUUIDs = dict()
    counter = 1

    found_new = True
    runDelegates = False

    while(found_new):

        found_new = False
        events = kc_admin.get_events(filterDate.update({"first": counter * 10}))
        counter += 1
        time.sleep(1)
        for e in events:
            eventUUID = e["time"]
            if not eventUUID:
                continue
            if eventUUID not in eventsUUIDs:
                eventsUUIDs.update({eventUUID: True})
                eventsAll.append(e)
                found_new = True
                runDelegates = True

    print("Got {} unique events in {} queries".format(len(eventsAll), counter))
    eventsTimeParsed = list(map(utils.parseEventDate, eventsAll))
    return (eventsTimeParsed, runDelegates)


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

    args = parser.parse_args()

    Base.metadata.create_all(bind=engine)

    #logging.basicConfig(level=logging.DEBUG)

    while(True):
        try:
            kc_admin = KeycloakAdmin(server_url=args.kc_admin_auth_url,
                                     username=args.kc_admin_user,
                                     password=args.kc_admin_pass,
                                     realm_name=args.realm,
                                     verify=True)

            startDate = datetime.datetime.now().strftime("%y-%d-%m")
            endDate = datetime.datetime.now().strftime("%y-%d-%m")
            filterDate = {"dateFrom": startDate, "dateTo": endDate, "max": 11}

            events, runDelegates = queryAllEvents(kc_admin)

            print("Run Delegates?: ", runDelegates)

            if runDelegates:

                # check conditions #
                actionsRequired = []
                tdelta = datetime.timedelta(minutes=10)
                conditionFieldLimit5 = conditions.ConditionFieldSpecificLimit(events, 5, tdelta)

                actionsRequired += conditionFieldLimit5.check(field="ipAddress")

                conditionFieldLimit3 = conditions.ConditionFieldSpecificLimit(events, 3, tdelta)
                actionsRequired += conditionFieldLimit3.check(field="code_id")

                print("====== ACTIONS REQUIRED ======")
                print(actionsRequired)

                # run actions #
                actionsDelegates = [
                    actions.ActionBlockIpProxy,
                    actions.ActionSendMail
                ]

                delegations = []
                for event, count, condition in actionsRequired:
                    for ad in actionsDelegates:
                        delegations += [ad(event, args, count, condition)]

                for d in delegations:

                    now = datetime.datetime.now()
                    deleteAfter = now + datetime.timedelta(minutes=1)
                    if "time" in d.state:
                        del d.state["time"]

                    saveState = ActiveDelegate(classname=d.__class__.__name__,
                                               created=now.timestamp(),
                                               deleteAfter=deleteAfter.timestamp(),
                                               args=json.dumps(d.state))

                    query = session.query(ActiveDelegate)
                    filterQuery = query.filter(ActiveDelegate.args == saveState.args)
                    exists = filterQuery.first()
                    if not exists or True:
                        d.trigger()
                        session.merge(saveState)
                        session.commit()

            # cleanup #
            # sqlachemly get save states relevant
            cleanupList = session.query(ActiveDelegate).filter(
                ActiveDelegate.deleteAfter < datetime.datetime.now().timestamp()).all()

            print("Cleaning up..")
            for s in cleanupList:
                d = getattr(actions, s.classname)(json.loads(s.args), args, 0, "ipAddress")
                d.cleanup()
                da = getattr(actions, s.classname)(json.loads(s.args), args, 0, "code_id")
                da.cleanup()
        except Exception as e:
            print(e)
        finally:
            time.sleep(3)
