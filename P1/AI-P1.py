class Node(object):
    def __init__(self):
        self.environments = []
        self.children = []

    def add_environment(self, environment):
        self.environments.append(environment)

    def add_child(self , obj):
        self.children.append(obj)
