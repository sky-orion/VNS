import numpy as np
import os


def load_instance(name="p01"):
    filename = os.path.join("./C-mdvrp", name)
    f = open(filename, 'r')
    data = {}
    linenumber = 0
    lines = f.readlines()
    for line in lines:
        tmpline = [int(i) for i in line.strip().split()]
        if linenumber == 0:
            data["number_of_vehicles"] = tmpline[1]
            data["number_of_customers"] = tmpline[2]
            data["number_of_depots"] = tmpline[3]
            data["depots"] = []
        if linenumber > 0 and linenumber <= data["number_of_depots"]:
            depots = {}
            depots["maximum_duration_of_a_route"] = tmpline[0]
            depots["maximum_load_of_a_vehicle"] = tmpline[1]
            data["depots"].append(depots)
        if linenumber > data["number_of_depots"] and linenumber <= data["number_of_depots"] + data[
            "number_of_customers"]:
            name = "customer_{}".format(tmpline[0])
            customer = {}
            customer["id"] = tmpline[0]
            customer["x_coordinate"] = tmpline[1]
            customer["y_coordinate"] = tmpline[2]
            customer["demand"] = tmpline[4]
            data[name] = customer
        if linenumber > data["number_of_depots"] + data["number_of_customers"]:
            name = "depot_{}".format(linenumber - data["number_of_depots"] - data["number_of_customers"])
            depot = {}
            depot["id"] = linenumber - data["number_of_depots"] - data["number_of_customers"]
            depot["x_coordinate"] = tmpline[1]
            depot["y_coordinate"] = tmpline[2]
            data[name] = depot
        linenumber = linenumber + 1
    cust = []
    for i in range(1, data["number_of_depots"] + 1):
        name = "depot_{}".format(i)
        cust.append(data[name])
    for i in range(1, data["number_of_customers"] + 1):
        name = "customer_{}".format(i)
        cust.append(data[name])
    distance_matrix = [[calculate_distance(customer1, customer2) for customer1 in cust] for customer2 in
                       cust]
    data["distance_matrix"] = np.array(distance_matrix)
    return data


def calculate_distance(customer1, customer2):
    return ((customer1['x_coordinate'] - customer2['x_coordinate']) ** 2 + (
            customer1['y_coordinate'] - customer2['y_coordinate']) ** 2) ** 0.5


def calculate_cost(route, printroute=False):
    cost = 0
    for subroute in route:
        cost = cost + subroute.cost
        if printroute:
            print("route {}: cost {:.2f}|load {:.2f}".format(subroute.route, subroute.cost,
                                                             subroute.load
                                                             ))

    return cost


def improve(route, newroute):
    cost1 = round(calculate_cost(route), 5)
    cost2 = round(calculate_cost(newroute), 5)
    return cost2 < cost1


if __name__ == '__main__':
    data = load_instance()
    fruits = ['d1', 'd2', 'd3', 'd4', 'd5']
    indexs = [0, 1]
    a, b = np.random.choice(50, 2, replace=False).tolist()
    print(a, b)
    del fruits[0]
    # fruits.insert(4, "d6")
    # fruits = list(reversed(fruits[1:4]))
    # tmp=[]
    print(fruits)
    # choice = np.random.randint(0, len(fruits))
    # print(choice)
    print(min(10, 15))
    tour = ['d0', 'c47', 'c12', 'c18', 'c4', 'c14', 'c19', 'c17', 'c41', 'c37', 'c44', 'c13', 'c42', 'c40', 'c48',
            'c23', 'c24', 'c33', 'c45', 'c8', 'c28', 'c21', 'c50', 'c43', 'd0']
