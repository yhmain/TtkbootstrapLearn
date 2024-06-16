import copy
import random
import time


class ToolPprof:
    def __init__(self):
        self.job_status = "Initialize"      # 初始化状态

    @staticmethod
    def get_pod_con_map():
        return {"1com": ["pod1", "vam-pod"], "2com": ["vam-pod", "vsm-pod"], "3com": ["vsm-pod", "pod1"]}

    @staticmethod
    def get_node_columns():
        return ["NAME", "READY", "STATUS", "RESTARTS", "AGE", "IP", "NODE", "NOMINATED NODE", "READINESS GATES"]

    def get_paas_info(self):
        return {"paas_ip": "127.0.0.1", "paas_port": 22, "mt_user": "mtuser", "mt_pwd": "login", "su_user": "root", "su_pwd": "root!!!", "ns": "ns100"}

    @staticmethod
    def get_node_rows_data(pod_type):
        row_data = dict()
        row_data["vam-pod"] = [["vam-pod", "2/2", "STATUS", "RESTARTS", "AGE", "127.0.0.1", "NODE", "NOMINATED NODE", "READINESS GATES"]]
        row_data["vsm-pod"] = [["vsm-pod", "4/4", "STATUS", "RESTARTS", "AGE", "137.2.2.1", "NODE", "NOMINATED NODE", "READINESS GATES"]]

        row_data["appctrl-pod"] = [["appctrl-pod", "3/3", "STATUS", "RESTARTS", "AGE", "137.2.2.1", "NODE", "NOMINATED NODE",
             "READINESS GATES"]]

        row_data["pod1"] = [["pod1-abcd", "4/4", "STATUS", "RESTARTS", "AGE", "157.0.8.1", "NODE", "NOMINATED NODE", "READINESS GATES"],
                            ["pod1-efgh", "4/4", "STATUS", "RESTARTS", "AGE", "157.0.8.1", "NODE", "NOMINATED NODE", "READINESS GATES"]]

        r =  row_data[pod_type]

        temp_row_list = list()
        for i in range(100):
            for row in r:
                # self.node_table.insert_row('end', row)
                temp_row = copy.deepcopy(row)
                temp_row[0] = "{0}-{1}".format(i, row[0])
                temp_row_list.append(temp_row)

        return temp_row_list

    @staticmethod
    def get_pprof_type():
        return ["cpu", "heap"]

    def __set_job_status(self, job_status):
        self.job_status = job_status

    def do_curl_job(self, pod_type, pod_ip, curl_type):
        self.pod_type = pod_type
        self.pro_val = 0
        self.pro_info = "Start login node  Progress: {0}%".format(self.pro_val)
        self.__set_job_status("Working")
        time.sleep(random.randint(1,5)) # 模拟登录节点
        self.pro_val = 5
        self.pro_info = "Start login docker  Progress: {0}%".format(self.pro_val)
        time.sleep(random.randint(1, 5))  # 模拟登录容器
        self.pro_val = 10
        curl_cost = random.randint(10, 20)
        self.pro_info = "Start curl pprof: {0}s  Progress: {1}%".format(int(curl_cost/3), self.pro_val)
        time.sleep(int(curl_cost/3))  # 模拟采集pprof
        self.pro_val = 40
        self.pro_info = "Working--> curl pprof: {0}s  Progress: {1}%".format(int(curl_cost / 3), self.pro_val)
        time.sleep(int(curl_cost / 3))  # 模拟采集pprof
        self.pro_val = 70
        self.pro_info = "Working--> curl pprof: {0}s  Progress: {1}%".format(int(curl_cost / 3), self.pro_val)
        time.sleep(int(curl_cost / 3))  # 模拟采集pprof
        self.__set_job_status("End")
        self.pro_val = 100
        self.pro_info = "Finish--> curl pprof: {0}s  Progress: {1}%".format(int(curl_cost / 3), self.pro_val)

    def is_finished_job(self):
        print(self.pod_type, "now: ", self.job_status)
        if self.job_status == "End":
            return True, self.pro_val, self.pro_info
        return False, self.pro_val, self.pro_info
