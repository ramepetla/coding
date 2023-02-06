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



# Function to View the File Contents via Dialog

function view_file_contents() {
    dialog --textbox "$1" 0 0
}


# Function to Create File using Dialog

function file_creation (){
    local f="$1"
    local m="$0: file $f failed to create."
    if [ -f $f ] 
    then
        m="$0: $f file already exists."
    else
        /bin/touch $FILE && m="$0: $f file created."
    fi 
    dialog --title "Create file" --clear --msgbox "$m" 10 50
}



# Function to Delete File using Dialog

function file_deletion (){
    local f="$1"
    local m="$0: file $f failed to delete."
    if [ -f $f ] 
    then
        /bin/rm $FILE && m="$0: $f file deleted."
    else
        m="$0: $f file does not exist."
    fi 
    dialog --title "Delete file" --clear --msgbox "$m" 10 50
}



# Function to Change Permissions of a File using Dialog

function file_permission (){
    local f="$1"                    
    local p="$2"
    local m="$0: file $f failed to change permissions."
    if [ -f $f ] 
    then
        /bin/chmod $PERM $FILE && m="$0: $f file permissions changed."
    else
        m="$0: $f is not a file."
    fi 
    dialog --title "Change file permissions" --clear --msgbox "$m" 10 50
}



# Script to Delete File using Dialog

function file_deletion (){
	local f="$1"
	local m="$0: file $f failed to delete."
	if [ -f $f ] 
	then
		/bin/rm $FILE && m="$0: $f file deleted."
        # Message Box for Confirmation on File Deletion
        dialog --title "File Deletion" --msgbox "$m" 10 50
	else
		m="$0: $f is not a file."
	fi 
	dialog --title "Remove file" --clear --msgbox "$m" 10 50
}



# Function to Create Symbolic Link with the Name Striped from Original File Name

function file_link (){
    local f="$1"
    local m="$0: file $f failed to create symbolic link."
    if [ -f $f ] 
    then
        FILE_NAME=$(basename $FILE)
        FILE_PATH=$(dirname $FILE)
        FILE_NAME_NO_EXT="${FILE_NAME%.*}"
        /bin/ln -f $FILE $FILE_PATH/$FILE_NAME_NO_EXT && m="$0: $f file symbolic link created."
    else
        m="$0: $f is not a file."
    fi 
    dialog --title "Create file symbolic link" --clear --msgbox "$m" 10 50
}


# Function for Multi Links

function multi_links () { 

   rm /tmp/file_name_extension

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
            files_found=()
            file_name=$(basename $file_path_found)
            # Print Only the File Extension
            file_name_extension="${file_name##*.}"

            # Write file_name_extension to a file if it does not contain string 'conf' and not exist in files_found Array

            if [[ $file_name_extension != *"conf"* ]] ; then
                echo $file_name_extension ">" >> /tmp/file_name_extension
            fi

        done


    # Remove Duplicate lines from the file /tmp/file_name_extension

    sort -u /tmp/file_name_extension > /tmp/file_name_extension.tmp && mv /tmp/file_name_extension.tmp /tmp/file_name_extension

    
    # Read the /tmp/file_name_extension file and display the contents in a Dialog Box

    file_name_extension=$(cat /tmp/file_name_extension)


    selected_operation=$(dialog --cancel-label "Quit" --title "File Operations" \
                        --menu "Select the desired Option from the below List" 15 50 10 \
                        $file_name_extension \
                        2>&1 1>&3)


    # Proceed with Below Code if selected_operation is not null

    files_found_with_criteria=($(find $working_directory -type f -name "*$selected_operation*"))
    for file_found in "${files_found_with_criteria[@]}"
    do
        file_name=$(basename $file_found)
        file_path=$(dirname $file_found)
        file_name_no_ext="${file_name%.*}"
        echo "$file_found $file_path/$file_name_no_ext" >> /tmp/log.log
        /bin/ln -f $file_found $file_path/$file_name_no_ext 
    done

    clear

}


# Funcation for Main Menu

main_menu () {
    selected_operation=$(dialog --cancel-label "Quit" --title "File Operations" \
                            --menu "Select the desired Option from the below List" 100 100 10 \
                            "A" "File Creation" \
                            "B" "File Deletion" \
                            "C" "File Permission Change" \
                            "D" "File Content View" \
                            "E" "File Link Creation" \
                            2>&1 1>&3)
    }




# Main Program Starts Here. As Soon as Srcript is Executed, the below code will be executed first. 

main_program () {

    while true; do
        
        exec 3>&1
        main_menu
        escape_and_cancel

        case $selected_operation in           
            "A") FILE=$(dialog --title "File Creation" --inputbox "Enter the File Name along with Path:" 8 60 3>&1 1>&2 2>&3 3>&-)
                file_creation $FILE
                ;;
            "B") FILE=$(dialog --title "File Deletion" --stdout --title "Choose a File to Delete" --fselect / 14 48)
                file_deletion $FILE
                ;;
            "C") FILE=$(dialog --title "File Permissions" --stdout --title "Choose a File to Change Permissions" --fselect / 14 48)
                PERM=$(dialog --title "File Permissions" --inputbox "Enter the Permissions in Octal Format:" 8 60 3>&1 1>&2 2>&3 3>&-)
                file_permission $FILE $PERM
                ;;
            "D") FILE=$(dialog --title "Contents of File" --stdout --title "Choose a File to View" --fselect / 14 48)
                view_file_contents $FILE
                ;;
            "E") FILE=$(dialog --title "File Deletion" --stdout --title "Choose a File to Create Hard Link" --fselect / 14 48)
                file_link $FILE
                ;;
            "F") break;;
        esac
    done

}