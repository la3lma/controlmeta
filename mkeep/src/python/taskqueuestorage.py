

class Task:

    WAITING="waiting"
    RUNNING="running"
    DONE="done"

    def __init__(self, id, status, tasktype):
      self.id = id
      self.status = status
      self.runner=None
      self.tasktype = tasktype

    def asMap(self):
        return {"taskId": self.id,
                "status": self.status,
                "taskType": self.tasktype}

    def state_transition(self, source, destination):
        if (self.status != SOURCE):
            return { "HTTP_error_code": 404,
                     "Description":
                     (("Attempt to change status to state '%s' " +
                       "of a task that wasn't in state " +
                       "'%s' but in state %s") % (destination, source, self.status)) }
        else:
            self.status = destination
            return {}

    def start(self, runner):
        if (not runner):
            return { "HTTP_error_code": 400,
                     "Description":
                     "Attempt to start processing, but no process runner specified" }

        error_desc = state_transition(None, RUNNING)
        if (not error_desc):
            self.runner = runner
        return error_desc

    def done(self):
        return state_transition(RUNNING, DONE)


    def hasStatus(self, taskType):
        return self.taskType == taskType

    def hasStatus(self, status):
        return self.status == status

    def isWaiting(self):
        return hasStatus(WAITING)

    def isRunning(self):
        return hasStatus(RUNNING)

    def isDone(self):
        return hasStatus(DONE)


class TaskQueueStorage:


    def __init__(self):
      self.next_taskid = 1
      self.tasks = {}

    def list_all_waiting_tasks(self):
        return filter(tasks, lambda x: x.isWaiting())

    def list_all_running_tasks(self):
        return filter(tasks, lambda x: x.isRunning())


    def list_all_done_tasks(self):
        return filter(tasks, lambda x: x.isDone())

    def list_all_waiting_tasks_of_type(self, tasktype):
        return filter (self.list_all_waiting_tasks(),
                       lambda x: x.hasTaskType(tasktype))

    def check_if_task_exists(self, taskid):
        if not(taskid in tasks):
            return { "HTTP_error_code": 404,
                     "Description":
                     "No such task"}
        else:
            return {}

    def pick_next_waiting_task_of_type(self, tasktype, runner):
        waiting_tasks = self.list_all_waiting_tasks()
        if waiting_tasks:
            picked_task=waiting_tasks.pop(1)
            picked_task.start(runner)
            return picked_task
        else:
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
        return task.asMap()


    def delete_task(self, taskid):
        errors=self.check_if_task_exists(taskid)
        if errors:
            return errors
        else:
            del tasks[taskid]
            return {}        
        



        


    
