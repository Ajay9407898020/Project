from Project.lib.common.remote_command import RemoteCommand


class Linux:
    def __init__(self, ip, username, password):
        self.remote_command = RemoteCommand(host=ip, user=username, password=password)

    def get_all_conf(self):
        pass

    def get_all_perf(self):
        pass




