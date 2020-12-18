import copy

class Node(object):
    def __init__(self):
        self.environments = []
        self.children = []
        self.parent = None
        self.process = ""

    def add_environment(self, environment):
        self.environments.append(environment)

    def add_environments(self , environments):
        self.environments = copy.deepcopy(environments)

    def add_child(self, obj):
        self.children.append(obj)

    def add_parent(self, obj):
        self.parent = obj

    def define_process(self, process):
        self.process += process

    def is_goal(self):
        for e in self.environments:
            for i in range(len(e) - 1):
                if string_to_card(e[i])[0] < string_to_card(e[i + 1])[0]:
                    return False
                if string_to_card(e[i])[1] != string_to_card(e[i + 1])[1]:
                    return False
        return True

    def expand(self):
        for i, e1 in enumerate(self.environments):
            card1 = e1[len(e1) - 1]
            num1, color1 = string_to_card(card1)
            for j, e2 in enumerate(self.environments):
                if i == j:
                    continue
                card2 = e2[len(e2) - 1]
                num2, color2 = string_to_card(card2)
                if num2 > num1:
                    #print("%d to %d" % (i, j))
                    newChild = Node()
                    newChild.add_environments(self.environments)
                    card = newChild.environments[i].pop()
                    if color2 == "#":
                        newChild.environments[j].pop()
                    newChild.environments[j].append(card)
                    #print(newChild.environments)
                    newChild.define_process("%d to %d" % (i, j))
                    newChild.add_parent(self)
                    self.add_child(newChild)


def string_to_card(str):
    l = len(str) - 1
    if l > 0:
        number = int(str[:l])
        color = str[l]
        return number, color
    if l == 0:
        global n
        return n + 1, "#"


def main():
    global n, m, k
    n, m, k = [int(x) for x in input().split()]
    root = Node()
    for i in range(n):
        root.add_environment(input().split())
    print(root.environments)
    #print(root.is_goal())
    root.expand()
    for c in root.children:
        print(c.process)
        print(c.environments)


if __name__ == '__main__':
    main()
