from local_search_operator_for_vns import *
from utils import improve, calculate_cost


def VNS(instance, specr=None):
    # specr 指定车辆数目
    s = initialization(instance=instance, specr=specr)
    NK = [Relocationmove_operator(instance=instance),
          twoExchangemove_operator(instance=instance),
          twoOptmove_operator(instance=instance),
          ArcNodeExchangemove_operator(instance=instance),
          OrOptmove_operator(instance=instance),
          ArbitryCrossExchangemove_operator(instance=instance, fastmode=True),
          random_perturbation(instance=instance),
          removeinsert_perturbation(instance=instance)]
    maxiter = 50  # VNS外层循环最大迭代次数
    maxiterVND = 1000  # VND的最大迭代次数
    iter = 0
    kmax = len(NK)
    while iter < maxiter:
        i = 0
        while i < kmax:
            nki = NK[i]
            x_one = nki.operate(s, random_choice=True)
            x_two = VND(s=x_one, instance=instance, maxvnd=maxiterVND)
            print("iteration {}| VND {} | x_one cost {:.2f} | x_two cost {:.2f} |s cost {:.2f} ".format(iter, i,
                                                                                                        calculate_cost(
                                                                                                            x_one),
                                                                                                        calculate_cost(
                                                                                                            x_two),
                                                                                                        calculate_cost(
                                                                                                            s)
                                                                                                        )
                  )
            if improve(s, x_two):
                s = x_two
                i = 0
            else:
                i = i + 1
        print("iteration {}| VNS  s cost {:.2f} ".format(iter,
                                                         calculate_cost(
                                                             s),
                                                         ))
        iter = iter + 1
    return s


def VND(instance, specr=None, s=None, maxvnd=None):
    if s is None:
        s = initialization(instance=instance, specr=specr)
        NK = [Relocationmove_operator(instance=instance),
              twoExchangemove_operator(instance=instance),
              twoOptmove_operator(instance=instance),
              ArcNodeExchangemove_operator(instance=instance),
              OrOptmove_operator(instance=instance),
              ArbitryCrossExchangemove_operator(instance=instance, fastmode=True),
              random_perturbation(instance=instance),
              removeinsert_perturbation(instance=instance)
              ]
    else:
        NK = [Relocationmove_operator(instance=instance),
              twoExchangemove_operator(instance=instance),
              twoOptmove_operator(instance=instance),
              ArcNodeExchangemove_operator(instance=instance),
              OrOptmove_operator(instance=instance),
              ArbitryCrossExchangemove_operator(instance=instance, fastmode=True)
              ]
    i = 0
    kmax = len(NK)
    if maxvnd:
        itervnd = 0
        while i < kmax and itervnd < maxvnd:
            ni = NK[i]
            s_one = ni.operate(s, random_choice_best=False)
            if improve(s, s_one):
                s = s_one
                i = 0
            else:
                i = i + 1
            itervnd = itervnd + 1
            # print("inter VND",itervnd,i)
    else:
        while i < kmax:
            ni = NK[i]
            s_one = ni.operate(s, random_choice_best=False)
            if improve(s, s_one):
                s = s_one
                i = 0
            else:
                i = i + 1
    return s


def main():
    testrange = 1
    result = []
    instancename = "p04"
    specr = 15  # 指定车辆数目 1065.17
    for _ in range(testrange):
        instance = load_instance(name=instancename)
        bestsolution = VNS(instance=instance, specr=specr)
        bestcost = calculate_cost(bestsolution, True)
        result.append(bestcost)
        print(instancename, bestcost)
    result = np.array(result)
    print(np.mean(result), np.std(result))


if __name__ == '__main__':
    main()
