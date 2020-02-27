import csv
from bisect import bisect_left


cdli_atf=open("./data/cdliatf_unblocked.atf", "r")
cdli_data = cdli_atf.readlines()


cdli_catalogue_csv = csv.DictReader(open("./data/cdli_catalogue_1of2.csv", "r"))
cdli_catalogue = []
for line in cdli_catalogue_csv:
    cdli_catalogue.append(line)


cdli_catalogue = []
genre_list = []
atf_id_list = []
catalogue_id_list = []


def list_of_genres():
    cdli_catalogue_csv = open("./data/cdli_catalogue_1of2.csv", "r")
    cdli_catalogue_data = csv.DictReader(cdli_catalogue_csv)
    for line in cdli_catalogue_data:
        cdli_catalogue.append(line)

    genre_set = set()
    for item in cdli_catalogue:
        genre_set.add(item["genre"])

    genre_list = list(genre_set)
    genre_list.sort()
    cdli_catalogue_csv.close()
    print(genre_list)

    return genre_list

def print_to_file(starting_line, file):
    file.write(cdli_data[starting_line])
    for i in range(starting_line+1, len(cdli_data)):
        line = cdli_data[i]
        if(line[:2]!="&P"):
            file.write(line)
        else:
            break

def translated_sumerian ():
    sumerian_translated = open("sumerian_translated.atf","w")

    for i in range(len(cdli_data)):

        line = cdli_data[i]
        starting_line = i-1
        last_line = i+1

        if(line.find("#atf:") !=-1 and line.find("lang") !=-1 and line.find("sux") !=-1):

            while(starting_line>=0):
                if(cdli_data[starting_line][:2]!="&P"):
                    starting_line-=1
                else:
                    break

            while(last_line < len(cdli_data) and cdli_data[last_line][:2]!="&P"):
                if(cdli_data[last_line].find("#tr.en:")!=-1):
                    print_to_file(starting_line, sumerian_translated)
                    break

                last_line+=1
    sumerian_translated.close()
    print("\nYour requested data has been printed into sumerian_translated.atf\n")

def all_sumerian():
    sumerian_untranslated = open("sumerian_untranslated.atf","w")

    for i in range(len(cdli_data)):

        line = cdli_data[i]
        starting_line = i-1

        if(line.find("#atf:") !=-1 and line.find("lang") !=-1 and line.find("sux") !=-1):

            while(starting_line>=0):
                if(cdli_data[starting_line][:2]!="&P"):
                    starting_line-=1
                else:
                    break

            print_to_file(starting_line, sumerian_untranslated)
    sumerian_untranslated.close()
    print("\nYour requested data has been printed into sumerian_untranslated.atf\n")

def catalogue(genre):
    for i in range(len(cdli_data)):
        line = cdli_data[i]

        if(line[:2]=="&P"):
            idlist = line.split()
            id = (idlist[0])[2:8]
            atf_id_list.append(((int(id)), i))

    for i in range(len(cdli_catalogue)):
        catalogue_id_list.append((cdli_catalogue[i]["genre"],int(cdli_catalogue[i]["id_text"])))

    atf_id_list.sort()
    catalogue_id_list.sort()
    search_index_low = bisect_left(catalogue_id_list, (genre,))
    search_index_high = search_index_low
    print_count = 0

    if(search_index_low < len(catalogue_id_list) and catalogue_id_list[search_index_low][0] == genre):
        genre_atf = open("genre.atf", "w")
        while search_index_high < len(catalogue_id_list)-1:
            if(catalogue_id_list[search_index_high+1][0] == genre):
                search_index_high+=1
            else:
                break
        for i in range(search_index_low, search_index_high+1):

            atf_index = bisect_left(atf_id_list, (catalogue_id_list[i][1],))
            if(atf_index < len(atf_id_list) and atf_id_list[atf_index][0] == catalogue_id_list[i][1]):
                if print_count == 0:
                    genre_atf = open("genre.atf", "w")
                    print_count+=1
                print_to_file(atf_id_list[atf_index][1], genre_atf)
    if(print_count > 0):
        genre_atf.close()
        print("\nYour requested data has been printed into genre.atf\n")
    elif print_count == 0:
        print("\nSorry, data pertaining to this genre is not currently available.")


print("\nHi, welcome to the cdli data extractor script\n")
print("1\tSumerian language texts.\n2\tSumerian language texts with translation.\n3\tSort by genre.\n ")
first_choice = int(input("Please enter the number corresponding to your choice: "))
if(first_choice==3):
    print("\nPlease wait for all the genres to appear.\n")
    genre_list = list_of_genres()
    for i in range(len(genre_list)):
        print("{}\t{}".format(i+1, genre_list[i]))
    second_choice = int(input("\n\nPlease enter the number corresponding to your choice: "))
    catalogue(genre_list[second_choice-1])
if(first_choice==1):
    all_sumerian()
if(first_choice==2):
    translated_sumerian()

cdli_atf.close()
