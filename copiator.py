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

    files_search_dir = []
    dir_search = listdir(path_to_search)
    for filename in dir_search:
        full_path_file = join(path_to_search, filename)
        if isfile(full_path_file) and filename != ".DS_Store":
            files_search_dir.append(filename)

    total_copied_files = 0
    total_files_not_match = 0

    with open('files_to_search.txt') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for filename_to_search in spamreader:
            if filename_to_search[0] in files_search_dir:
                full_path_file = join(path_to_search, filename_to_search[0])
                copy(full_path_file, path_to_copy)
                print_success("--> File: \"%s\" copied successfully !" % filename_to_search[0])
                total_copied_files += 1
            else:
                print_warning("--> File: \"%s\" was not found in the directory search" % filename_to_search[0])
                total_files_not_match += 1
    
    print_standard("")
    print_success("-------------------Summary process-------------------")
    print_success("Total new files copied: %s" % total_copied_files)
    print_warning("Total files not found in the list: %s" % total_files_not_match)
    print_success("-----------------------------------------------------")
    print_standard("")

def main(argv):
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

