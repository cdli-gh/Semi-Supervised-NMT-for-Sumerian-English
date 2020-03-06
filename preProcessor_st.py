raw = open('sumerian_translated.atf', encoding="utf8")
raw = raw.readlines()
english = open('english_st.txt', 'a', encoding="utf8")
sumerian = open('sumerian_st.txt', 'a', encoding="utf8")
for index,line in enumerate(raw):
    flag = 0
    if line[0].isdigit():
        sumerian.writelines(line[3:])
        for engLine in raw[(index+1):]:
            if engLine[1:6] == "tr.en":
                try:
                    english.write(engLine[8])
                    english.write(engLine[9:])
                except:
                    english.write('nAn\n')
                flag = 0
                break
            elif engLine[0].isdigit():
                english.write('nAn\n')
                flag = 0
                break
            else:
                flag = 1
        if flag == 1:
            english.write('nAn\n')
            
english.close()
sumerian.close()