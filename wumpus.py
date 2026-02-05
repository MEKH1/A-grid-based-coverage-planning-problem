import os
from methods import Check_Plan, Find_Plan


directory = 'example-problems'

for filename in os.listdir(directory):
    caveMap=[]
    with open(os.path.join(directory, filename), 'r') as file:
        first_line = file.readline().strip()
        print(filename)
        if first_line =="CHECK PLAN":
            vaccum_path = file.readline().strip() 
            #print(first_line)

            for line in file:
                caveMap.append(line.rstrip('\n'))
            Check_Plan(caveMap,vaccum_path,filename)

        else:
            for line in file:
                caveMap.append(line.rstrip('\n'),)
            print(filename)
            Find_Plan(caveMap,filename)

    
"""
#x="/Users/mohammedekh/Desktop/AI 1 Project/ko40huto-1/assignment/example-problems/problem_f_19.txt"
file_path = "/Users/mohammedekh/Desktop/AI 1 Project/ko40huto-1/assignment/example-problems"

caveMap=[]

with open(x, 'r') as file:
    first_line = file.readline().strip()
    if first_line =="CHECK PLAN":
        vaccum_path = file.readline().strip()
        
        for line in file:
            caveMap.append(line.rstrip('\n'))
        Check_Plan(caveMap,vaccum_path,'problem_f_03.txt')
    else:
        for line in file:
            caveMap.append(line.rstrip('\n'))
        Find_Plan(caveMap,"problem_f_03.txt")

"""