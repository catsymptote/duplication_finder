## Finds and displays duplication files (based on hashes, filenames, file sizes).
# Author:   Catsymptote
# Email:    catsymptote@gmail.com


##########################################
##########################################

## Settings:
# Include the file running the script in the check?
checkThisFile   = True

# Check file hashes?
checkHashes     = True

# Check file (base)names?
checkFilenames  = True

# Check file sizes?
checkFileSizes  = True

# Exclude certain folders from the check?
excludeFolders  = True

# Folders to be excluded.
excludedFolders   = [
    "venv",
    "test2",
    "test\\example"
]

##########################################
##########################################



import os
import hashlib
import sys
import re
import string



# Print info
print("This script finds the file duplications based on hashes, basenames/filenames, and file sizes.")
print("Hashes are duplications, filenames and file sizes may not.")



def get_files(directory):
    file_list = []
    for path, subdirs, files in os.walk(directory):
        for name in files:
            file_list.append(os.path.join(path, name))
    return file_list



def purge_folders():
    for j in range(len(excludedFolders)):
        i = 0
        while(i < len(file_list)):
            if (get_local_path(file_list[i]).startswith(excludedFolders[j] + "\\")):
                remove_from_lists(i)
            else:
                i += 1



def remove_from_lists(index):
    file_list.pop(index)



def get_basename(filename):
    return os.path.basename(filename)



def is_this_file(filename):
    if(get_local_path(file_list[filename]) == os.path.basename(__file__)):
       return True
    
    return False



def get_name_list(file_list):
    name_list = []
    for i in range(len(file_list)):
        name_list.append(get_basename(file_list[i]))
    return name_list



def get_local_path(filename):
    filename = filename.replace(directory + "\\", "")
    return filename



def calc_hash(file):
    hash_md5 = hashlib.md5()
    with open(file, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()



def get_hash_list(file_list):
    hash_list = []
    for i in range(len(file_list)):
        hash_list.append(calc_hash(file_list[i]))
    return hash_list



def get_size_list(file_list):
    size_list = []
    for i in range(len(file_list)):
        sze = os.path.getsize(file_list[i])
        size_list.append(sze)
    return size_list



def size_matches_empty_file_thingy(size_matches):
    for i in range(len(size_matches)):
        if(os.path.getsize(file_list[size_matches[i][0]]) == 0):
            size_matches.insert(0, -1)
            break
    return size_matches



def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False



def get_matches(s_list):
    matches = []
    for i in range(len(s_list)):
        a = s_list[i]
        for j in range(len(s_list)):
            b = s_list[j]
            if(not i == j):
                if(a == b):
                    if(not i in matches):
                        # Check if the match found is with this file. (See settings)
                        if(checkThisFile and not( is_this_file(i) or is_this_file(j) )):
                            matches = append_match(matches, i, j)
    return matches



def append_match(matches, i, j):
    # Loop through sublists
    inList = False
    for x in range(len(matches)):
        iIn = False
        jIn = False
        # Loop through sublist elements
        for y in range(len(matches[x])):
            # If one element is already matched: add the other
            if(matches[x][y] == i):
                iIn = True
            if(matches[x][y] == j):
                jIn = True
        
        if(iIn or jIn):
            inList = True
        #if(iIn and jIn):
            
        if(iIn and not jIn):
            matches[x].append(j)
        elif(jIn and not iIn):
            matches[x].append(i)

    # If not found in the entire list.
    if(not inList):
        matches.append([i, j])

    return matches



def printer(llist):
    i = 0
    list_length = len(llist)
    while(i < list_length):
        printStr = ">\t"

        # Extra condition when file sizes return -1 instead of list, to indicate empty files. Not the prettiest of solutions.
        if (llist[i] == -1):
            i += 1
            printStr = "Empty files >\t"
        sublist_length = len(llist[i])
        for j in range(sublist_length):
            printStr += str(get_local_path(file_list[llist[i][j]]))
            if (j < sublist_length -1):
                printStr += "\t    ==    "

        print(printStr)
        i += 1



def run():
    print("Working directory:\t" + str(directory) + "\n\n")
    print("\n##########################################")

    # Exclude files in selscted folders. (See settings)
    if(excludeFolders):
        purge_folders()

    # Find matches. (See settings)
    if(checkHashes):
        hash_matches = get_matches(hash_list)
        if (hash_matches):
            print("Hash matches:\n")
            printer(hash_matches)
            print("\n##########################################")


    if(checkFilenames):
        name_matches = get_matches(name_list)
        if (name_matches):
            print("Filename matches:\n")
            printer(name_matches)
            print("\n##########################################")


    if(checkFileSizes):
        size_matches = get_matches(size_list)
        if(size_matches):
            size_matches = size_matches_empty_file_thingy(size_matches)
            print("Filesize matches:\n")
            printer(size_matches)
            print("\n##########################################")


    if (checkHashes):
        print("Hash matches:\t\t" + str(len(hash_matches)))
    if (checkFilenames):
        print("Filename matches:\t" + str(len(name_matches)))
    if (checkFileSizes):
        print("Filesize matches:\t" + str(len(size_matches)))




directory   = os.getcwd()
file_list   = get_files(directory)
if(excludeFolders):
    purge_folders()
    print("Excluded folders:\t" + str(excludedFolders))


hash_list   = get_hash_list(file_list)
name_list   = get_name_list(file_list)
size_list   = get_size_list(file_list)
## Adding new parallel lists? Remember to add to the "matches" print function.



run()
print("\nPress ENTER to close.")
input()
