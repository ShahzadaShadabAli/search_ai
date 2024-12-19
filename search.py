import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-m', help="The maze to be searched...")
args = parser.parse_args()

def main():
    nodes = []
    content = []
    explored = []
    frontier_nodes = []
    path_nodes = []
    new_map = ""
    init(content, frontier_nodes, nodes)

    while True:
            try:
                current_node = frontier_nodes[0]
            except IndexError:
                sys.exit("Invalid Maze")
            explored.append(f"{current_node['row']},{current_node['col']}") 
            frontier_nodes.pop(0)
            if current_node["char"] == "G":
                parent = current_node["parent"]
                break
                
                
            else:
                if (checkIfExist(explored, current_node["row"]+1, current_node["col"], content)): #top node
                    addToFrontier({"current": f"{current_node["row"]+1},{current_node["col"]}", "row":current_node["row"]+1, "col":current_node["col"], "action": "t", "parent": current_node["current"], "char": content[current_node["row"]+1][current_node["col"]] }, frontier_nodes, nodes)
                if (checkIfExist(explored, current_node["row"]-1, current_node["col"], content)): #bottom node
                    addToFrontier({"current": f"{current_node["row"]-1},{current_node["col"]}", "row":current_node["row"]-1, "col":current_node["col"], "action": "b", "parent": current_node["current"], "char": content[current_node["row"]-1][current_node["col"]] }, frontier_nodes, nodes)
                if (checkIfExist(explored, current_node["row"], current_node["col"]-1, content)): #left node
                    addToFrontier({"current": f"{current_node["row"]},{current_node["col"]-1}", "row":current_node["row"], "col":current_node["col"]-1, "action": "l", "parent": current_node["current"], "char": content[current_node["row"]][current_node["col"]-1] }, frontier_nodes, nodes)
                if (checkIfExist(explored, current_node["row"], current_node["col"]+1, content)): #right node
                    addToFrontier({"current": f"{current_node["row"]},{current_node["col"]+1}", "row":current_node["row"], "col":current_node["col"]+1, "action": "r", "parent": current_node["current"], "char": content[current_node["row"]][current_node["col"]+1] }, frontier_nodes, nodes)
    while True:
        row, col = parent.split(',')
        for node in nodes:
            if node["row"]==int(row) and node["col"] == int(col):
                path_nodes.insert(0, node)
                parent = node["parent"]
                char = node["char"]
        if char == "S":
            break
    filename = drawMap(path_nodes, content, new_map)
    print("The solution is produced in", filename)

def drawMap(path_nodes, content, new_map):
    sol_num, _ = args.m.split(".")
    sol_filename = "solution-"+sol_num[-1]+".txt"
    file = open(sol_filename, "w")
    for i, row in enumerate(content):
        for j, col in enumerate(row):
           char = checkIfPath(i, j, path_nodes)
           char = ("+" if char == " " else char)
           if char != False:
               new_map = new_map+char
           else:
               new_map = new_map+content[i][j]
        file.write(f"{new_map}\n")
        new_map = ''
    return sol_filename
def checkIfPath(row, col, path_nodes):
    try:
        res = False
        for path_node in path_nodes:
            if (path_node["row"] == int(row) and path_node["col"] == int(col)):
                res = path_node["char"]
        return res
    except KeyError:
        return False
  
def checkIfExist(explored, row, col, content):
    try:
        isTrue = False
        res = content[row][col]
        if res != "#":
            isTrue = True
        for ids in explored:
            thisrow, thiscol = ids.split(",")
            if (int(thisrow) == row and int(thiscol) == col):
                isTrue = False
        return isTrue
    except IndexError:
        return False
    
def init(content, frontier_nodes, nodes):
      with open(args.m) as file:
        lines = file.readlines()
        for i, line in enumerate(lines):
            content.append([])
            chars = [char for char in line if char != '\n']
            for j, char in enumerate(chars):
                content[i].append([])
                content[i][j] = char 
                if char == "S":
                    addToFrontier({"current": f"{i},{j}", "row":i, "col":j, "action": None, "parent": None, "char": char}, frontier_nodes, nodes)


def addToFrontier(node, frontier_nodes, nodes):
    frontier_nodes.append(node)
    nodes.append(node)

main()