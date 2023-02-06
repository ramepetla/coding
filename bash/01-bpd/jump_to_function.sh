#!/bin/bash


CANCEL_DIALOG=1
ESC_DIALOG=255
HEIGHT=0
WIDTH=0


file_ext=".config"
working_directory="/home/linadmin/configuration.switch/12-Mantech.network.d"


# Function for Cancel and Escape

escape_and_cancel () {
  exit_status=$?
  exec 3>&-
  case $exit_status in
    $CANCEL_DIALOG)
      clear
      echo "USER TERMINATED"
      exit
      ;;
    $ESC_DIALOG)
      clear
      echo "USER ABORTED" >&2
      exit 1
      ;;
  esac
}



# Function for Multi Links

function multi_links () { 

    # Calling this Function from Command Line: /home/linadmin/links/bpd/jump_to_function.sh multi_links ".config" "/home/linadmin/configuration.switch/12-Mantech.network.d"

    # Variables for Arguments

    file_ext=$1
    working_directory=$2

    exec 3>&1
    
    selected_operation=$(dialog --cancel-label "Quit" --title "File Operations" \
                        --menu "Select the desired Option from the below List" 15 50 10 \
                        "mantech" ">" \
                        "traffic" ">" \
                        "customer" ">" \
                        "bootstrap" ">" \
                        "core" ">" \
                        2>&1 1>&3)

    files_found_with_criteria=($(find $working_directory -type f -name "*$selected_operation*"))
    for file_found in "${files_found_with_criteria[@]}"
    do
        file_name=$(basename $file_found)
        file_path=$(dirname $file_found)
        file_name_no_ext="${file_name%.*}"
        /bin/ln -f $file_found $file_path/$file_name_no_ext 
    done    

}

multi_links