def extractTokenName(string):
    i = 1
    tokenName = ''
    while string[i]!='>':
        tokenName += string[i]
        i+=1
    return tokenName





token = " <ANIMAL> := 'CAT' | 'DOG' | 'PARROT' | 'LAMA' "
print(extractTokenName(token))





