import os
import hashlib


def hash_file(filename):
    """"This function returns the SHA-1 hash
    of the file passed into it"""

    # make a hash object
    h = hashlib.sha1()

    # open file for reading in binary mode
    with open(filename, 'rb') as file:
        # loop till the end of the file
        chunk = 0
        while chunk != b'':
            # read only 1024 bytes at a time
            chunk = file.read(1024)
            h.update(chunk)

    # return the hex representation of digest
    return h.hexdigest()


def check_for_duplicates(path):
    """This function checks for duplicates in the directory
    specified in 'path' and removes them"""

    # create a list of files in the directory
    files = os.listdir(path)

    # create a dictionary to store the hash values
    hash_keys = dict()

    # loop through each file in the directory
    for index, file in enumerate(files):

        # get the full path of the file
        full_path = os.path.join(path, file)

        # check if the file is a directory
        if os.path.isdir(full_path):
            # if the file is a directory, recursively check for duplicates
            check_for_duplicates(full_path)
        else:
            # if the file is empty, remove it
            if os.path.getsize(full_path) == 0:
                os.remove(full_path)
            else:
                # get the hash value of the file
                file_hash = hash_file(full_path)

                # check if the hash value is in the dictionary
                if file_hash in hash_keys:
                    # if the hash value is in the dictionary,
                    # remove the current file
                    os.remove(full_path)
                else:
                    # if the hash value is not in the dictionary,
                    # add it to the dictionary
                    hash_keys[file_hash] = index


# specify the directory you want to check for duplicates
directory = 'C:\\Users\\feder\\PycharmProjects\\IndexRetrivalProject\\src\\Documents'

# call the function to remove duplicates
check_for_duplicates(directory)
