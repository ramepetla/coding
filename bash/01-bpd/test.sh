#!/bin/bash

#!/bin/bash


CANCEL_DIALOG=1
ESC_DIALOG=255
HEIGHT=0
WIDTH=0


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

    echo > /tmp/file_name_extension

    # Calling this Function from Command Line: source /home/linadmin/links/bpd/test.sh ; multi_links ".conf" "/home/linadmin/configuration.switch/12-Mantech.network.d"

    # Variables for Arguments

    file_ext=$1
    working_directory=$2

    exec 3>&1

    # Add Files found in in $working_directory to an Array

    files_path_found=($(find $working_directory -type f -name "*$file_ext*"))

    # Add the filenames to an Array if it contains $file_ext

    for file_path_found in "${files_path_found[@]}"
        do
            file_name=$(basename $file_path_found)
            # Print Only the File Extension
            file_name_extension="${file_name##*.}"

            # Write file_name_extension to a file if it does not contain string 'conf'
            if [[ $file_name_extension != *"conf"* ]]; then
                echo $file_name_extension ">" >> /tmp/file_name_extension
            fi
        done

    # Read the /tmp/file_name_extension file and display the contents in a Dialog Box

    file_name_extension=$(cat /tmp/file_name_extension)


    selected_operation=$(dialog --cancel-label "Quit" --title "File Operations" \
                        --menu "Select the desired Option from the below List" 15 50 10 \
                        $file_name_extension \
                        2>&1 1>&3)


    files_found_with_criteria=($(find $working_directory -type f -name "*$selected_operation*"))
    for file_found in "${files_found_with_criteria[@]}"
    do
        file_name=$(basename $file_found)
        file_path=$(dirname $file_found)
        file_name_no_ext="${file_name%.*}"
        /bin/ln -f $file_found $file_path/$file_name_no_ext 
    done    

    clear

}