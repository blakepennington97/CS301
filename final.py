
# REQUIRES PYTHON 3.6.9 or greater
from pprint import pprint


# read the input file data.txt and parse it into a data structure
def readParse():
    data = []
    ID = 1
    f = open("data.txt", 'r')

    # append in each line in input with a unique ID field 'A'
    for line in f:
        temp_dict = {}
        formatted_segment = (f'A: {ID} ' + line.strip('\n ')).split(' ')
        for i in range(len(formatted_segment)):
            if (i < len(formatted_segment) and (i % 2 == 0)):
                temp_dict[formatted_segment[i].strip(':')] = formatted_segment[i+1]
        data.append(temp_dict)
        ID+=1

    
    #pprint(data)
    return data


# process queries from final.txt in combination with the data gathered
def processQueries(data):
    processing_find = False
    processing_sort = False
    queries = []
    conditions = []
    projections = ''
    count = 1
    key = ''
    order = ''
    f = open("final.txt", "r")

    for line in f:
        queries.append(line.strip('\n '))

    for i in queries:
        if (i == 'FIND' and processing_find == False):
            processing_find = True
        elif (processing_find):
            # get conditions
            if 'Y' in i:
                conditions.append(i)
            elif (any(cond in i for cond in ('=', '<', '>'))):
                conditions.append(i)
            # now get projections
            else:
                projections = i.strip(' ;')
                find(data, count, conditions, projections)
                conditions = []
                projections = ''
                processing_find = False
                count+=1
        elif (i == 'SORT' and processing_sort == False):
            processing_sort = True
        elif (processing_sort):
            if '1' in i or '-1' in i:
                key = i.split(' = ')[0]
                order = i.split(' = ')[1].strip('; ')
                sort(data, key, order)
                processing_sort = False
                key = ''
                order = ''
        else:
            exit('ERROR IN QUERIES: NO FIND OR SORT FOUND')


def sort(data, key, order):
    temp_data = data.copy()
    sorted_data = []
    remove_list = []

    # check if ANY document contains the sort field
    if (any(key in d for d in data)):
        pass
    else:
        return



    # remove documents that DO NOT have the sort field
    for j in range(len(temp_data)):
        #temp = temp_data[j].pop(key_for_condition, '')
        if key in temp_data[j]:
            continue
        else:
            remove_list.append(temp_data[j])

    # remove all non-matches from temp_data
    for x in remove_list:
        temp_data.remove(x)

    sorted_data = bubbleSort(temp_data, key, order)

    print()
    for i in temp_data:
        for k, v in i.items():
            print(k, v, sep=': ', end=' ')
        print()
    #print()
                

def bubbleSort(data, key, order):
    size = len(data)
    for i in range(size - 1):
        for j in range(0, size-i-1):
            if order == '-1':
                if data[j][key] < data[j+1][key]:
                    temp = data[j]
                    data[j] = data[j+1]
                    data[j+1] = temp
            elif order == '1':
                if data[j][key] > data[j+1][key]:
                    temp = data[j]
                    data[j] = data[j+1]
                    data[j+1] = temp

    return data

def find (data, count, conditions, projections):
    # no conditions
    if 'Y' in conditions:
        # no projections, so print all
        if 'Z' in projections:
            print(f"Query {count}")
            for i in data:
                for k, v in i.items():
                    print(k, v, sep=': ', end=' ')
                print()

        # get projections
        else:

            projections_list = projections.split(' ')

            # check if projection key even exists in db
            for i in projections_list:
                if (any(i in d for d in data)):
                    pass
                else:
                    return

            print(f"Query {count}")

            for i in data:
                for k, v in i.items():
                    if k in projections_list:
                        print(k, v, sep=': ', end=' ')
                print()

    # get conditions
    else:
        temp_data = data.copy()
        key_for_condition = ''
        value_for_condition = ''
        remove_list = []

        for i in conditions:

            # check if condition key even exists in db
            if (any(i.split(' ')[0] in d for d in data)):
                pass
            else:
                return

            # remove all non-matches from temp_data
            for x in remove_list:
                temp_data.remove(x)
            remove_list.clear()
            if '=' in i:
                segment = i.split(' = ')
                key_for_condition = segment[0]
                value_for_condition = segment[1]
                for j in range(len(temp_data)):
                    #temp = temp_data[j].pop(key_for_condition, '')
                    if key_for_condition in temp_data[j]:
                        if (temp_data[j][key_for_condition] == value_for_condition):
                            # keep the line because key was found
                            continue
                        else:
                            remove_list.append(temp_data[j])
                    else:
                        remove_list.append(temp_data[j])
            elif '>' in i:
                segment = i.split(' > ')
                key_for_condition = segment[0]
                value_for_condition = segment[1]
                for j in range(len(temp_data)):
                    #temp = temp_data[j].pop(key_for_condition, '')
                    if key_for_condition in temp_data[j]:
                        if (temp_data[j][key_for_condition] > value_for_condition):
                            # keep the line because key was found
                            continue
                        else:
                            remove_list.append(temp_data[j])
                    else:
                        remove_list.append(temp_data[j])
            elif '<' in i:
                segment = i.split(' < ')
                key_for_condition = segment[0]
                value_for_condition = segment[1]
                for j in range(len(temp_data)):
                    #temp = temp_data[j].pop(key_for_condition, '')
                    if key_for_condition in temp_data[j]:
                        if (temp_data[j][key_for_condition] < value_for_condition):
                            # keep the line because key was found
                            continue
                        else:
                            remove_list.append(temp_data[j])
                    else:
                        remove_list.append(temp_data[j])
                    
        for x in remove_list:
            temp_data.remove(x)

        # no projections, so print all
        if 'Z' in projections:
            print(f"Query {count}")
            for i in temp_data:
                for k, v in i.items():
                    print(k, v, sep=': ', end=' ')
                print()

        # get projections
        else:
            print(f"Query {count}")
            projections_list = projections.split(' ')
            for i in temp_data:
                for k, v in i.items():
                    if k in projections_list:
                        print(k, v, sep=': ', end=' ')
                print()
                




if __name__ == "__main__":

    data = readParse()
    processQueries(data)
