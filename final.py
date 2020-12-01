
# REQUIRES PYTHON 3.6.9 or greater
from pprint import pprint


# read the input file data.txt and parse it into a data structure
def readParse():
    data = []
    ID = 0
    f = open("data.txt", 'r')

    # append in each line in input with a unique ID field 'A'
    for line in f:
        temp_dict = {}
        formatted_segment = (f'A: {ID} ' + line.strip('\n ')).split(' ')
        for i in range(len(formatted_segment)):
            if (i < len(formatted_segment) and (i % 2 == 0)):
                temp_dict[formatted_segment[i]] = formatted_segment[i+1]
        data.append(temp_dict)
        ID+=1

    
    pprint(data)
    return data


# process queries from final.txt in combination with the data gathered
def processQueries(data):
    processing_find = False
    queries = []
    conditions = []
    projections = []
    count = 0
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
                projections.append(i.strip(' ;'))
                find(data, count, conditions, projections)
                processing_find = False
                count+=1


def find (data, count, conditions, projections):
    print(f"Query {count}")
    # if no conditions
    if 'Y' in conditions:
        # if no projections
        if 'Z' in projections:
            for i in data:
                print(i)




if __name__ == "__main__":

    data = readParse()
    processQueries(data)
