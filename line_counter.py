import sys
import os

endings=["lua"]
line_count = 0

if not sys.argv[1]:
    print("Please enter a directory as first parameter")
    exit()
path = sys.argv[1]

if not os.path.exists(path):
    print("Your given path does not exist!")
    exit()

for root,folders,files in os.walk(path):

    
    for file in files:
        if root.find(".git") != -1:
            
            continue

        split_file = file.split(".")
        #print(split_file)
        if len(split_file) >1:
            
            if split_file[1] in endings:
                file_path = os.path.abspath(os.path.join(root,file))
                file = open(file_path)
                lines=file.readlines()
                file.close()

                

                for line in lines:
                    line_count+=1
                    if line.strip() !="":
                        line_bare =line.strip()
                        

print(line_count)

