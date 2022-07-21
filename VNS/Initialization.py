import numpy as np

from utils import load_instance,calculate_cost


class subtour():
    def __init__(self, depot=0):
        self.depot = depot
        self.route = ["d{}".format(depot), "d{}".format(depot)]
        self.cost = 0
        self.nowtime = 0  # 现在行车时间
        self.load = 0

    def reset(self):
        self.cost = 0
        self.nowtime = 0  # 现在行车时间
        self.load = 0

    def insertcusotmer(self, customer, instance):
        id = customer["id"]
        name = "c{}".format(id)
        distance_matrix = instance["distance_matrix"]
        customerindex = id + instance["number_of_depots"] - 1
        lastnode = self.route[-2]
        demand = customer["demand"]
        if "d" in lastnode:
            lastnodeindex = int(lastnode.replace("d", ""))
        else:
            lastnodeindex = int(lastnode.replace("c", "")) + instance["number_of_depots"] - 1
        self.nowtime = self.nowtime + distance_matrix[lastnodeindex][customerindex]
        self.cost = self.cost + self.nowtime
        self.load = self.load + demand
        self.route.insert(-1, name)


def initialization(instance, specr=None):
    NV = instance["number_of_vehicles"]
    ND = instance["number_of_depots"]
    NC = instance["number_of_customers"]
    g = NV * ND
    r = NV * ND  # \
    if specr is not None:
        r = specr
    t = min(g, r)  # 允许的车辆数目
    selectlist = selectroute(instance, t)

    # 每个节点各有number_of_vehicles个车
    route = []
    for i in range(ND):
        for j in range(NV):
            subroute = subtour(depot=i)
            route.append(subroute)
    AT = 0
    RC = []
    for i in range(1, NC + 1):
        name = "customer_{}".format(i)
        RC.append(instance[name])
    while len(RC) != 0:
        RV = []
        for customer in RC:
            RV.append(ComputeRegretValue(customer, selectlist, instance, route))
        rv_array = np.array(RV)
        rvindex = rv_array.argmax()
        customeru = RC[rvindex]
        icindex = Computeinsertioncostall(customeru, route, instance, selectlist)[0][0]
        e = route[icindex]
        if len(e.route) != 2:
            AT = AT + 1
        RC.pop(rvindex)
        e.insertcusotmer(customeru, instance)
    newroute = []
    # 去除虚拟路径
    for i in range(len(route)):
        subroute = route[i]
        if len(subroute.route) != 2:
            newroute.append(subroute)
    return newroute


# 整体路径
def Computeinsertioncostall(customer, route, instance, selectlist):
    # 计算插入cost
    insertioncost = {}
    for index in selectlist:
        subroute = route[index]
        insertioncost[index] = Computeinsertioncost(customer, subroute, instance)
    sortedinsertioncost = sorted(insertioncost.items(), key=lambda x: x[1])
    return sortedinsertioncost


# 单条路径
def Computeinsertioncost(customer, subroute, instance):
    nowtime = subroute.nowtime
    route = subroute.route
    lastnode = route[-2]
    id = customer["id"]
    distance_matrix = instance["distance_matrix"]
    customerindex = id + instance["number_of_depots"] - 1
    if "d" in lastnode:
        lastnodeindex = int(lastnode.replace("d", ""))
    else:
        lastnodeindex = int(lastnode.replace("c", "")) + instance["number_of_depots"] - 1
    timeafterlastnode = nowtime + distance_matrix[lastnodeindex][customerindex]
    # 容量约束
    depotid = int(route[0].replace("d", ""))
    if customer["demand"] + subroute.load > instance["depots"][depotid]["maximum_load_of_a_vehicle"]:
        timeafterlastnode = 99999999
    return timeafterlastnode


def selectroute(instance, t):  # 选择合适的出发点
    sign = False
    at = 0
    selectlist = []
    for i in range(instance["number_of_vehicles"]):
        if sign:
            break
        for j in range(instance["number_of_depots"]):
            # print(i + instance["number_of_depots"] * j)
            selectlist.append(i + instance["number_of_vehicles"] * j)
            at = at + 1
            if at >= t:
                sign = True
                break
    return selectlist


def ComputeRegretValue(customer, selectlist, instance, route):
    insertioncost = {}
    for index in selectlist:
        subroute = route[index]
        insertioncost[index] = Computeinsertioncost(customer, subroute, instance)
    sortedinsertioncost = sorted(insertioncost.items(), key=lambda x: x[1])
    RV = sortedinsertioncost[2][1] - sortedinsertioncost[0][1]
    return RV


if __name__ == '__main__':
    instance = load_instance(name="p05")
    route = initialization(instance,specr=None)
    cost=calculate_cost(route=route,printroute=True)
    print("cost", cost)
    print(selectroute(instance, 2))
