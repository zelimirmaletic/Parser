def stripBegining(len, string):
    i=0
    temp = ""
    for index,char in enumerate(string):
        if(i>len-1):
            temp += char
        i+=1
    return temp

print(stripBegining(1,'abc'))
