from pprint import pprint


# read the input file data.txt and parse it into a data structure
def readParse():
    data = {}
    temp = []
    temp2 = []
    f = open("data.txt", 'r')
    for line in f:
        temp3 = line.strip('\n').split(': ')
        for i in temp3:
            temp.append(i.strip(' ').split(' '))
    pprint(temp)

    for sublist in temp:
        for j in sublist:
            temp2.append(j)

    pprint(temp2)
    fieldname = 0
    value = 0

    for i in temp2:
        if (i.isalpha()):
            fieldname = i
            value = 0
        elif (i.isdigit()):
            value = i
            data.setdefault(fieldname, []).append(value)
            fieldname = 0
            value = 0
    
    pprint(data)

            
        

    #pprint(temp2)

    return data



if __name__ == "__main__":

    data = readParse()
