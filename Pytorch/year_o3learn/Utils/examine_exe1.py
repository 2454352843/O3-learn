def read_txt_file(file_name):
    data_list = []
    with open(file_name, 'r') as file:
        for line in file:
            items = line.strip().split('\t')
            # Convert the last item to a list of floats
            last_item = []
            for i in range(11):
                last_item += list(map(float, items[5+i][1:-1].split(', ')))

            data_list.append(last_item)
    return data_list

def filter_data(data_list):
    filtered_data = []
    for row in data_list:
        if all(value <= 10000000 and value >= -100000 for value in row):
            filtered_data.append(True)
        else:
            filtered_data.append(False)
    return filtered_data

if __name__ == "__main__":
    file_name = "../Resource/test3.txt"
    data_list = read_txt_file(file_name)
    filtered_data = filter_data(data_list)


    # Read the original txt file
    with open(file_name, "r") as file:
        lines = file.readlines()

    # Filter the lines based on filtered_data list
    filtered_lines = [line for i, line in enumerate(lines) if filtered_data[i]]

    # Save the filtered content to a new file
    with open("../Resource/test4.txt", "w") as new_file:
        new_file.writelines(filtered_lines)

    # with open("filtered_data.txt", "w") as output_file:
    #     for row in filtered_data:
    #         row_str = "\t".join(str(value) for value in row)
    #         output_file.write(row_str + "\n")
    #
    # print("过滤后的数据已保存到 ../Resource/test2.txt")
