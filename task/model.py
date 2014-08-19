# XXX Too aggressive import list
from sqlalchemy import *
from sqlalchemy import schema, types
from database import Base, db_session, commit_db
from model_exception import ModelException
import json

WAITING = "waiting"
RUNNING = "running"
DONE = "done"


class Task(Base):
    __tablename__ = 'tasks'

    id = schema.Column(Integer, primary_key=True)
    status = Column(String)
    task_type = Column(String)
    params = Column(String)
    runner = Column(String)

    def __init__(self, status, task_type, params=None, runner=None):
        self.status = status
        self.runner = runner
        self.task_type = task_type
        self.params = params

    # XXX This method should be identical to the one in client.py
    def __repr__(self):
        return "<Task id:'%r', type:'%r',  status:'%r', parameters:'%r'>" % \
               (self.id, self.task_type, self.status, self.params)

    # #
    ## Represent the task as a map.  To be used when moving it
    ## as a json representation.
    ##
    def as_map(self):
        return {"task_id": self.id,
                "status": self.status,
                "task_type": self.task_type,
                "parameters": json.loads(self.params)}

    ##
    ## The start state needs some special case handling
    ##
    def start(self, runner):
        if not runner:
            raise ModelException(
                "Attempt to start processing, but no process runner specified",
                400)

        self.state_transition(WAITING, RUNNING)
        self.runner = runner

    ##
    ## State transition model
    ##
    def state_transition(self, source, destination):
        if self.status != source:
            attempted_transition = "(%s -> %s)" % (source, destination)
            message = "Attempt to perform state transition " + attempted_transition
            message += " while in state '" + self.status + "'"
            raise ModelException(message, 403)
        else:
            self.status = destination
        return self.as_map()

    def done(self):
        return self.state_transition(RUNNING, DONE)

    def run(self, runner):
        return_value = self.state_transition(WAITING, RUNNING)
        self.runner = runner
        return return_value

    def has_status(self, status):
        return self.status == status

    def is_waiting(self):
        return self.has_status(WAITING)

    def is_running(self):
        return self.has_status(RUNNING)

    def is_done(self):
        return self.has_status(DONE)

    def has_task_type(self, tasktype):
        return self.task_type == tasktype


class RDBQueueStorage():
    def __init__(self):
        pass

    @staticmethod
    def clean():
        Task.query.delete()
        commit_db()

    @staticmethod
    def list_all_tasks_of_status(status):
        result = db_session.query(Task).filter(Task.status == status).all()
        mapped_result = map(lambda x: x.as_map(), result)
        return mapped_result

    @staticmethod
    def list_all_tasks():
        result = db_session.query(Task).all()
        mapped_result = map(lambda x: x.as_map(), result)
        return mapped_result

    def list_all_waiting_tasks(self):
        return self.list_all_tasks_of_status(WAITING)

    def list_all_running_tasks(self):
        return self.list_all_tasks_of_status(RUNNING)

    def list_all_done_tasks(self):
        return self.list_all_tasks_of_status(DONE)

    @staticmethod
    def list_all_tasks_of_type_with_status(task_type, status):
        result = db_session.query(Task).filter(
            Task.status == status,
            Task.task_type == task_type).all()
        mapped_result = map(lambda x: x.as_map(), result)
        return mapped_result

    def list_all_waiting_tasks_of_type(self, task_type):
        return self.list_all_tasks_of_type_with_status(task_type, WAITING)

    def list_all_running_tasks_of_type(self, task_type):
        return self.list_all_tasks_of_type_with_status(task_type, RUNNING)

    # The "runner" is the agent description, and it's a map
    # that needs to be serialized before being stored

    @staticmethod
    def pick_next_waiting_task_of_type(task_type, runner):

        result = db_session.query(Task) \
            .filter(Task.status == WAITING,
                    Task.task_type == task_type) \
            .first()

        # Handle missing object
        if not result:
            return None

        serialized_runner = json.dumps(runner)
        update_result = result.run(serialized_runner)

        # XXX Should throw an exception if the
        # update_result isn't empty.
        return result.as_map()

    @staticmethod
    def get_task(task_id):
        result = db_session.query(Task).get(task_id)
        if result:
            return result.as_map()
        else:
            return {}

    @staticmethod
    def do_if_task_exists_error_if_not(task_id, function):
        # XXX This rampant stringification of taskid is unsound.
        task_id = str(task_id)
        task = db_session.query(Task).get(task_id)
        if not task:
            raise ModelException("No such task task_id='%s'" % task_id, 404)
        else:
            return function(task)

    # XXX This design is a bit bogus. It's a bit too astonishing
    # for its own good.
    def check_if_task_exists(self, task_id):
        return self.do_if_task_exists_error_if_not(
            task_id,
            lambda task: task)


    def declare_as_running(self, task_id, runner):
        return self.do_if_task_exists_error_if_not(
            task_id,
            lambda task: task.run(runner))

    @staticmethod
    def do_done(task):
        return task.done()

    def declare_as_done(self, task_id, terminator):
        return self.do_if_task_exists_error_if_not(task_id, lambda task: self.do_done(task))

    @staticmethod
    def create_task(task_type, params):
        json_params = json.dumps(params)
        task = Task(WAITING, task_type, json_params)
        db_session.add(task)
        commit_db()
        new_task = task.as_map()
        return new_task

    @staticmethod
    def nuke(task):
        task_map = task.as_map()
        db_session.delete(task)
        task_map['status'] = 'deleted'
        return task_map

    def delete_task(self, task_id):
        return self.do_if_task_exists_error_if_not(task_id, lambda task: self.nuke(task))
