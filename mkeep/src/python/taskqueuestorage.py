

class Task:

    WAITING="waiting"
    RUNNING="running"
    DONE="done"

    def __init__(self, id, status, tasktype):
      self.id = id
      self.status = status
      self.runner=None
      self.tasktype = tasktype

    def as_map(self):
        return {"taskId": self.id,
                "status": self.status,
                "taskType": self.tasktype}

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

    def start(self, runner):
        print "starting"
        if (not runner):
            print "Starter error"
            return { "HTTP_error_code": 400,
                     "Description":
                     "Attempt to start processing, but no process runner specified" }

        print "Transitioning state"
        error_desc = self.state_transition(self.WAITING, self.RUNNING)
        print "State transitioned"
        if (error_desc):
            print "State transition failed %r" % (error_desc)
            return error_desc
        print "setting runner"
        self.runner = runner
        return {}


    def done(self):
        return state_transition(self.RUNNING, self.DONE)

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


class TaskQueueStorage:


    def __init__(self):
      self.next_taskid = 1
      self.tasks = {}

    def list_all_waiting_tasks(self):
        return filter(lambda x: x.is_waiting(), self.tasks.values())

    def list_all_running_tasks(self):
        return filter (lambda x: x.is_running(), self.tasks.values())


    def list_all_done_tasks(self):
        return filter(lambda x: x.is_done(), self.tasks.values())

    def list_all_waiting_tasks_of_type(self, tasktype):
        return filter (lambda x: x.has_task_type(tasktype),
                       self.list_all_waiting_tasks())

    def check_if_task_exists(self, taskid):
        if not(taskid in self.tasks):
            return { "HTTP_error_code": 404,
                     "Description":
                     "No such task"}
        else:
            return {}

    def pick_next_waiting_task_of_type(self, tasktype, runner):
        waiting_tasks = self.list_all_waiting_tasks_of_type(tasktype)
        print "hello"
        if waiting_tasks:
            print "a, tasks = %r" %(waiting_tasks)
            picked_task=waiting_tasks.pop(0)
            print "b"
            error_description=picked_task.start(runner)
            if error_description:
                print  "e"   
                return error_description
            print  "c"
            return picked_task.as_map()
        else:
            print "d"            
            return {}

    def delare_as_done(self, taskid):
        errors=self.check_if_task_exists(taskid)
        if errors:
            return errors
        else:
            task=self.tasks[taskid]
            return task.done();

    def create_task(self, tasktype):
        taskid = self.next_taskid
        self.next_taskid = self.next_taskid + 1
        task = Task(taskid, "waiting", tasktype)
        self.tasks[taskid] = task
        return task.as_map()

    def delete_task(self, taskid):
        errors=self.check_if_task_exists(taskid)
        if errors:
            return errors
        else:
            del tasks[taskid]
            return {}        
        



        


    
