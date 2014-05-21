# XXX Too aggressive import list
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import schema, types
from database import Base, db_session
import json

class Task(Base):
    __tablename__ = 'tasks'

    id = schema.Column(Integer, primary_key=True)
    status = Column(String)
    tasktype = Column(String)
    params = Column(String)
    runner = Column(String)

    WAITING="waiting"
    RUNNING="running"
    DONE="done"

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
            return { "HTTP_error_code": 400,
                     "Description":
                     "Attempt to start processing, but no process runner specified" }

        error_desc = self.state_transition(self.WAITING, self.RUNNING)
        if (error_desc):
            print "State transition failed %r" % (error_desc)
            return error_desc
        self.runner = runner
        return {}

    ##
    ## State transition model
    ##
    def state_transition(self, source, destination):
        if (self.status != source):
            return { "HTTP_error_code": 404,
                     "Description":
                     (("Attempt to change status to state '%s' " +
                       "of a task that wasn't in state " +
                       "'%s' but in state %s") % (destination, source, self.status)) }
        else:
            self.status = destination
            return {}

    def done(self):
        return self.state_transition(self.RUNNING, self.DONE)

    def run(self, runner):
        result = self.state_transition(self.WAITING, self.RUNNING)
        if not result:
            self.runner = runner


    def has_status(self, taskType):
        return self.taskType == taskType

    def has_status(self, status):
        return self.status == status

    def is_waiting(self):
        return self.has_status(self.WAITING)

    def is_running(self):
        return self.has_status(self.RUNNING)

    def is_done(self):
        return self.has_status(self.DONE)

    def has_task_type(self, tasktype):
        return self.tasktype == tasktype


class RDBQueueStorage():

    def list_all_tasks_of_status(self, status):
        # XXX  Bogus static string.  Use better encapsulation
        result = db_session.query(Task).filter(Task.status == status).all()
        mapped_result = map(lambda x: x.as_map(), result)
        return mapped_result

    def list_all_waiting_tasks(self):
        return self.list_all_tasks_of_status("waiting")

    def list_all_running_tasks(self):
        return self.list_all_tasks_of_status("running")


    def list_all_done_tasks(self):
        return self.list_all_tasks_of_status("done")

    def list_all_waiting_tasks_of_type(self, tasktype):
        result = db_session.query(Task).filter(
            Task.status == "waiting",
            Task.tasktype == tasktype).all()
        mapped_result = map(lambda x: x.as_map(), result)
        return mapped_result        



    def pick_next_waiting_task_of_type(self, tasktype, runner):
        # XXX  Bogus static string.  Use better encapsulation
        # XXX2 Repeated code.

        result = db_session.query(Task)\
                .filter(Task.status == "waiting",
                        Task.tasktype == tasktype)\
                .first()

        # Handle missing object
        if not result:
            return None

        update_result = result.run(runner)
        # XXX Should throw an exception if the
        #     update_result isn't empty.
        return result.as_map()

    def get_task(self, taskid):
        result = db_session.query(Task).get(taskid)
        if result:
            return result.as_map()
        else:
            return {}

    def check_if_task_exists(self, taskid):
        task_id=str(taskid)
        result = db_session.query(Task).get(task_id)
        if not result :
            return { "HTTP_error_code": 404,
                     "Description":
                     ("No such task taskid='%s'"%taskid)}
        else:
            return {}

    def declare_as_running(self, taskid, runner):
        result = db_session.query(Task).get(taskid)
        if not result:
            return { "HTTP_error_code": 404,
                     "Description":
                     ("No such task taskid='%s'"%taskid)}

        result.run(runner)
        return {}

    def declare_as_done(self, taskid):
        result = db_session.query(Task).get(taskid)
        if not result :
            return { "HTTP_error_code": 404,
                     "Description":
                     ("No such task taskid='%s'"%taskid)}

        result.done()
        return {}


    def create_task(self, tasktype, params):
        json_params = json.dumps(params)
        task = Task("waiting", tasktype, json_params)
        db_session.add(task)
        db_session.commit()
        mtask =task.as_map()
        return mtask


    def delete_task(self, taskid):
        (result, found_it) = db_session.query(Task, Task.id == taskid).first()

        if found_it:
            db_session.delete(result)
            # XXX Check deletion result
            return {}
        else:
            # XXX Repeated code
            return { "HTTP_error_code": 404,
                     "Description":
                     ("No such task taskid='%s'"%taskid)}

