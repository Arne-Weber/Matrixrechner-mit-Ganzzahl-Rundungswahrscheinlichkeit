import sys
import copy
import shutil
import math
import time
import matplotlib.pyplot as plt
import os

last_input_time = time.time()

sys.setrecursionlimit(150000000)

#size = int(input("size: "))
size = 4
Base_empty = []
for row in range(size):
  Base_empty.append([])
  for column in range(size):
    Base_empty[row].append(float(0))

Start_empty = []
for row in range(size):
  Start_empty.append([])
  Start_empty[row].append(float(0))

for i in range(shutil.get_terminal_size().lines):
  print("\n")

def draw(text, *Matrices):
  max_length = shutil.get_terminal_size().columns
  print(chr(27) + "[2J")
  #print(Matrices)
  for Matrix in Matrices:
    for line in Matrix:
      justify_length = math.floor((max_length - len(line))/(len(line)))
      pretty = ""
      for i, value in enumerate(line):
        pretty = pretty + str(value).ljust(justify_length) + '|'
      print(pretty)
    print("\n")
  print (text)

def define(Matrix):
  for line, line_v in enumerate(Matrix):
   for column, column_v in enumerate(line_v):
    draw(f"({line+1}|{column+1})", Matrix)
    val = input()
    if val == '':
      val = Matrix[line][column]
    else:
      val = float(val)
    Matrix[line][column] = val
  return Matrix

def step(matrix, lists, position, lists_index, output):
    lists_length = len(lists) - 1
    if position == "init":
        position = []
        lists_index = -1
        output = []
        for i in matrix:
          output.append([])
    
    if not (lists_index == lists_length):
        position.append(0)
        lists_index += 1
        return step(matrix, lists, position, lists_index, output)
    else:
        combination = []
        for list, cell in enumerate(position):
            combination.append(lists[list][cell])
        # CODE HERE
        #output.append(combination)
        #print(position)
        for coordinate, coordinate_v in enumerate(matrix):
          result_value = 0
          result_probability = 1
          for position_i, position_v in enumerate(position):
            input_vector_probability = lists[position_i][position_v][0]
            input_vector_value = lists[position_i][position_v][1]
            input_matrix_value = coordinate_v[position_i]
            result_value +=  input_vector_value * input_matrix_value
            result_probability *= input_vector_probability

          if result_value.is_integer():
            output[coordinate].append((result_probability, result_value))
          else:
            output[coordinate].append((result_probability * (result_value % 1), math.ceil(result_value)))
            output[coordinate].append((result_probability * (1 - (result_value % 1)), math.floor(result_value)))
          #input(f"position_i: {position_i}\nposition_v: {position_v}\nresult: {output}")
        
        # /CODE HERE
        position[lists_index] += 1
        while len(lists[lists_index]) == position[lists_index]:
            lists_index -= 1
            position.pop()
            if position == []:
                return output
            position[lists_index] += 1
        return step(matrix, lists, position, lists_index, output)
  
def congregate(vector):
  output_vector = []
  for coordinate, coordinate_v in enumerate(vector):
    output_vector.append([])
    found_values = []
    for tup in coordinate_v:
      try:
        output_vector[coordinate][found_values.index(tup[1])][0] += tup[0]
      except ValueError:
        output_vector[coordinate].append(list(tup))
        found_values.append(tup[1]) 
  return output_vector



#Base = define(Base_empty)
Base = [[0.95, 0.0, 0.0, 0.15], [300.0, 0.0, 0.0, 0.0], [0.0, 0.01, 0.0, 0.0], [0.0, 0.0, 0.7, 0.0]]
  
#Start = define(Start_empty)
#for line, line_v in enumerate(Start):
#  Start[line] = [(1, line_v[0])]

Start = [[(1, 264)], [(1, 0)], [(1, 0)], [(1, 0)]]
#Start = [[(1, 264)], [(1, 0)], [(1, 0)], [(0.75, 0), (0.25, 7)]]
  
Active_Matrix = copy.deepcopy(Base)
Active_values = copy.deepcopy(Start)

iteration_count = 0
last_exec_time = 0
history_for_draw = []
while True:
  last_exec_time = time.time() - last_input_time
  draw(f"clear(cl), reset(rs), step(st), show(sh)     | iterations: {iteration_count}, last execution took: {last_exec_time}s", Start, Active_values, Active_Matrix)
  cli = input()
  last_input_time = time.time()
  match cli:
    case "clear" | "cl":
      iteration_count = 0
      Active_Matrix = copy.deepcopy(Base)
      Active_values = copy.deepcopy(Start)
      
    case "reset" | "rs":
      iteration_count = 0
      Base = define(Base_empty)
  
      Start = define(Start_empty)
      for line, line_v in enumerate(Start):
        Start[line] = (1, line_v)
      
      Active_Matrix = copy.deepcopy(Base)
      Active_values = copy.deepcopy(Start)
      

    case "step" | "st" | "":
      step_count = int(input("How many steps?"))
      for i in range(step_count):
        last_iter_time = time.time()
        iteration_count += 1
        Active_values = step(Active_Matrix, Active_values, "init", "", "")
        Active_values = congregate(Active_values)
        history_for_draw.append([])
        for dimension in Active_values:
          history_for_draw[-1].append([])
          history_for_draw[-1][-1].append([])
          history_for_draw[-1][-1].append([])
          for tuple in dimension:
            history_for_draw[-1][-1][-2].append(tuple[0])
            history_for_draw[-1][-1][-1].append(tuple[1])
        draw(f"iterations: {iteration_count}/{step_count}, last execution took: { time.time() - last_iter_time}s", Start, Active_values, Active_Matrix)

        save_file_int = 1
        while os.path.exists(f"./saved_data_{save_file_int}.txt"):
          save_file_int += 1
        with open(f"./saved_data_{save_file_int}.txt", 'w+') as f:
          f.write(str(history_for_draw))


    case "show" | "sh":
      rows_num = math.floor(math.sqrt(size))
      columns_num = math.ceil(size/rows_num)
      fig, axs = plt.subplots(rows_num, columns_num) #nrows, ncols
      row_i = 0
      col_i = 0
      for dimension in range(size):
        for timepoint, timepoint_v in enumerate(history_for_draw):
          axs[row_i, col_i].plot(timepoint_v[dimension][1], timepoint_v[dimension][0], label=f"time: {timepoint + 1}")
        axs[row_i, col_i].set_title(f'x{dimension + 1}')
        axs[row_i, col_i].legend()
        axs[row_i, col_i].grid(True)
        col_i += 1
        if col_i == columns_num:
          row_i += 1
          col_i = 0
      plt.show()
  

    case source:
      print(source)