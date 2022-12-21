import os
import json
import datetime
import logging

from modules import actions
from modules import conditions

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker


engine = create_engine("sqlite:///test.db")
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(bind=engine)


class ActiveDelegate(Base):
    __tablename__ = "active"

    classname = Column(String)
    created = Column(Integer)
    delete_after = Column(Integer)
    args = Column(String, primary_key=True)


Base.metadata.create_all(bind=engine)


class Delegation:

    def __init__(self):
        # Configure logging
        log_level = os.environ.get('LOG_LEVEL', 'INFO')
        logging.basicConfig(
            format='%(asctime)s %(levelname)s %(message)s',
            datefmt='%d/%m/%Y %I:%M:%S',
            level=log_level)
        self.logger = logging.getLogger(__name__)

        self.actions_delegates = [
            actions.ActionBlockIpProxy,
            actions.ActionSendMail
        ]

    def evaluate_required_actions(self, events):
        actions_required = []
        t_delta = datetime.timedelta(
            minutes=int(os.environ.get("RATE_MINUTES")))

        ip_conditions_limit = conditions.ConditionFieldSpecificLimit(
            5, t_delta)
        device_id_conditions_limit = conditions.ConditionFieldSpecificLimit(
            3, t_delta)

        actions_required += ip_conditions_limit.check(
            events, field="ipAddress")
        actions_required += device_id_conditions_limit.check(
            events, field="code_id")

        self.logger.debug("ACTIONS REQUIRED")
        self.logger.debug(actions_required)

        return actions_required

    def get_delegations(self, required_actions):
        delegations = []
        for event, count, condition in required_actions:
            for ad in self.actions_delegates:
                delegations += [ad(event, count, condition)]
        return delegations

    def trigger_actions(self, delegations):
        for d in delegations:
            now = datetime.datetime.now()
            delete_after = now + datetime.timedelta(minutes=1)
            d.state.pop("time", None)

            save_state = ActiveDelegate(
                classname=d.__class__.__name__,
                created=now.timestamp(),
                delete_after=delete_after.timestamp(),
                args=json.dumps(d.state)
            )

            query = session.query(ActiveDelegate)
            filter_query = query.filter(ActiveDelegate.args == save_state.args)
            exists = filter_query.first()
            # Another suspect to bug... The line below is always True
            if not exists or True:
                d.trigger()
                session.merge(save_state)
                session.commit()

    def cleanup_expired_actions(self):
        cleanup_list = session.query(ActiveDelegate).filter(
            ActiveDelegate.delete_after < datetime.datetime.now().timestamp()).all()

        self.logger.debug("Cleaning up expired actions")
        for s in cleanup_list:
            d = getattr(actions, s.classname)(
                json.loads(s.args), args, 0, "ipAddress")
            d.cleanup()
            da = getattr(actions, s.classname)(
                json.loads(s.args), args, 0, "code_id")
            da.cleanup()
