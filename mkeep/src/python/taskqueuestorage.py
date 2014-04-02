
class TaskQueueStorage:

    waiting_tasks = {}
    running_tasks = {}
    done_tasks = {}

    def list_all_waiting_tasks(self):
        return {}


    def list_all_running_tasks(self):
        return {}

    def list_all_done_tasks(self):
        return {}


    def list_all_waiting_tasks_of_type(self, type):
        return []


    def next_waiting_task_of_type(self, type):
        return {}


    def pick_next_waiting_task_of_type(self, type):
        return {}

    def delare_as_done(self, taskid):
        return {}

    def create_task(self, taskid):
        return {"taskid": 1}

    def delete_taskid(self, type):
        return {}
    


        


    
