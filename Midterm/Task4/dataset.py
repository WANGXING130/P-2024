import random

# model params as below:
# @brief 模型参数

# @param K 汽车数量
K = 2              # 按照论文参考文献[3]中的数据来，有2辆车
# @param Q_k 单汽车载重量上限
Q = 8           # 单位为吨，因为数据都相同，则做成一个数值
# @param D_k 单汽车单次行驶距离上限 *原文为h，疑似写错*
D = 40             # 单位为km，因为数据都相同，则做成一个数值

# @param L 需求物资点数量
L = 8              # 按照论文参考文献[3]中的数据来，有8物资点
# @param q_i 每个物资点需求数量
q = [1, 2, 1, 2, 1, 4, 2, 2]


# @param d_ij 物资点i和物资点j的距离
# @param d_0j 汽车出发地到物资点j的距离 *即出发地下标设为0*
d = [
    0, 4.0, 6.0, 7.5, 9.0, 20.0, 10.0, 16.0, 8.0, 0,
    4.0, 0, 6.5, 4.0, 10.0, 5.0, 7.5, 11.0, 10.0, 4.0,
    6.0, 6.5, 0, 7.5, 10.0, 10.0, 7.5, 7.5, 7.5, 6.0,
    7.5, 4.0, 7.5, 0, 10.0, 5.0, 9.0, 9.0, 15.0, 7.5,
    9.0, 10.0, 10.0, 10.0, 0, 10.0, 7.5, 7.5, 10.0, 9.0,
    20.0, 5.0, 10.0, 5.0, 10.0, 0, 7.0, 9.0, 7.5, 20.0,
    10.0, 7.5, 7.5, 9.0, 7.5, 7.0, 0, 7.0, 10.0, 10.0,
    16.0, 11.0, 7.5, 9.0, 7.5, 9.0, 7.0, 0, 10.0, 16.0,
    8.0, 10.0, 7.5, 15.0, 10.0, 7.5, 10.0, 10.0, 0, 8.0,
    0, 4.0, 6.0, 7.5, 9.0, 20.0, 10.0, 16.0, 8.0, 0
]

lst_sum = []  #初始群体
F_sum = []    #个体适应度
P_sum = []    #单个概率
P_Cumu_sum = []  #累计概率

#创建初始群体
for i in range(20):
    lst = random.sample(range(1, 10), 9)
    lst_sum.append(lst)

#传入一个列表作为参数
def MinZ(lst):
#若最后一个值为9，则为空列表
    z = 0
    n = 0

    if len(lst) == 0:
     return z
    while n < len(lst) - 1:
        z += d[lst[n] * 10 + lst[n + 1]]
        n += 1
    z = z + d[lst[0]] + d[lst[len(lst) - 1]]
    return z
def Check(lst):
    error = 0
    if MinZ(lst) > D:
        error += 1

    Q_sum = 0
    for i in range(len(lst)):
        Q_sum += q[lst[i]-1]

    if Q_sum > Q:
        error += 1

    return error
#选择操作
def choice():
    lst_sum_new = []  # 储存 选择操作后的 新群体

    lst_sum_new.append(lst_sum[0])

    #其他N-1个个体的选择
    while len(lst_sum_new) <= 20:
        for i in range(1,len(lst_sum)):
            if random.random() <= P_Cumu_sum[i]:
                for j in range(round(20 * P_Cumu_sum[i])):
                    lst_sum_new.append(lst_sum[i])
                    if len(lst_sum_new) == 20:
                        return lst_sum_new
    return lst_sum_new
#交叉操作
def cross():

    lst_sum_new1 = lst_sum[:1]

    lst_sum_slice = lst_sum[1:]

    remaining_indices = list(range(len(lst_sum_slice)))

    for i in range( len(lst_sum_slice) //2):

        if len(lst_sum_slice) < 2:
            break

        idx1,idx2 = random.sample(remaining_indices, 2)
        subA,subB = lst_sum_slice[idx1],lst_sum_slice[idx2]

        slice_subA = subA[:4]
        slice_subB = subB[:4]

        new_subA = slice_subB + [item for item in subA if item not in slice_subB]
        lst_sum_new1.append(new_subA)

        new_subB = slice_subA + [item for item in subB if item not in slice_subA]
        lst_sum_new1.append(new_subB)

        remaining_indices.remove(idx1)
        remaining_indices.remove(idx2)

    lst_sum_new1.extend(lst_sum_slice[i] for i in remaining_indices)

    return lst_sum_new1

#变异操作
def vary(lst):

    selected_indexs = []          #存储被选中的数字的index

    selected_items = random.sample(lst, 3)
    for i in selected_items:
        selected_indexs.append(lst.index(i))

    random.shuffle(selected_items) #打乱顺序

    for index,item in zip(selected_indexs,selected_items):
        lst[index] = item

#计算个体适应度
def CalcF():
    for lst in lst_sum:
        index = lst.index(9)
        sub1 = lst[:index]
        sub2 = lst[index + 1:]

        Z = 0
        M = 0
        for sub in [sub1,sub2]:
            Z += MinZ(sub)
            M += Check(sub)

        F = 1.0 / (Z + 100 * M)
        F_sum.append(F)
#计算选择概率
def CalcP():
    sum = 0  #F_sum 列表的所有加和
    for i in range(20):
        sum += F_sum[i]
    for i in range(20):
        P_sum.append(F_sum[i] * 1.0 / sum)


def CumuP():
    P = 0
    for i in range(19,0,-1):
        for j in range(19,i-1,-1):
            P += P_sum[j]
        P_Cumu_sum.append(P)
    P_Cumu_sum.reverse()



#为F、P、个体排序
def sortout():
    for i in range(20):
        for n in range(19,0,-1):
            if F_sum[n] > F_sum[n-1]:
                temp_F = F_sum[n]
                F_sum[n] = F_sum[n-1]
                F_sum[n-1] = temp_F

                temp_lst = lst_sum[n]
                lst_sum[n] = lst_sum[n-1]
                lst_sum[n-1] = temp_lst

                temp_P = P_sum[n]
                P_sum[n] = P_sum[n-1]
                P_sum[n-1] = temp_P
#初始化
def init():
    CalcF()
    CalcP()
    sortout()
    CumuP()


if __name__ == '__main__':
    for i in range(500):
        #初始化F、P
        F_sum = []
        P_sum = []
        P_Cumu_sum = []
        init()

        for i in range(20):
            print(lst_sum[i],F_sum[i],P_sum[i])
        print('\n')


        lst_sum = choice()
        F_sum = []
        P_sum = []
        P_Cumu_sum = []
        init()


        if random.random() <= 0.95:
            print('交叉')
            lst_sum = cross()
            F_sum = []
            P_sum = []
            P_Cumu_sum = []
            init()


        for lst in lst_sum:
            if random.random() <= 0.05:
                print('变异')
                vary(lst)

            F_sum = []
            P_sum = []
            P_Cumu_sum = []
            init()

    print('\n')
    for i in lst_sum:
        print(i)


    print('\n')
    index = lst_sum[0].index(9)
    sub1 = lst_sum[0][:index]
    sub2 = lst_sum[0][index + 1:]
    print(sub1,sub2)

    Z = 0
    for sub in [sub1,sub2]:
        Z += MinZ(sub)
        print(Z)
    print(Z)
