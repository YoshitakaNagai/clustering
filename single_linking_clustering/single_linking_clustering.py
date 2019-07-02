import math 
import numpy as np 
import matplotlib.pyplot as plt



class Data:
    def __init__(self, size):
        self.size = size
        self.Coordinate= np.empty((0, 2), float)
        self.Point = np.empty((0, 1))

size = 0
Input = Data(size)


file_name = "./dataset.txt"
try:
    file = open(file_name, "r")
    for line in file:
        if line[0] == "x":
            continue
        else:
            data = line.split()
            Coordinate_tmp = np.array([[float(data[0]), float(data[1])]])
            Point_tmp = np.array([[(data[2])]])
            Input.Coordinate = np.append(Input.Coordinate, Coordinate_tmp, axis=0)
            Input.Point = np.append(Input.Point, Point_tmp, axis=0)
            Input.size += 1
            print("Loading now")
except Exception as error:
    print(error)
finally:
    file.close()


dist_idx = 0
dist_rank_idx = 1

def def_matrix(N):
    dist_matrix = np.zeros((N, N, 2))
    cnt = 0
    for i in range(N):
        for j in range(N):
            if i < j:
                cnt += 1
                dist_matrix[i,j,:] = np.array([calc_dist(i, j), cnt])
            else:
                dist_matrix[i,j,:] = np.array([0, 0])
    return dist_matrix, cnt


def calc_dist(i, j):
    dist = np.linalg.norm(Input.Coordinate[i] - Input.Coordinate[j])
    return dist

def dist_rank_checker(matrix, N, cnt):
    dist_list = np.zeros(cnt)
     
    #make distance list
    list_cnt = 0
    for i in range(N):
        for j in range(N):
            if i < j:
                dist_list[list_cnt] = matrix[i,j,dist_idx]
                list_cnt += 1

    #sort distance list
    for k in range(cnt):
        l = k + 1 
        for l in range(cnt):
            if dist_list[k] < dist_list[l]:
                tmp_dist = dist_list[k]
                dist_list[k] = dist_list[l]
                dist_list[l] = tmp_dist
    ranked_dist_list = dist_list

    for n in range(cnt):
        for i in range(N):
            for j in range(N):
                if i < j and matrix[i,j,dist_idx] == ranked_dist_list[n]:
                    matrix[i,j,dist_rank_idx] = n + 1 
    return matrix


def main():
    N = Input.size
    dist_matrix , dist_rank_cnt = def_matrix(N)
    #print("\ndist_matrix = \n", dist_matrix)
    dist_ranked_matrix = dist_rank_checker(dist_matrix, N, dist_rank_cnt)
    #print("\ndist_ranked_matrix = \n", dist_ranked_matrix)
    
    ic = 0
    jc = 0
    roop = 0
    clustered_chr_list = np.empty((0,1), int)

    #clustering
    print("Let clustering movie start!")

    for roop in range(dist_rank_cnt):
        for i in range(N):
            for j in range(N):
                if i < j and dist_ranked_matrix[i,j,dist_rank_idx] == roop:
                    ic = i
                    jc = j
        
        exist_cluster_flag = False
        for l in range(len(clustered_chr_list)):
            if clustered_chr_list[l] == Input.Point[ic] or clustered_chr_list[l] == Input.Point[jc]:
                Input.Point[ic] = clustered_chr_list[l]
                Input.Point[jc] = clustered_chr_list[l]
                exist_cluster_flag = True
                #print("exist")
                break

        if roop > 0 and exist_cluster_flag == False: 
            #print("new")
            clustered_chr_list = np.append(clustered_chr_list, Input.Point[ic])
            Input.Point[jc] = Input.Point[ic]

       
        plt.clf()
         
        for i in range(Input.size):
            if Input.Point[i] == "A":
                plt_dataset = plt.scatter(Input.Coordinate[i,0], Input.Coordinate[i,1], c="red")
            elif Input.Point[i] == "B":
                plt_dataset = plt.scatter(Input.Coordinate[i,0], Input.Coordinate[i,1], c="orange")
            elif Input.Point[i] == "C":
                plt_dataset = plt.scatter(Input.Coordinate[i,0], Input.Coordinate[i,1], c="green")
            elif Input.Point[i] == "D":
                plt_dataset = plt.scatter(Input.Coordinate[i,0], Input.Coordinate[i,1], c="blue")
            else :
                plt_dataset = plt.scatter(Input.Coordinate[i,0], Input.Coordinate[i,1], c="black")
        
        #plt.show()
        plt.pause(1.0)
    
    print("The end.")

main()
