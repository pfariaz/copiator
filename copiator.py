import sys, getopt
from os.path import (
    exists,
    isdir,
    isfile,
    join
)
from os import (
    mkdir,
    listdir
)
from shutil import (
    copy
)
import csv

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_error(msg):
    print(bcolors.FAIL+msg)
def print_success(msg):
    print(bcolors.OKGREEN+msg)
def print_standard(msg):
    print(bcolors.ENDC+msg)
def print_warning(msg):
    print(bcolors.WARNING+msg)

def process_copy(path_to_search, path_to_copy):
    if not exists(path_to_search):
        print_error("The path \"%s\" doesn't exists" % path_to_search)
        return
    if not exists(path_to_copy):
        print_error("The path \"%s\" doesn't exists but it will be created for this purpose :)" % path_to_search)
        mkdir(path_to_copy)

    files_to_copy = []
    with open('files_to_search.txt') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            files_to_copy.append(row[0])

    dir_search = listdir(path_to_search)
    total_copied_files = 0
    total_files_not_match = 0
    total_files_destination = 0
    total_files_not_mp3 = 0
    if len(dir_search) == 0:
        print_error("There are no files in this directory :(")
    for filename in dir_search:
        full_path_file = join(path_to_search, filename)
        if isfile(full_path_file):
            files_splitted = filename.split(".")
            if files_splitted[0] in files_to_copy:
                if not exists(join(path_to_copy, filename)):
                    copy(full_path_file, path_to_copy)
                    if files_splitted[1] is not "mp3":
                        print_error("--> File: \"%s\" copied successfully but is not a mp3 format !" % filename)
                        total_files_not_mp3 += 1
                    else:
                        print_success("--> File: \"%s\" copied successfully !" % filename)
                    total_copied_files += 1
                else:
                    print_warning("--> File: \"%s\" was found in the destination folder !" % filename)
                    total_files_destination += 1
            else:
                print_warning("--> File: \"%s\" was not found in the file list to copy" % filename)
                total_files_not_match += 1
    
    print_standard("")
    print_success("-------------------Summary process-------------------")
    print_success("Total new files copied: %s" % total_copied_files)
    print_warning("Total files not found in the list: %s" % total_files_not_match)
    print_warning("Total files not mp3: %s" % total_files_not_mp3)
    print_warning("Total files matching list but already in destination folder: %s" % total_files_destination)
    print_success("-----------------------------------------------------")
    print_standard("")

def main(argv):
   file_names = ''
   path_to_search = ''
   path_to_copy = ''
   try:
      opts, args = getopt.getopt(argv,"hs:o:",["pathsearch=","pathout="])
   except getopt.GetoptError:
      print('Usage: test.py -s <path_to_search> -o <path_to_copy>')
      sys.exit(2)

   for opt, arg in opts:
      if opt == '-h':
         print('Usage: test.py -s <path_to_search> -o <path_to_copy>')
         sys.exit()
      elif opt in ("-s", "--pathsearch"):
         path_to_search = arg
      elif opt in ("-o", "--pathout"):
         path_to_copy = arg

   print("Initializing....")
   process_copy(path_to_search, path_to_copy)
   print_success("Process finished")

if __name__ == "__main__":
    main(sys.argv[1:])

