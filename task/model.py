# XXX Too aggressive import list
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import schema, types
from database import Base, db_session, commit_db
from model_exception import ModelException
import json

WAITING="waiting"
RUNNING="running"
DONE="done"

class Task(Base):
    __tablename__ = 'tasks'

    id = schema.Column(Integer, primary_key=True)
    status = Column(String)
    tasktype = Column(String)
    params = Column(String)
    runner = Column(String)

    def __init__(self, status, tasktype, params=None, runner=None):
      self.status = status
      self.runner=runner
      self.tasktype = tasktype
      self.params = params

    ##
    ## Represent the task as a map.  To be used when moving it
    ## as a json representation.
    ##
    def as_map(self):
        return {"taskId": self.id,
                "status": self.status,
                "taskType": self.tasktype,
                "params": json.loads(self.params) }

    ##
    ## The start state needs some special case handling
    ##
    def start(self, runner):
        if (not runner):
            # Use model exception instead.
            return { "HTTP_error_code": 400,
                     "Description":
                     "Attempt to start processing, but no process runner specified" }

        error_desc = self.state_transition(WAITING, RUNNING)
        if (error_desc):
            #  XXXX Raise model exception
            return error_desc
        self.runner = runner
        return {}

    ##
    ## State transition model
    ##
    def state_transition(self, source, destination):
        if (self.status != source):
            # XXX Raise model exception
            return { "HTTP_error_code": 403,
                     "Description":
                     (("Attempt to change status to state '%s' " +
                       "of a task that wasn't in state " +
                       "'%s' but in state %s") % (destination, source, self.status)) }
        else:
            self.status = destination
            return {}

    def done(self):
        return self.state_transition(RUNNING, DONE)

    def run(self, runner):
        result = self.state_transition(WAITING, RUNNING)

        if result:
            return result
        self.runner = runner

    def has_status(self, taskType):
        return self.taskType == taskType

    def has_status(self, status):
        return self.status == status

    def is_waiting(self):
        return self.has_status(WAITING)

    def is_running(self):
        return self.has_status(RUNNING)

    def is_done(self):
        return self.has_status(DONE)

    def has_task_type(self, tasktype):
        return self.tasktype == tasktype


class RDBQueueStorage():

    def list_all_tasks_of_status(self, status):
        result = db_session.query(Task).filter(Task.status == status).all()
        mapped_result = map(lambda x: x.as_map(), result)
        return mapped_result

    def list_all_tasks(self):
        result = db_session.query(Task).all()
        mapped_result = map(lambda x: x.as_map(), result)
        return mapped_result

    def list_all_waiting_tasks(self):
        return self.list_all_tasks_of_status(WAITING)

    def list_all_running_tasks(self):
        return self.list_all_tasks_of_status(RUNNING)

    def list_all_done_tasks(self):
        return self.list_all_tasks_of_status(DONE)

    def list_all_tasks_of_type_with_status(self, tasktype, status):
        result = db_session.query(Task).filter(
            Task.status == status,
            Task.tasktype == tasktype).all()
        mapped_result = map(lambda x: x.as_map(), result)
        return mapped_result        

    def list_all_waiting_tasks_of_type(self, tasktype):
        return self.list_all_tasks_of_type_with_status(tasktype, WAITING)

    def list_all_running_tasks_of_type(self, tasktype):
        return self.list_all_tasks_of_type_with_status(tasktype, RUNNING)


    # The "runner" is the agent description, and it's a map
    # that needs to be serialized before being stored
    
    def pick_next_waiting_task_of_type(self, tasktype, runner):

        result = db_session.query(Task)\
                .filter(Task.status == WAITING,
                        Task.tasktype == tasktype)\
                .first()

        # Handle missing object
        if not result:
            return None

        serialized_runner = json.dumps(runner)
        update_result = result.run(serialized_runner)

        # XXX Should throw an exception if the
        #     update_result isn't empty.
        return result.as_map()

    def get_task(self, taskid):
        result = db_session.query(Task).get(taskid)
        if result:
            return result.as_map()
        else:
            return {}

    def do_if_task_exists_error_if_not(self, taskid, function):
        task_id=str(taskid)
        task = db_session.query(Task).get(task_id)
        if not task:
            raise ModelException("No such task taskid='%s'"%taskid, 404)
        else:
            return function(task)

    # XXX This design is a bit bogus. It's a bit too astonishing
    #     for its own good.
    def check_if_task_exists(self, task_id):
        return self.do_if_task_exists_error_if_not(task_id,
                                            lambda task: task )
        

    def declare_as_running(self, task_id, runner):
        self.do_if_task_exists_error_if_not(task_id,
                                            lambda task: task.run(runner))

    # Hack to ensure that task.done is invoked exactly once
    def do_done(self, task):
        task.done()

    def declare_as_done(self, task_id):
        self.do_if_task_exists_error_if_not(task_id, lambda task: task.done())
        retval = self.do_if_task_exists_error_if_not(task_id, self.do_done)
        return retval
        

    def create_task(self, tasktype, params):
        json_params = json.dumps(params)
        task = Task(WAITING, tasktype, json_params)
        db_session.add(task)
        commit_db()
        mtask = task.as_map()
        return mtask

    def nuke(self, task):
        task_id = task.id
        task_map = task.as_map()
        db_session.delete(task)
        return task_map

    def delete_task(self, task_id):
        self.do_if_task_exists_error_if_not(task_id, lambda task: self.nuke(task))
