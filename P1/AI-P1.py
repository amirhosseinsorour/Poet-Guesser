class Node(object):
    def __init__(self):
        self.environments = []
        self.children = []
        self.parent = None
        self.process = ""

    def add_environment(self, environment):
        self.environments.append(environment)

    def add_child(self, obj):
        self.children.append(obj)

    def add_parent(self, obj):
        self.parent = obj

    def define_process(self, process):
        self.process += process

    def is_goal(self):
        for e in self.environments:
            for i in range(len(e)-1):
                if string_to_card(e[i])[0] < string_to_card(e[i+1])[0]:
                    return False
                if string_to_card(e[i])[1] != string_to_card(e[i+1])[1]:
                    return False
        return True

def string_to_card(str):
    if len(str) == 2:
        number = int(str[0])
        color = str[1]
        return number, color
    elif len(str) == 3:
        number = int(str[:2])
        color = str[2]
        return number, color


def main():
    global n, m, k
    n, m, k = [int(x) for x in input().split()]
    root = Node()
    for i in range(n):
        root.add_environment(input().split())
    print(root.environments)


if __name__ == '__main__':
    main()
