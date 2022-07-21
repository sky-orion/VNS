import copy

import numpy as np

from Initialization import initialization
from utils import load_instance, calculate_cost, improve


class Relocationmove_operator():
    def __init__(self, instance):
        self.instance = instance
        self.distance_matrix = instance["distance_matrix"]
        return

    def operate(self, route, random_choice_best=False, random_choice=False):
        route = copy.deepcopy(route)
        bestgain = 0
        bestlocationa = -1
        bestlocationb = -1
        bestroutei = -1
        bestroutej = -1
        gainlist = []
        if random_choice:
            sign = True
            while sign:
                bestroutei, bestroutej = np.random.choice(len(route), 2, replace=False).tolist()
                subtouri = route[bestroutei]
                subtourj = route[bestroutej]
                while len(subtouri.route) == 2 or len(subtourj.route) == 2:
                    bestroutei, bestroutej = np.random.choice(len(route), 2, replace=False).tolist()
                    subtouri = route[bestroutei]
                    subtourj = route[bestroutej]
                    # print(len(subtouri.route),len(subtouri.route))
                bestlocationa = np.random.randint(low=1, high=len(subtouri.route) - 1)
                bestlocationb = np.random.randint(low=1, high=len(subtourj.route) - 1)
                gain = self.computergain(subtouri, subtourj, bestlocationa, bestlocationb)  # 把a插入b位置
                # print(len(subtouri.route), len(subtourj.route), bestroutei, bestroutej,gain)
                if abs(gain) < 100:
                    sign = False
        else:
            for i in range(len(route)):
                subtouri = route[i]
                if len(subtouri.route) == 2:
                    continue
                for j in range(i + 1, len(route)):
                    subtourj = route[j]
                    if len(subtourj.route) == 2:
                        continue
                    # 交换顾客
                    for a in range(1, len(subtouri.route) - 1):
                        for b in range(1, len(subtourj.route) - 1):
                            gain = self.computergain(subtouri, subtourj, a, b)  # 把a插入b位置
                            # print(gain)
                            if gain > 0:
                                tmpgain = gain
                                tmplocationa = a
                                tmplocationb = b
                                tmproutei = i
                                tmproutej = j
                                gainthis = [tmpgain, tmplocationa, tmplocationb, tmproutei, tmproutej]
                                gainlist.append(gainthis)
                            if gain > bestgain:
                                bestgain = gain
                                bestlocationa = a
                                bestlocationb = b
                                bestroutei = i
                                bestroutej = j
        if random_choice:
            newroutei = copy.deepcopy(route[bestroutei])
            newroutej = copy.deepcopy(route[bestroutej])
            newroutei.route.pop(bestlocationa)
            newroutej.route.insert(bestlocationb, route[bestroutei].route[bestlocationa])
            self.computercost(newroutei)
            self.computercost(newroutej)
            route[bestroutei] = newroutei
            route[bestroutej] = newroutej
        else:
            if bestgain != 0:
                if random_choice_best:
                    choice = np.random.randint(0, len(gainlist))
                    listchoice = gainlist[choice]
                    bestgain, bestlocationa, bestlocationb, bestroutei, bestroutej = listchoice[0], listchoice[1], \
                                                                                     listchoice[2], listchoice[3], \
                                                                                     listchoice[4]
                    # print("bestgain", bestgain)
                    newroutei = copy.deepcopy(route[bestroutei])
                    newroutej = copy.deepcopy(route[bestroutej])
                    newroutei.route.pop(bestlocationa)
                    newroutej.route.insert(bestlocationb, route[bestroutei].route[bestlocationa])
                    self.computercost(newroutei)
                    self.computercost(newroutej)
                    route[bestroutei] = newroutei
                    route[bestroutej] = newroutej
                else:
                    # print("bestgain", bestgain)
                    newroutei = copy.deepcopy(route[bestroutei])
                    newroutej = copy.deepcopy(route[bestroutej])
                    newroutei.route.pop(bestlocationa)
                    newroutej.route.insert(bestlocationb, route[bestroutei].route[bestlocationa])
                    self.computercost(newroutei)
                    self.computercost(newroutej)
                    route[bestroutei] = newroutei
                    route[bestroutej] = newroutej
        return route

    def computergain(self, subtouri, subtourj, a, b):
        newroutei = copy.deepcopy(subtouri)
        newroutej = copy.deepcopy(subtourj)
        newroutei.route.pop(a)
        newroutej.route.insert(b, subtouri.route[a])
        self.computercost(newroutei)
        self.computercost(newroutej)
        gain = subtouri.cost + subtourj.cost - newroutej.cost - newroutei.cost
        return gain

    def computercost(self, tour):
        tour.reset()
        lastnode = tour.route[0]
        lastnodeindex = int(lastnode.replace("d", ""))
        depotid = lastnodeindex
        for i in range(1, len(tour.route) - 1):
            name = tour.route[i]
            nodeindex = int(name.replace("c", "")) + self.instance["number_of_depots"] - 1
            tour.nowtime = tour.nowtime + self.distance_matrix[lastnodeindex][nodeindex]
            tour.cost = tour.cost + tour.nowtime
            customer = "customer_{}".format(name.replace("c", ""))
            if self.instance[customer]["demand"] + tour.load > self.instance["depots"][depotid][
                "maximum_load_of_a_vehicle"]:
                tour.cost = 99999999
                return 99999999
            tour.load = tour.load + self.instance[customer]["demand"]
            lastnodeindex = nodeindex
        return tour.cost


class twoExchangemove_operator():
    def __init__(self, instance):
        self.instance = instance
        self.distance_matrix = instance["distance_matrix"]
        return

    def operate(self, route, random_choice_best=False, random_choice=False):
        route = copy.deepcopy(route)
        bestgain = 0
        bestlocationa = -1
        bestlocationb = -1
        bestroutei = -1
        bestroutej = -1
        gainlist = []
        if random_choice:
            sign = True
            while sign:
                bestroutei, bestroutej = np.random.choice(len(route), 2, replace=False).tolist()
                subtouri = route[bestroutei]
                subtourj = route[bestroutej]
                while len(subtouri.route) == 2 or len(subtourj.route) == 2:
                    bestroutei, bestroutej = np.random.choice(len(route), 2, replace=False).tolist()
                    subtouri = route[bestroutei]
                    subtourj = route[bestroutej]
                bestlocationa = np.random.randint(low=1, high=len(subtouri.route) - 1)
                bestlocationb = np.random.randint(low=1, high=len(subtourj.route) - 1)
                gain = round(self.computergain(subtouri, subtourj, bestlocationa, bestlocationb), 5)
                # print(len(subtouri.route), len(subtourj.route), bestroutei, bestroutej,gain)
                if abs(gain) < 100:
                    sign = False

        else:
            for i in range(len(route)):
                subtouri = route[i]
                if len(subtouri.route) == 2:
                    continue
                for j in range(i + 1, len(route)):  # 两条路径不一样
                    subtourj = route[j]
                    if len(subtourj.route) == 2:
                        continue
                    # 交换depot
                    for a in [0, len(subtouri.route) - 1]:
                        for b in [0, len(subtourj.route) - 1]:
                            gain = round(self.computergain(subtouri, subtourj, a, b), 5)
                            # print(gain)
                            if gain > 0:
                                tmpgain = gain
                                tmplocationa = a
                                tmplocationb = b
                                tmproutei = i
                                tmproutej = j
                                gainthis = [tmpgain, tmplocationa, tmplocationb, tmproutei, tmproutej]
                                gainlist.append(gainthis)
                            if gain > bestgain:
                                bestgain = gain
                                bestlocationa = a
                                bestlocationb = b
                                bestroutei = i
                                bestroutej = j
                    # 交换顾客
                    for a in range(1, len(subtouri.route) - 1):
                        for b in range(1, len(subtourj.route) - 1):
                            gain = round(self.computergain(subtouri, subtourj, a, b), 5)
                            # print(gain)
                            if gain > 0:
                                tmpgain = gain
                                tmplocationa = a
                                tmplocationb = b
                                tmproutei = i
                                tmproutej = j
                                gainthis = [tmpgain, tmplocationa, tmplocationb, tmproutei, tmproutej]
                                gainlist.append(gainthis)
                            if gain > bestgain:
                                bestgain = gain
                                bestlocationa = a
                                bestlocationb = b
                                bestroutei = i
                                bestroutej = j
        if random_choice:
            newroutei = copy.deepcopy(route[bestroutei])
            newroutej = copy.deepcopy(route[bestroutej])
            newroutei.route[bestlocationa] = route[bestroutej].route[bestlocationb]
            newroutej.route[bestlocationb] = route[bestroutei].route[bestlocationa]
            newroutei.route[-1] = newroutei.route[0]
            newroutej.route[-1] = newroutej.route[0]
            self.computercost(newroutei)
            self.computercost(newroutej)
            route[bestroutei] = newroutei
            route[bestroutej] = newroutej
        else:
            if bestgain >= 1e-5:
                if random_choice_best:
                    choice = np.random.randint(0, len(gainlist))
                    listchoice = gainlist[choice]
                    bestgain, bestlocationa, bestlocationb, bestroutei, bestroutej = listchoice[0], listchoice[1], \
                                                                                     listchoice[2], listchoice[3], \
                                                                                     listchoice[4]
                    # print("bestgain", bestgain)
                    newroutei = copy.deepcopy(route[bestroutei])
                    newroutej = copy.deepcopy(route[bestroutej])
                    newroutei.route[bestlocationa] = route[bestroutej].route[bestlocationb]
                    newroutej.route[bestlocationb] = route[bestroutei].route[bestlocationa]
                    newroutei.route[-1] = newroutei.route[0]
                    newroutej.route[-1] = newroutej.route[0]
                    self.computercost(newroutei)
                    self.computercost(newroutej)
                    route[bestroutei] = newroutei
                    route[bestroutej] = newroutej
                else:
                    # print("bestgain", bestgain)
                    newroutei = copy.deepcopy(route[bestroutei])
                    newroutej = copy.deepcopy(route[bestroutej])
                    newroutei.route[bestlocationa] = route[bestroutej].route[bestlocationb]
                    newroutej.route[bestlocationb] = route[bestroutei].route[bestlocationa]
                    newroutei.route[-1] = newroutei.route[0]
                    newroutej.route[-1] = newroutej.route[0]
                    self.computercost(newroutei)
                    self.computercost(newroutej)
                    route[bestroutei] = newroutei
                    route[bestroutej] = newroutej
        return route

    def computergain(self, subtouri, subtourj, a, b):
        newroutei = copy.deepcopy(subtouri)
        newroutej = copy.deepcopy(subtourj)
        newroutei.route[a] = subtourj.route[b]
        newroutej.route[b] = subtouri.route[a]
        self.computercost(newroutei)
        self.computercost(newroutej)
        gain = subtouri.cost + subtourj.cost - newroutej.cost - newroutei.cost
        return gain

    def computercost(self, tour):
        tour.reset()
        lastnode = tour.route[0]
        lastnodeindex = int(lastnode.replace("d", ""))
        depotid = lastnodeindex
        for i in range(1, len(tour.route) - 1):
            name = tour.route[i]
            nodeindex = int(name.replace("c", "")) + self.instance["number_of_depots"] - 1
            tour.nowtime = tour.nowtime + self.distance_matrix[lastnodeindex][nodeindex]
            tour.cost = tour.cost + tour.nowtime
            customer = "customer_{}".format(name.replace("c", ""))
            if self.instance[customer]["demand"] + tour.load > self.instance["depots"][depotid][
                "maximum_load_of_a_vehicle"]:
                tour.cost = 99999999
                return 99999999
            tour.load = tour.load + self.instance[customer]["demand"]
            lastnodeindex = nodeindex
        return tour.cost


class twoOptmove_operator():
    def __init__(self, instance):
        self.instance = instance
        self.distance_matrix = instance["distance_matrix"]

        return

    def operate(self, route, random_choice_best=False, random_choice=False):
        route = copy.deepcopy(route)
        bestgain = 0
        bestlocationa = -1
        bestlocationb = -1
        bestroutei = -1
        bestroutej = -1
        gainlist = []
        if random_choice:
            sign = True
            while sign:
                bestroutei, bestroutej = np.random.choice(len(route), 2, replace=False).tolist()
                subtouri = route[bestroutei]
                subtourj = route[bestroutej]
                while len(subtouri.route) <= 3 or len(subtourj.route) <= 3:
                    bestroutei, bestroutej = np.random.choice(len(route), 2, replace=False).tolist()
                    subtouri = route[bestroutei]
                    subtourj = route[bestroutej]
                bestlocationa = np.random.randint(low=1, high=len(subtouri.route) - 2)
                bestlocationb = np.random.randint(low=1, high=len(subtourj.route) - 2)
                gain = self.computergain(subtouri, subtourj, bestlocationa, bestlocationb)
                # print(len(subtouri.route), len(subtourj.route), bestroutei, bestroutej,gain)
                if abs(gain) < 100:
                    sign = False
        else:
            for i in range(len(route)):
                subtouri = route[i]
                if len(subtouri.route) == 2:
                    continue
                # 路径内
                if len(subtouri.route) >= 6:
                    for a in range(1, len(subtouri.route) - 4):
                        for b in range(a + 3, len(subtouri.route) - 1):
                            newroutei = copy.deepcopy(subtouri)
                            tmp = list(reversed(subtouri.route[a + 1:b]))
                            for k in range(a + 1, b):
                                newroutei.route[k] = tmp[k - a - 1]
                            self.computercost(newroutei)
                            gain = subtouri.cost - newroutei.cost
                            if gain > 0:
                                tmpgain = gain
                                tmplocationa = a
                                tmplocationb = b
                                tmproutei = i
                                tmproutej = i
                                gainthis = [tmpgain, tmplocationa, tmplocationb, tmproutei, tmproutej]
                                gainlist.append(gainthis)
                            if gain > bestgain:
                                bestgain = gain
                                bestlocationa = a
                                bestlocationb = b
                                bestroutei = i
                                bestroutej = i
                # 路径间
                for j in range(i + 1, len(route)):  # 两条路径不一样
                    subtourj = route[j]
                    if len(subtourj.route) == 2:
                        continue
                    for a in range(1, len(subtouri.route) - 2):
                        for b in range(1, len(subtourj.route) - 2):
                            ci, cj = a, a + 1
                            cs, cr = b, b + 1
                            gain = self.computergain(subtouri, subtourj, ci, cs)
                            # print(gain)
                            if gain > 0:
                                tmpgain = gain
                                tmplocationa = a
                                tmplocationb = b
                                tmproutei = i
                                tmproutej = j
                                gainthis = [tmpgain, tmplocationa, tmplocationb, tmproutei, tmproutej]
                                gainlist.append(gainthis)
                            if gain > bestgain:
                                bestgain = gain
                                bestlocationa = a
                                bestlocationb = b
                                bestroutei = i
                                bestroutej = j
        if random_choice:
            newroutei = copy.deepcopy(route[bestroutei])
            newroutej = copy.deepcopy(route[bestroutej])
            if bestroutei != bestroutej:
                del newroutei.route[bestlocationa + 1:len(route[bestroutei].route)]
                del newroutej.route[bestlocationb + 1: len(route[bestroutej].route)]
                for index in range(bestlocationb + 1, len(route[bestroutej].route)):
                    newroutei.route.append(route[bestroutej].route[index])
                for index in range(bestlocationa + 1, len(route[bestroutei].route)):
                    newroutej.route.append(route[bestroutei].route[index])
                newroutei.route[-1] = newroutei.route[0]
                newroutej.route[-1] = newroutej.route[0]
                self.computercost(newroutei)
                self.computercost(newroutej)
                route[bestroutei] = newroutei
                route[bestroutej] = newroutej
            else:
                newroutei = copy.deepcopy(route[bestroutei])
                tmp = list(reversed(route[bestroutei].route[bestlocationa + 1:bestlocationb]))
                for k in range(bestlocationa + 1, bestlocationb):
                    newroutei.route[k] = tmp[k - bestlocationa - 1]
                self.computercost(newroutei)
                route[bestroutei] = newroutei
        else:
            if bestgain != 0:
                if random_choice_best:
                    choice = np.random.randint(0, len(gainlist))
                    listchoice = gainlist[choice]
                    bestgain, bestlocationa, bestlocationb, bestroutei, bestroutej = listchoice[0], listchoice[1], \
                                                                                     listchoice[2], listchoice[3], \
                                                                                     listchoice[4]
                    newroutei = copy.deepcopy(route[bestroutei])
                    newroutej = copy.deepcopy(route[bestroutej])
                    if bestroutei != bestroutej:
                        del newroutei.route[bestlocationa + 1:len(route[bestroutei].route)]
                        del newroutej.route[bestlocationb + 1: len(route[bestroutej].route)]
                        for index in range(bestlocationb + 1, len(route[bestroutej].route)):
                            newroutei.route.append(route[bestroutej].route[index])
                        for index in range(bestlocationa + 1, len(route[bestroutei].route)):
                            newroutej.route.append(route[bestroutei].route[index])
                        newroutei.route[-1] = newroutei.route[0]
                        newroutej.route[-1] = newroutej.route[0]
                        self.computercost(newroutei)
                        self.computercost(newroutej)
                        route[bestroutei] = newroutei
                        route[bestroutej] = newroutej
                    else:
                        newroutei = copy.deepcopy(route[bestroutei])
                        tmp = list(reversed(route[bestroutei].route[bestlocationa + 1:bestlocationb]))
                        for k in range(bestlocationa + 1, bestlocationb):
                            newroutei.route[k] = tmp[k - bestlocationa - 1]
                        self.computercost(newroutei)
                        route[bestroutei] = newroutei
                else:
                    newroutei = copy.deepcopy(route[bestroutei])
                    newroutej = copy.deepcopy(route[bestroutej])
                    if bestroutei != bestroutej:
                        del newroutei.route[bestlocationa + 1:len(route[bestroutei].route)]
                        del newroutej.route[bestlocationb + 1: len(route[bestroutej].route)]
                        for index in range(bestlocationb + 1, len(route[bestroutej].route)):
                            newroutei.route.append(route[bestroutej].route[index])
                        for index in range(bestlocationa + 1, len(route[bestroutei].route)):
                            newroutej.route.append(route[bestroutei].route[index])
                        newroutei.route[-1] = newroutei.route[0]
                        newroutej.route[-1] = newroutej.route[0]
                        self.computercost(newroutei)
                        self.computercost(newroutej)
                        route[bestroutei] = newroutei
                        route[bestroutej] = newroutej
                    else:
                        newroutei = copy.deepcopy(route[bestroutei])
                        tmp = list(reversed(route[bestroutei].route[bestlocationa + 1:bestlocationb]))
                        for k in range(bestlocationa + 1, bestlocationb):
                            newroutei.route[k] = tmp[k - bestlocationa - 1]
                        self.computercost(newroutei)
                        route[bestroutei] = newroutei
        # print("bestgain", bestgain)
        return route

    def computergain(self, subtouri, subtourj, a, b):
        newroutei = copy.deepcopy(subtouri)
        newroutej = copy.deepcopy(subtourj)
        del newroutei.route[a + 1:len(subtouri.route)]
        del newroutej.route[b + 1:len(subtourj.route)]
        for index in range(b + 1, len(subtourj.route)):
            newroutei.route.append(subtourj.route[index])
        for index in range(a + 1, len(subtouri.route)):
            newroutej.route.append(subtouri.route[index])
        self.computercost(newroutei)
        self.computercost(newroutej)
        gain = subtouri.cost + subtourj.cost - newroutej.cost - newroutei.cost
        return gain

    def computercost(self, tour):
        tour.reset()
        lastnode = tour.route[0]
        lastnodeindex = int(lastnode.replace("d", ""))
        depotid = lastnodeindex
        for i in range(1, len(tour.route) - 1):
            name = tour.route[i]
            nodeindex = int(name.replace("c", "")) + self.instance["number_of_depots"] - 1
            tour.nowtime = tour.nowtime + self.distance_matrix[lastnodeindex][nodeindex]
            tour.cost = tour.cost + tour.nowtime
            customer = "customer_{}".format(name.replace("c", ""))
            if self.instance[customer]["demand"] + tour.load > self.instance["depots"][depotid][
                "maximum_load_of_a_vehicle"]:
                tour.cost = 99999999
                return 99999999
            tour.load = tour.load + self.instance[customer]["demand"]
            lastnodeindex = nodeindex
        return tour.cost


class ArcNodeExchangemove_operator():
    def __init__(self, instance):
        self.instance = instance
        self.distance_matrix = instance["distance_matrix"]
        return

    def operate(self, route, random_choice_best=False, random_choice=False):
        route = copy.deepcopy(route)
        bestgain = 0
        bestlocationa = -1
        bestlocationb = -1
        bestroutei = -1
        bestroutej = -1
        gainlist = []
        if random_choice:
            sign = True
            while sign:
                bestroutei, bestroutej = np.random.choice(len(route), 2, replace=False).tolist()
                subtouri = route[bestroutei]
                subtourj = route[bestroutej]
                while len(subtouri.route) <= 3 or len(subtourj.route) < 3:
                    bestroutei, bestroutej = np.random.choice(len(route), 2, replace=False).tolist()
                    subtouri = route[bestroutei]
                    subtourj = route[bestroutej]
                bestlocationa = np.random.randint(low=1, high=len(subtouri.route) - 2)
                bestlocationb = np.random.randint(low=1, high=len(subtourj.route) - 1)
                gain = self.computergain(subtouri, subtourj, bestlocationa, bestlocationa + 1, bestlocationb)
                # print(len(subtouri.route), len(subtourj.route), bestroutei, bestroutej, gain)
                if abs(gain) < 100:
                    sign = False
        else:
            for i in range(len(route)):
                subtouri = route[i]
                if len(subtouri.route) == 2:
                    continue
                # 路径间
                for j in range(len(route)):  # 两条路径不一样
                    if i == j:
                        continue  # 不进行路径内搜索
                    subtourj = route[j]
                    if len(subtourj.route) == 2:
                        continue
                    for a in range(1, len(subtouri.route) - 2, 1):
                        for b in range(1, len(subtourj.route) - 1):
                            ci, cj = a, a + 1
                            cs, cr = b, b + 1
                            gain = self.computergain(subtouri, subtourj, ci, cj, cs)
                            # print(gain)
                            if gain > 0:
                                tmpgain = gain
                                tmplocationa = a
                                tmplocationb = b
                                tmproutei = i
                                tmproutej = j
                                gainthis = [tmpgain, tmplocationa, tmplocationb, tmproutei, tmproutej]
                                gainlist.append(gainthis)
                            if gain > bestgain:
                                bestgain = gain
                                bestlocationa = a
                                bestlocationb = b
                                bestroutei = i
                                bestroutej = j
        if random_choice:
            newroutei = copy.deepcopy(route[bestroutei])
            newroutej = copy.deepcopy(route[bestroutej])
            del newroutei.route[bestlocationa:bestlocationa + 2]
            del newroutej.route[bestlocationb]
            newroutei.route.insert(bestlocationa, route[bestroutej].route[bestlocationb])
            for i in range(bestlocationa, bestlocationa + 2):
                newroutej.route.insert(bestlocationb + i - bestlocationa, route[bestroutei].route[i])
            self.computercost(newroutei)
            self.computercost(newroutej)
            route[bestroutei] = newroutei
            route[bestroutej] = newroutej
        else:
            if bestgain != 0:
                if random_choice_best:
                    choice = np.random.randint(0, len(gainlist))
                    listchoice = gainlist[choice]
                    bestgain, bestlocationa, bestlocationb, bestroutei, bestroutej = listchoice[0], listchoice[1], \
                                                                                     listchoice[2], listchoice[3], \
                                                                                     listchoice[4]
                    # print("bestgain", bestgain)
                    newroutei = copy.deepcopy(route[bestroutei])
                    newroutej = copy.deepcopy(route[bestroutej])
                    del newroutei.route[bestlocationa:bestlocationa + 2]
                    del newroutej.route[bestlocationb]
                    newroutei.route.insert(bestlocationa, route[bestroutej].route[bestlocationb])
                    for i in range(bestlocationa, bestlocationa + 2):
                        newroutej.route.insert(bestlocationb + i - bestlocationa, route[bestroutei].route[i])
                    self.computercost(newroutei)
                    self.computercost(newroutej)
                    route[bestroutei] = newroutei
                    route[bestroutej] = newroutej
                else:
                    # print("bestgain", bestgain)
                    newroutei = copy.deepcopy(route[bestroutei])
                    newroutej = copy.deepcopy(route[bestroutej])
                    del newroutei.route[bestlocationa:bestlocationa + 2]
                    del newroutej.route[bestlocationb]
                    newroutei.route.insert(bestlocationa, route[bestroutej].route[bestlocationb])
                    for i in range(bestlocationa, bestlocationa + 2):
                        newroutej.route.insert(bestlocationb + i - bestlocationa, route[bestroutei].route[i])
                    self.computercost(newroutei)
                    self.computercost(newroutej)
                    route[bestroutei] = newroutei
                    route[bestroutej] = newroutej
        return route

    def computergain(self, subtouri, subtourj, a, b, c):  # 把弧ab 插入c中
        newroutei = copy.deepcopy(subtouri)
        newroutej = copy.deepcopy(subtourj)
        del newroutei.route[a:b + 1]
        del newroutej.route[c]
        newroutei.route.insert(a, subtourj.route[c])
        for i in range(a, b + 1):
            newroutej.route.insert(c + i - a, subtouri.route[i])
        self.computercost(newroutei)
        self.computercost(newroutej)
        gain = subtouri.cost + subtourj.cost - newroutej.cost - newroutei.cost
        return gain

    def computercost(self, tour):
        tour.reset()
        lastnode = tour.route[0]
        lastnodeindex = int(lastnode.replace("d", ""))
        depotid = lastnodeindex
        for i in range(1, len(tour.route) - 1):
            name = tour.route[i]
            nodeindex = int(name.replace("c", "")) + self.instance["number_of_depots"] - 1
            tour.nowtime = tour.nowtime + self.distance_matrix[lastnodeindex][nodeindex]
            tour.cost = tour.cost + tour.nowtime
            customer = "customer_{}".format(name.replace("c", ""))
            if self.instance[customer]["demand"] + tour.load > self.instance["depots"][depotid][
                "maximum_load_of_a_vehicle"]:
                tour.cost = 99999999
                return 99999999
            tour.load = tour.load + self.instance[customer]["demand"]
            lastnodeindex = nodeindex
        return tour.cost


class OrOptmove_operator():
    def __init__(self, instance, arclenset=3):
        self.instance = instance
        self.distance_matrix = instance["distance_matrix"]
        self.arclenset = arclenset
        return

    def operate(self, route, random_choice_best=False, random_choice=False):
        arclenset = self.arclenset
        route = copy.deepcopy(route)
        bestgain = 0
        bestlocationa = -1
        bestlocationb = -1
        bestroutei = -1
        bestroutej = -1
        arclen = arclenset
        gainlist = []
        if random_choice:
            sign = True
            maxtry = 100
            iter = 0
            while sign:
                bestroutei, bestroutej = np.random.choice(len(route), 2, replace=False).tolist()
                subtouri = route[bestroutei]
                subtourj = route[bestroutej]
                while len(subtouri.route) <= 2 + arclenset:
                    bestroutei, bestroutej = np.random.choice(len(route), 2, replace=False).tolist()
                    subtouri = route[bestroutei]
                    subtourj = route[bestroutej]
                bestlocationa = np.random.randint(low=1, high=len(subtouri.route) - arclen - 1)
                bestlocationb = np.random.randint(low=1, high=len(subtourj.route) - 1)
                gain = self.computergain(subtouri, subtourj, bestlocationa, bestlocationa + 1, bestlocationb)
                # print(len(subtouri.route), len(subtourj.route), bestroutei, bestroutej,gain)
                iter = iter + 1
                if iter > maxtry:
                    return route
                if abs(gain) < 100:
                    sign = False
        else:
            for i in range(len(route)):
                subtouri = route[i]
                if len(subtouri.route) < arclen + 2:
                    continue
                # 路径内
                if len(subtouri.route) >= arclen + 3:
                    subtourj = route[i]
                    for a in range(1, len(subtouri.route) - arclen - 1):
                        for b in range(a + arclen, len(subtourj.route) - 1):
                            ci, cj = a, a + arclen - 1
                            cs, cr = b, b + 1
                            gain = self.computergainintra(subtouri, subtourj, ci, cj, cs)
                            if gain > 0:
                                tmpgain = gain
                                tmplocationa = a
                                tmplocationb = b
                                tmproutei = i
                                tmproutej = i
                                gainthis = [tmpgain, tmplocationa, tmplocationb, tmproutei, tmproutej]
                                gainlist.append(gainthis)
                            if gain > bestgain:
                                bestgain = gain
                                bestlocationa = a
                                bestlocationb = b
                                bestroutei = i
                                bestroutej = i

                # 路径间
                for j in range(len(route)):  # 两条路径不一样
                    if i == j: continue
                    subtourj = route[j]
                    if len(subtourj.route) == 2:
                        continue
                    for a in range(1, len(subtouri.route) - arclen - 1, 1):
                        for b in range(1, len(subtourj.route) - 1):
                            ci, cj = a, a + arclen - 1
                            cs, cr = b, b + 1
                            gain = self.computergain(subtouri, subtourj, ci, cj, cs)
                            # print(gain)
                            if gain > 0:
                                tmpgain = gain
                                tmplocationa = a
                                tmplocationb = b
                                tmproutei = i
                                tmproutej = j
                                gainthis = [tmpgain, tmplocationa, tmplocationb, tmproutei, tmproutej]
                                gainlist.append(gainthis)
                            if gain > bestgain:
                                bestgain = gain
                                bestlocationa = a
                                bestlocationb = b
                                bestroutei = i
                                bestroutej = j
        if random_choice:
            newroutei = copy.deepcopy(route[bestroutei])
            newroutej = copy.deepcopy(route[bestroutej])
            del newroutei.route[bestlocationa:bestlocationa + arclen - 1]
            for i in range(bestlocationa, bestlocationa + arclen - 1):
                newroutej.route.insert(bestlocationb + i - bestlocationa, route[bestroutei].route[i])
            self.computercost(newroutei)
            self.computercost(newroutej)
            route[bestroutei] = newroutei
            route[bestroutej] = newroutej
        else:

            if bestgain != 0:
                if random_choice_best:
                    choice = np.random.randint(0, len(gainlist))
                    listchoice = gainlist[choice]
                    bestgain, bestlocationa, bestlocationb, bestroutei, bestroutej = listchoice[0], listchoice[1], \
                                                                                     listchoice[2], listchoice[3], \
                                                                                     listchoice[4]
                    # print("bestgain", bestgain)
                    if bestroutei != bestroutej:
                        newroutei = copy.deepcopy(route[bestroutei])
                        newroutej = copy.deepcopy(route[bestroutej])
                        del newroutei.route[bestlocationa:bestlocationa + arclen - 1]
                        for i in range(bestlocationa, bestlocationa + arclen - 1):
                            newroutej.route.insert(bestlocationb + i - bestlocationa, route[bestroutei].route[i])
                        self.computercost(newroutei)
                        self.computercost(newroutej)
                        route[bestroutei] = newroutei
                        route[bestroutej] = newroutej
                    else:
                        newroutei = copy.deepcopy(route[bestroutei])
                        del newroutei.route[bestlocationa:bestlocationa + arclen - 1]
                        for i in range(bestlocationa, bestlocationa + arclen - 1):
                            newroutei.route.insert(bestlocationb + i - bestlocationa - arclen,
                                                   route[bestroutei].route[i])
                        self.computercost(newroutei)
                        route[bestroutei] = newroutei
                else:
                    # print("bestgain", bestgain)
                    if bestroutei != bestroutej:
                        newroutei = copy.deepcopy(route[bestroutei])
                        newroutej = copy.deepcopy(route[bestroutej])
                        del newroutei.route[bestlocationa:bestlocationa + arclen - 1]
                        for i in range(bestlocationa, bestlocationa + arclen - 1):
                            newroutej.route.insert(bestlocationb + i - bestlocationa, route[bestroutei].route[i])
                        self.computercost(newroutei)
                        self.computercost(newroutej)
                        route[bestroutei] = newroutei
                        route[bestroutej] = newroutej
                    else:
                        newroutei = copy.deepcopy(route[bestroutei])
                        del newroutei.route[bestlocationa:bestlocationa + arclen - 1]
                        for i in range(bestlocationa, bestlocationa + arclen - 1):
                            newroutei.route.insert(bestlocationb + i - bestlocationa - arclen,
                                                   route[bestroutei].route[i])
                        self.computercost(newroutei)
                        route[bestroutei] = newroutei

        return route

    def computergain(self, subtouri, subtourj, a, b, c):  # 把弧ab 插入c中
        newroutei = copy.deepcopy(subtouri)
        newroutej = copy.deepcopy(subtourj)
        del newroutei.route[a:b + 1]
        # newroutei.route.insert(a, subtourj.route[c])
        for i in range(a, b + 1):
            newroutej.route.insert(c + i - a + 1, subtouri.route[i])
        self.computercost(newroutei)
        self.computercost(newroutej)
        gain = subtouri.cost + subtourj.cost - newroutej.cost - newroutei.cost
        return gain

    def computergainintra(self, subtouri, subtourj, a, b, c):  # 把弧ab 插入c中
        newroutei = copy.deepcopy(subtouri)
        del newroutei.route[a:b + 1]
        arclen = b - a
        for i in range(a, b + 1):
            newroutei.route.insert(c + i - a - arclen, subtouri.route[i])
        self.computercost(newroutei)
        gain = subtouri.cost - newroutei.cost
        return gain

    def computercost(self, tour):
        tour.reset()
        lastnode = tour.route[0]
        lastnodeindex = int(lastnode.replace("d", ""))
        depotid = lastnodeindex
        for i in range(1, len(tour.route) - 1):
            name = tour.route[i]
            nodeindex = int(name.replace("c", "")) + self.instance["number_of_depots"] - 1
            tour.nowtime = tour.nowtime + self.distance_matrix[lastnodeindex][nodeindex]
            tour.cost = tour.cost + tour.nowtime
            customer = "customer_{}".format(name.replace("c", ""))
            if self.instance[customer]["demand"] + tour.load > self.instance["depots"][depotid][
                "maximum_load_of_a_vehicle"]:
                tour.cost = 99999999
                return 99999999
            tour.load = tour.load + self.instance[customer]["demand"]
            lastnodeindex = nodeindex
        return tour.cost


class CrossExchangemove_operator():
    def __init__(self, instance, arclenset=2):
        self.instance = instance
        self.distance_matrix = instance["distance_matrix"]
        self.arclenset = arclenset
        return

    def operate(self, route, random_choice_best=False, random_choice=False):
        arclenset = self.arclenset
        route = copy.deepcopy(route)
        bestgain = 0
        bestlocationa = -1
        bestlocationb = -1
        bestroutei = -1
        bestroutej = -1
        arclen = arclenset
        gainlist = []
        for i in range(len(route)):
            subtouri = route[i]
            if len(subtouri.route) < arclen + 2:
                continue
            # 路径间
            for j in range(i + 1, len(route)):  # 两条路径不一样
                subtourj = route[j]
                if len(subtourj.route) < arclen + 2:
                    continue
                for a in range(1, len(subtouri.route) - arclen - 1):
                    for b in range(1, len(subtourj.route) - arclen - 1):
                        ci, cj = a, a + arclen - 1
                        cs, cr = b, b + arclen - 1
                        gain = self.computergain(subtouri, subtourj, ci, cj, cs, cr)
                        # print(gain)
                        if gain > 0:
                            tmpgain = gain
                            tmplocationa = a
                            tmplocationb = b
                            tmproutei = i
                            tmproutej = j
                            gainthis = [tmpgain, tmplocationa, tmplocationb, tmproutei, tmproutej]
                            gainlist.append(gainthis)
                        if gain > bestgain:
                            bestgain = gain
                            bestlocationa = a
                            bestlocationb = b
                            bestroutei = i
                            bestroutej = j
        if bestgain != 0:
            if random_choice_best:
                choice = np.random.randint(0, len(gainlist))
                listchoice = gainlist[choice]
                bestgain, bestlocationa, bestlocationb, bestroutei, bestroutej = listchoice[0], listchoice[1], \
                                                                                 listchoice[2], listchoice[3], \
                                                                                 listchoice[4]
                # print("bestgain", bestgain)
                newroutei = copy.deepcopy(route[bestroutei])
                newroutej = copy.deepcopy(route[bestroutej])
                del newroutei.route[bestlocationa:bestlocationa + arclen]
                del newroutej.route[bestlocationb:bestlocationb + arclen]
                for i in range(bestlocationa, bestlocationa + arclen):
                    newroutej.route.insert(bestlocationb + i - bestlocationa, route[bestroutei].route[i])
                for i in range(bestlocationb, bestlocationb + arclen):
                    newroutei.route.insert(bestlocationa + i - bestlocationb, route[bestroutej].route[i])
                self.computercost(newroutei)
                self.computercost(newroutej)
                route[bestroutei] = newroutei
                route[bestroutej] = newroutej
            else:
                # print("bestgain", bestgain)
                newroutei = copy.deepcopy(route[bestroutei])
                newroutej = copy.deepcopy(route[bestroutej])
                del newroutei.route[bestlocationa:bestlocationa + arclen]
                del newroutej.route[bestlocationb:bestlocationb + arclen]
                for i in range(bestlocationa, bestlocationa + arclen):
                    newroutej.route.insert(bestlocationb + i - bestlocationa, route[bestroutei].route[i])
                for i in range(bestlocationb, bestlocationb + arclen):
                    newroutei.route.insert(bestlocationa + i - bestlocationb, route[bestroutej].route[i])
                self.computercost(newroutei)
                self.computercost(newroutej)
                route[bestroutei] = newroutei
                route[bestroutej] = newroutej

        return route

    def computergain(self, subtouri, subtourj, a, b, c, d):  # 把弧ab 插入c中
        newroutei = copy.deepcopy(subtouri)
        newroutej = copy.deepcopy(subtourj)
        del newroutei.route[a:b + 1]
        del newroutej.route[c:d + 1]
        for i in range(a, b + 1):
            newroutej.route.insert(c + i - a, subtouri.route[i])
        for i in range(c, d + 1):
            newroutei.route.insert(a + i - c, subtourj.route[i])
        self.computercost(newroutei)
        self.computercost(newroutej)
        gain = subtouri.cost + subtourj.cost - newroutej.cost - newroutei.cost
        return gain

    def computercost(self, tour):
        tour.reset()
        lastnode = tour.route[0]
        lastnodeindex = int(lastnode.replace("d", ""))
        depotid = lastnodeindex
        for i in range(1, len(tour.route) - 1):
            name = tour.route[i]
            nodeindex = int(name.replace("c", "")) + self.instance["number_of_depots"] - 1
            tour.nowtime = tour.nowtime + self.distance_matrix[lastnodeindex][nodeindex]
            tour.cost = tour.cost + tour.nowtime
            customer = "customer_{}".format(name.replace("c", ""))
            if self.instance[customer]["demand"] + tour.load > self.instance["depots"][depotid][
                "maximum_load_of_a_vehicle"]:
                tour.cost = 99999999
                return 99999999
            tour.load = tour.load + self.instance[customer]["demand"]
            lastnodeindex = nodeindex
        return tour.cost


class ArbitryCrossExchangemove_operator():
    def __init__(self, instance, fastmode=False):
        self.instance = instance
        self.distance_matrix = instance["distance_matrix"]
        self.fastmode = fastmode
        return

    def operate(self, route, random_choice_best=False, random_choice=False):
        route = copy.deepcopy(route)
        bestgain = 0
        bestlocationa = -1
        bestlocationb = -1
        bestroutei = -1
        bestroutej = -1
        bestlena = -1
        bestlenb = -1
        gainlist = []
        if random_choice:
            sign = True
            maxtry = 100
            iter = 0
            while sign:
                bestroutei, bestroutej = np.random.choice(len(route), 2, replace=False).tolist()
                subtouri = route[bestroutei]
                subtourj = route[bestroutej]
                while len(subtouri.route) < 4 or len(subtourj.route) < 4:
                    bestroutei, bestroutej = np.random.choice(len(route), 2, replace=False).tolist()
                    subtouri = route[bestroutei]
                    subtourj = route[bestroutej]
                arclena = np.random.randint(low=2, high=len(subtouri.route) - 1)
                arclenb = np.random.randint(low=2, high=len(subtourj.route) - 1)
                a = np.random.randint(low=1, high=len(subtouri.route) - arclena)
                b = np.random.randint(low=1, high=len(subtourj.route) - arclenb)
                ci, cj = a, a + arclena - 1
                cs, cr = b, b + arclenb - 1
                gain = self.computergain(subtouri, subtourj, ci, cj, cs, cr)
                bestlocationa = a
                bestlocationb = b
                bestlena = arclena
                bestlenb = arclenb
                iter = iter + 1
                if iter > maxtry:
                    return route
                # print(len(subtouri.route), len(subtourj.route), bestroutei, bestroutej,gain)
                if abs(gain) < 100:
                    sign = False

        else:
            for i in range(len(route)):
                subtouri = route[i]
                if len(subtouri.route) < 4:
                    continue
                allarclena = [i for i in range(2, len(subtouri.route) - 1)]
                for arclena in allarclena:
                    for j in range(i + 1, len(route)):  # 两条路径不一样
                        subtourj = route[j]
                        if len(subtourj.route) < 4:
                            continue
                        allarclenb = [i for i in range(2, len(subtourj.route) - 1)]
                        for arclenb in allarclenb:
                            for a in range(1, len(subtouri.route) - arclena):
                                for b in range(1, len(subtourj.route) - arclenb):
                                    ci, cj = a, a + arclena - 1
                                    cs, cr = b, b + arclenb - 1
                                    gain = self.computergain(subtouri, subtourj, ci, cj, cs, cr)
                                    # print(gain)
                                    if gain > 0:
                                        if self.fastmode:
                                            bestlocationa = a
                                            bestlocationb = b
                                            bestroutei = i
                                            bestroutej = j
                                            bestlena = arclena
                                            bestlenb = arclenb
                                            newroutei = copy.deepcopy(route[bestroutei])
                                            newroutej = copy.deepcopy(route[bestroutej])
                                            del newroutei.route[bestlocationa:bestlocationa + bestlena]
                                            del newroutej.route[bestlocationb:bestlocationb + bestlenb]
                                            for i in range(bestlocationa, bestlocationa + bestlena):
                                                newroutej.route.insert(bestlocationb + i - bestlocationa,
                                                                       route[bestroutei].route[i])
                                            for i in range(bestlocationb, bestlocationb + bestlenb):
                                                newroutei.route.insert(bestlocationa + i - bestlocationb,
                                                                       route[bestroutej].route[i])
                                            self.computercost(newroutei)
                                            self.computercost(newroutej)
                                            route[bestroutei] = newroutei
                                            route[bestroutej] = newroutej
                                            return route
                                        tmpgain = gain
                                        tmplocationa = a
                                        tmplocationb = b
                                        tmproutei = i
                                        tmproutej = j
                                        tmplena = arclena
                                        tmplenb = arclenb
                                        gainthis = [tmpgain, tmplocationa, tmplocationb, tmproutei, tmproutej, tmplena,
                                                    tmplenb]
                                        gainlist.append(gainthis)
                                    if gain > bestgain:
                                        bestgain = gain
                                        bestlocationa = a
                                        bestlocationb = b
                                        bestroutei = i
                                        bestroutej = j
                                        bestlena = arclena
                                        bestlenb = arclenb
        if random_choice:
            newroutei = copy.deepcopy(route[bestroutei])
            newroutej = copy.deepcopy(route[bestroutej])
            del newroutei.route[bestlocationa:bestlocationa + bestlena]
            del newroutej.route[bestlocationb:bestlocationb + bestlenb]
            for i in range(bestlocationa, bestlocationa + bestlena):
                newroutej.route.insert(bestlocationb + i - bestlocationa, route[bestroutei].route[i])
            for i in range(bestlocationb, bestlocationb + bestlenb):
                newroutei.route.insert(bestlocationa + i - bestlocationb, route[bestroutej].route[i])
            self.computercost(newroutei)
            self.computercost(newroutej)
            route[bestroutei] = newroutei
            route[bestroutej] = newroutej
        else:
            if bestgain != 0:
                if random_choice_best:
                    choice = np.random.randint(0, len(gainlist))
                    listchoice = gainlist[choice]
                    bestgain, bestlocationa, bestlocationb, bestroutei, bestroutej, bestlena, bestlenb = listchoice[0], \
                                                                                                         listchoice[1], \
                                                                                                         listchoice[2], \
                                                                                                         listchoice[3], \
                                                                                                         listchoice[4], \
                                                                                                         listchoice[5], \
                                                                                                         listchoice[6]
                    # print("bestgain", bestgain)
                    newroutei = copy.deepcopy(route[bestroutei])
                    newroutej = copy.deepcopy(route[bestroutej])
                    del newroutei.route[bestlocationa:bestlocationa + bestlena]
                    del newroutej.route[bestlocationb:bestlocationb + bestlenb]
                    for i in range(bestlocationa, bestlocationa + bestlena):
                        newroutej.route.insert(bestlocationb + i - bestlocationa, route[bestroutei].route[i])
                    for i in range(bestlocationb, bestlocationb + bestlenb):
                        newroutei.route.insert(bestlocationa + i - bestlocationb, route[bestroutej].route[i])
                    self.computercost(newroutei)
                    self.computercost(newroutej)
                    route[bestroutei] = newroutei
                    route[bestroutej] = newroutej
                else:
                    # print("bestgain", bestgain)
                    newroutei = copy.deepcopy(route[bestroutei])
                    newroutej = copy.deepcopy(route[bestroutej])
                    del newroutei.route[bestlocationa:bestlocationa + bestlena]
                    del newroutej.route[bestlocationb:bestlocationb + bestlenb]
                    for i in range(bestlocationa, bestlocationa + bestlena):
                        newroutej.route.insert(bestlocationb + i - bestlocationa, route[bestroutei].route[i])
                    for i in range(bestlocationb, bestlocationb + bestlenb):
                        newroutei.route.insert(bestlocationa + i - bestlocationb, route[bestroutej].route[i])
                    self.computercost(newroutei)
                    self.computercost(newroutej)
                    route[bestroutei] = newroutei
                    route[bestroutej] = newroutej

        return route

    def computergain(self, subtouri, subtourj, a, b, c, d):  # 把弧ab 插入c中
        newroutei = copy.deepcopy(subtouri)
        newroutej = copy.deepcopy(subtourj)
        del newroutei.route[a:b + 1]
        del newroutej.route[c:d + 1]
        for i in range(a, b + 1):
            newroutej.route.insert(c + i - a, subtouri.route[i])
        for i in range(c, d + 1):
            newroutei.route.insert(a + i - c, subtourj.route[i])
        self.computercost(newroutei)
        self.computercost(newroutej)
        gain = subtouri.cost + subtourj.cost - newroutej.cost - newroutei.cost
        return gain

    def computercost(self, tour):
        tour.reset()
        lastnode = tour.route[0]
        lastnodeindex = int(lastnode.replace("d", ""))
        depotid = lastnodeindex
        for i in range(1, len(tour.route) - 1):
            name = tour.route[i]
            nodeindex = int(name.replace("c", "")) + self.instance["number_of_depots"] - 1
            tour.nowtime = tour.nowtime + self.distance_matrix[lastnodeindex][nodeindex]
            tour.cost = tour.cost + tour.nowtime
            customer = "customer_{}".format(name.replace("c", ""))
            if self.instance[customer]["demand"] + tour.load > self.instance["depots"][depotid][
                "maximum_load_of_a_vehicle"]:
                tour.cost = 99999999
                return 99999999
            tour.load = tour.load + self.instance[customer]["demand"]
            lastnodeindex = nodeindex
        return tour.cost


class random_perturbation():
    def __init__(self, instance):
        self.instance = instance
        self.distance_matrix = instance["distance_matrix"]
        self.R = instance["number_of_vehicles"] * instance["number_of_depots"]
        self.twoExchangemove_operators = twoExchangemove_operator(instance=self.instance)
        self.twoOptmove_operators = twoOptmove_operator(instance=self.instance)
        return

    def operate(self, route, random_choice=False, random_choice_best=False):
        # H = np.random.randint(2, min(self.R, 10))
        H = 2
        for i in range(H):
            r = np.random.rand()
            if r <= 0.5:
                route = self.twoExchangemove_operators.operate(route=route, random_choice_best=random_choice_best,
                                                               random_choice=random_choice)
            else:
                route = self.twoOptmove_operators.operate(route=route, random_choice_best=random_choice_best,
                                                          random_choice=random_choice)
        return route


class removeinsert_perturbation():
    def __init__(self, instance):
        self.instance = instance
        self.distance_matrix = instance["distance_matrix"]
        self.r = min(20, instance["number_of_customers"] // 10)

    def operate(self, route, random_choice=False, random_choice_best=False):
        flist = {}
        for index in range(len(route)):
            subroute = route[index]
            if len(subroute.route) == 2:
                continue
            for c in range(1, len(subroute.route) - 1):
                tmproute = copy.deepcopy(subroute)
                name = subroute.route[c]
                customer = "customer_{}".format(name.replace("c", ""))
                demand = self.instance[customer]["demand"]
                del tmproute.route[c]
                self.computercost(tmproute)
                difference = subroute.cost - tmproute.cost
                f = demand / difference
                flist[name] = f
        sortedflist = sorted(flist.items(), key=lambda x: x[1])
        selectflist = sortedflist[:self.r]
        for i in range(len(selectflist)):
            name = selectflist[i][0]
            route = self.least_cost_insertion(name, route)
            # print(self.computercostall(route))

        return route

    def least_cost_insertion(self, name, route):  # 寻找最好位置插入

        index, subindex = self.findindex(name, route)
        newroute = copy.deepcopy(route)
        newsubroute = newroute[index]
        del newsubroute.route[subindex]
        self.computercost(newsubroute)
        newroute[index] = newsubroute
        leastcostgain = 99999999
        bestindex = index
        bestsubindex = subindex
        # 寻找最优插入点
        for i in range(len(newroute)):
            subroute = newroute[i]
            costnow = self.computercost(subroute)
            for j in range(1, len(subroute.route)):
                newsubroute = copy.deepcopy(subroute)
                newsubroute.route.insert(j, name)
                newcost = self.computercost(newsubroute)
                gain = newcost - costnow
                if gain < leastcostgain:
                    bestindex = i
                    bestsubindex = j
                    leastcostgain = gain

        subroute = newroute[bestindex]
        subroute.route.insert(bestsubindex, name)
        self.computercost(subroute)
        newroute[bestindex] = subroute
        # costbefore=self.computercostall(route)
        # costbnow=self.computercostall(newroute)
        return newroute

    def findindex(self, name, route):
        for i in range(len(route)):
            subroute = route[i]
            for j in range(len(subroute.route)):
                if subroute.route[j] == name:
                    return i, j

    def computercostall(self, route):
        allcost = 0
        for tour in route:
            tour.reset()
            lastnode = tour.route[0]
            lastnodeindex = int(lastnode.replace("d", ""))
            depotid = lastnodeindex
            for i in range(1, len(tour.route) - 1):
                name = tour.route[i]
                nodeindex = int(name.replace("c", "")) + self.instance["number_of_depots"] - 1
                tour.nowtime = tour.nowtime + self.distance_matrix[lastnodeindex][nodeindex]
                tour.cost = tour.cost + tour.nowtime
                customer = "customer_{}".format(name.replace("c", ""))
                if self.instance[customer]["demand"] + tour.load > self.instance["depots"][depotid][
                    "maximum_load_of_a_vehicle"]:
                    tour.cost = 99999999
                    allcost = allcost + tour.cost
                    break
                tour.load = tour.load + self.instance[customer]["demand"]
                lastnodeindex = nodeindex
            allcost = allcost + tour.cost
        return allcost

    def computercost(self, tour):
        tour.reset()
        lastnode = tour.route[0]
        lastnodeindex = int(lastnode.replace("d", ""))
        depotid = lastnodeindex
        for i in range(1, len(tour.route) - 1):
            name = tour.route[i]
            nodeindex = int(name.replace("c", "")) + self.instance["number_of_depots"] - 1
            tour.nowtime = tour.nowtime + self.distance_matrix[lastnodeindex][nodeindex]
            tour.cost = tour.cost + tour.nowtime
            customer = "customer_{}".format(name.replace("c", ""))
            if self.instance[customer]["demand"] + tour.load > self.instance["depots"][depotid][
                "maximum_load_of_a_vehicle"]:
                tour.cost = 99999999
                return 99999999
            tour.load = tour.load + self.instance[customer]["demand"]
            lastnodeindex = nodeindex
        return tour.cost


if __name__ == '__main__':
    testrange = 1
    random_choice_best = True
    printroute = True
    instance = load_instance()
    route = initialization(instance)
    random_choice = True
    cost = calculate_cost(route, printroute=printroute)
    print("original cost", cost)

    # operator = twoExchangemove_operator(instance=instance)
    # for i in range(testrange):
    #     route = operator.operate(route, random_choice_best=random_choice_best, random_choice=random_choice)
    # cost = calculate_cost(route, printroute=printroute)
    # print("twoExchangemove_operator cost", cost)

    # operator = Relocationmove_operator(instance=instance)
    # for i in range(testrange):
    #     route = operator.operate(route, random_choice_best=random_choice_best, random_choice=random_choice)
    # cost = calculate_cost(route, printroute=printroute)
    # print("Relocationmove_operator cost", cost)
    #
    # operator = twoOptmove_operator(instance=instance)
    # for i in range(testrange):
    #     route = operator.operate(route, random_choice_best=random_choice_best, random_choice=random_choice)
    # cost = calculate_cost(route, printroute=printroute)
    # print("twoOptmove_operator cost", cost)

    # operator = ArcNodeExchangemove_operator(instance=instance)
    # for i in range(testrange):
    #     route = operator.operate(route, random_choice_best=random_choice_best, random_choice=random_choice)
    # cost = calculate_cost(route, printroute=printroute)
    # print("ArcNodeExchangemove_operator cost", cost)

    # operator = OrOptmove_operator(instance=instance)
    # for i in range(testrange):
    #     route = operator.operate(route, random_choice_best=random_choice_best, random_choice=random_choice)
    # cost = calculate_cost(route, printroute=printroute)
    # print("OrOptmove_operator cost", cost)
    #
    # operator = CrossExchangemove_operator(instance=instance)
    # for i in range(testrange):
    #     route = operator.operate(route, random_choice_best=random_choice_best, random_choice=random_choice)
    # cost = calculate_cost(route, printroute=printroute)
    # print("CrossExchangemove_operator cost", cost)
    #
    perturbation = random_perturbation(instance=instance)
    route = perturbation.operate(route=route, random_choice=random_choice)
    cost = calculate_cost(route, printroute=printroute)
    print("random_perturbation cost", cost)
    #
    # perturbation = removeinsert_perturbation(instance=instance)
    # route = perturbation.operate(route=route, random_choice=random_choice)
    # cost = calculate_cost(route, printroute=printroute)
    # print("removeinsert_perturbation cost", cost)

    # operator = ArbitryCrossExchangemove_operator(instance=instance)
    # for i in range(testrange):
    #     route = operator.operate(route, random_choice_best=random_choice_best, random_choice=random_choice)
    # cost = calculate_cost(route, printroute=printroute)
    # print("ArbitryCrossExchangemove_operator cost", cost)

    # print(improve(route, newroute=newroute))
    # tour = subtour()
    # tour.route = ['d1', 'c12', 'c47', 'c13', 'd1']
    # tmp = twoOptmove_operator(instance)
    # tmp.computercost(tour)
    # print()
