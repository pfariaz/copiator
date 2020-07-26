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
        print_error("La carpeta \"%s\" no existe" % path_to_search)
        return
    if not exists(path_to_copy):
        print_error("La carpeta \"%s\" no existe pero la crearemos para este proposito :)" % path_to_search)
        mkdir(path_to_copy)

    files_search_dir = []
    dir_search = listdir(path_to_search)
    for filename in dir_search:
        full_path_file = join(path_to_search, filename)
        if isfile(full_path_file) and filename != ".DS_Store":
            files_search_dir.append(filename)

    total_copied_files = 0
    total_files_not_match = 0
    total_files_not_copied = 0
    total_files_to_copy = 0
    total_duplicated_files = 0

    line_number = 1
    with open('files_to_search.txt') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for filename_to_search in spamreader:
            total_files_to_copy +=1 
            if filename_to_search[0] in files_search_dir:
                full_path_file = join(path_to_search, filename_to_search[0])
                destination_final_name = join(path_to_copy, filename_to_search[0])
                if exists(destination_final_name):
                    print_error("--> Archivo({}): \"{}\" ya existe en la carpeta de destino (DUPLICADO) !".format(line_number,filename_to_search[0]))
                    total_duplicated_files += 1
                    continue
                copy(full_path_file, destination_final_name)
                print_standard("Tratando de copiar de {} a {}".format(full_path_file, destination_final_name))
                if exists(destination_final_name):
                    print_success("--> Archivo({}): \"{}\" copiado exitosamente !".format(line_number,filename_to_search[0]))
                    total_copied_files += 1
                else:
                    print_error("--> Archivo({}): \"{}\" no se pudo copiar !".format(line_number,filename_to_search[0]))
                    total_files_not_copied =+ 1
            else:
                print_warning("--> Archivo({}): \"{}\" no fue encontrado en la carpeta de busqueda".format(line_number,filename_to_search[0]))
                total_files_not_match += 1
            line_number +=1
    
    print_standard("")
    print_success("-------------------Summary process-------------------")
    print_success("Total de archivos en la carpeta de busqueda: %s" % len(files_search_dir))
    print_success("Total de archivos a copiar: %s" % total_files_to_copy)
    print_success("Total de archivos copiados: %s" % total_copied_files)
    print_warning("Total de archivos que no se encuentran en la carpeta de busqueda: %s" % total_files_not_match)
    print_error("Total de archivos encontrados pero no copiados: %s" % total_files_not_copied)
    print_error("Total de archivos duplicados: %s" % total_duplicated_files)
    print_success("-----------------------------------------------------")
    print_standard("")

def main(argv):
   path_to_search = ''
   path_to_copy = ''
   try:
      opts, args = getopt.getopt(argv,"hs:o:",["pathsearch=","pathout="])
   except getopt.GetoptError:
      print('Usage: copiator.py -s <carpeta_a_buscar> -o <carpeta_a_copiar>')
      sys.exit(2)

   for opt, arg in opts:
      if opt == '-h':
         print('Usage: copiator.py -s <carpeta_a_buscar> -o <carpeta_a_copiar>')
         sys.exit()
      elif opt in ("-s", "--pathsearch"):
         path_to_search = arg
      elif opt in ("-o", "--pathout"):
         path_to_copy = arg

   print("Iniciando....")
   process_copy(path_to_search, path_to_copy)
   print_success("Proceso finalizado")

if __name__ == "__main__":
    main(sys.argv[1:])

