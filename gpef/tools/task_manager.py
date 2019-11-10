import os
import pickle
import pandas as pd


class TaskManager:
    def __init__(self, task_id):
        self.CURRENT_DIR = os.getcwd()
        self.tmp_path = os.path.join(self.CURRENT_DIR, 'task_manager%d.pickle' % task_id)
        self.tasks_remain = []
        self.tasks_finished = []
        self.tasks_failed = []

    def print_status(self):
        print("TaskManager: %d remain, %d finished, %d failed." % (
            len(self.tasks_remain), len(self.tasks_finished), len(self.tasks_failed)))

    def generate_task_list(self, csv_path):
        if os.path.exists(self.tmp_path):
            try:
                self.load_tmp()
            except Exception as e:
                print("TaskManager.generate_task_list().self.load_tmp().Exception: %s" % e)
        else:
            self.tasks_finished.clear()
            try:
                df = pd.read_csv(csv_path)
                self.tasks_remain = list(df.T.to_dict().values())
            except Exception as e:
                self.tasks_remain = []
                print("TaskManager.generate_task_list().list_of_dict_from_csv().Exception: %s" % e)
        self.print_status()

    def update_task_status(self, status):
        if len(self.tasks_remain):
            task = self.tasks_remain.pop(0)
            if status == "success":
                self.tasks_finished.append(task)
            else:
                self.tasks_failed.append(task)
            self.print_status()
            self.save_tmp()
        else:
            print("TaskManager.update_task_status().Exception: No task to update")

    def get_next_task(self):
        if len(self.tasks_remain):
            return self.tasks_remain[0]
        else:
            return None

    def has_next_task(self):
        return len(self.tasks_remain) > 0

    def save_tmp(self):
        try:
            with open(self.tmp_path, 'wb') as f:
                pickle.dump([self.tasks_remain, self.tasks_finished, self.tasks_failed], f)
        except Exception as e:
            print("TaskManager.save_tmp().Exception: %s" % e)

    def load_tmp(self):
        try:
            with open(self.tmp_path, 'rb') as f:
                [self.tasks_remain, self.tasks_finished, self.tasks_failed] = pickle.load(f)
        except Exception as e:
            print("TaskManager.load_tmp().Exception: %s" % e)
