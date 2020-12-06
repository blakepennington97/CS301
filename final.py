# Author: Blake Pennington

#----------------------------------#
# REQUIRES PYTHON 3.6.9 or greater #
#----------------------------------#


# read the input file data.txt and parse it into a dict
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

    return data


# process queries from final.txt in combination with the data gathered
def processQueries(data):
    processing_find = False
    processing_sort = False
    processing_error = False
    queries = []
    conditions = []
    projections = ''
    count = 1
    key = ''
    order = ''
    f = open("final.txt", "r")

    # grab queries and store in queries list
    for line in f:
        queries.append(line.strip('\n '))

    # iterate through lines in queries
    for i in queries:
        # if FIND found, set flag to true so can do appropriate action on following query lines
        if (i == 'FIND' and processing_find == False):
            processing_find = True
            processing_error = False
        # if FIND query lines
        elif (processing_find):
            # get conditions list
            if 'Y' in i:
                conditions.append(i)
            elif (any(cond in i for cond in ('=', '<', '>'))):
                conditions.append(i)
            # now get projections string and send to find() function with appropriate query attributes
            else:
                projections = i.strip(' ;')
                find(data, count, conditions, projections)
                conditions = []
                projections = ''
                processing_find = False
                count+=1
        # if SORT found, set flag to true so can do appropriate action on following query lines
        elif (i == 'SORT' and processing_sort == False):
            processing_sort = True
            processing_error = False
        # if SORT query lines
        elif (processing_sort):
            if '1' in i or '-1' in i:
                # now send to sort() function with appropriate query attributes
                key = i.split(' = ')[0]
                order = i.split(' = ')[1].strip('; ')
                sort(data, count, key, order)
                processing_sort = False
                key = ''
                order = ''
                count+=1
        # if query is NOT FIND or SORT, print error and set flag to process garbage
        elif(not processing_error):
            processing_error = True
        elif(processing_error and ';' in i):
            print(f'\nQuery {count}')
            count+=1
            print('QUERY ERROR: NO FIND OR SORT FOUND')


# sorts db based on key attribute in ascending or descending order
def sort(data, count, key, order):
    print(f'\nQuery {count}')
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

    # sort the data in either ascending/descending order based on key and order parameter
    sorted_data = bubbleSort(temp_data, key, order)

    # print sorted data structure
    for i in temp_data:
        for k, v in i.items():
            print(k, v, sep=': ', end=' ')
        print()
                

# helper function for sort() that sorts the data appropriately based on given parameters
def bubbleSort(data, key, order):
    size = len(data)
    for i in range(size - 1):
        for j in range(0, size-i-1):
            if order == '-1':
                if int(data[j][key]) < int(data[j+1][key]):
                    temp = data[j]
                    data[j] = data[j+1]
                    data[j+1] = temp
            elif order == '1':
                if int(data[j][key]) > int(data[j+1][key]):
                    temp = data[j]
                    data[j] = data[j+1]
                    data[j+1] = temp

    return data


# finds and prints documents in db that meet the wanted criteria for the query
def find (data, count, conditions, projections):
    # query has no conditions
    print(f"\nQuery {count}")
    if 'Y' in conditions:
        # no projections, so print all
        if 'Z' == projections:
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

            # print documents based on the given key(s)
            format_flag = False
            for i in data:
                for k, v in i.items():
                    if k in projections_list:
                        print(k, v, sep=': ', end=' ')
                        format_flag = True
                if (format_flag):
                    print()
                    format_flag = False

    # query has conditions, so process them
    else:
        temp_data = data.copy()
        key_for_condition = ''
        value_for_condition = ''
        remove_list = []

        # loop through conditions and apply appropriate actions
        for i in conditions:
            # first check if condition key even exists in db
            if (any(i.split(' ')[0] in d for d in data)):
                pass
            else:
                return

            # remove all non-matches from temp_data
            for x in remove_list:
                temp_data.remove(x)
            remove_list.clear()
            # if comparison operator is =
            if '=' in i:
                # split condition into key and value variables
                segment = i.split(' = ')
                key_for_condition = segment[0]
                value_for_condition = segment[1]
                # loop through db and gather documents that will be kept or removed
                for j in range(len(temp_data)):
                    if key_for_condition in temp_data[j]:
                        if (temp_data[j][key_for_condition] == value_for_condition):
                            # keep the line because key was found
                            continue
                        else:
                            remove_list.append(temp_data[j])
                    else:
                        remove_list.append(temp_data[j])
            # if comparison operator is >
            elif '>' in i:
                # split condition into key and value variables
                segment = i.split(' > ')
                key_for_condition = segment[0]
                value_for_condition = segment[1]
                # loop through db and gather documents that will be kept or removed
                for j in range(len(temp_data)):
                    if key_for_condition in temp_data[j]:
                        if (temp_data[j][key_for_condition] > value_for_condition):
                            # keep the line because key was found
                            continue
                        else:
                            remove_list.append(temp_data[j])
                    else:
                        remove_list.append(temp_data[j])
            # if comparison operator is <
            elif '<' in i:
                # split condition into key and value variables
                segment = i.split(' < ')
                key_for_condition = segment[0]
                value_for_condition = segment[1]
                # loop through db and gather documents that will be kept or removed
                for j in range(len(temp_data)):
                    if key_for_condition in temp_data[j]:
                        if (temp_data[j][key_for_condition] < value_for_condition):
                            # keep the line because key was found
                            continue
                        else:
                            remove_list.append(temp_data[j])
                    else:
                        remove_list.append(temp_data[j])

        # remove documents that do not match the condition    
        for x in remove_list:
            temp_data.remove(x)

        # no projections, so print all
        if 'Z' == projections:
            for i in temp_data:
                for k, v in i.items():
                    print(k, v, sep=': ', end=' ')
                print()

        # projections exist, so process projections
        else:
            projections_list = projections.split(' ')
            # check if projection key even exists in db
            for i in projections_list:
                if (any(i in d for d in data)):
                    break
                else:
                    return

            # print processed db
            projections_list = projections.split(' ')
            for i in temp_data:
                for k, v in i.items():
                    if k in projections_list:
                        print(k, v, sep=': ', end=' ')
                print()
                




if __name__ == "__main__":

    data = readParse()
    processQueries(data)