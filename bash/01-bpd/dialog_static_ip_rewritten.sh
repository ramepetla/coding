#!/bin/bash

# Bash Script  for Dialog Static IP


<<'COMMENT'

To Add Customize Dialog with configuration file, dialog --create-rc ~/.dialogrc

For a given dialog process, you can select a specific configuration file using the environment variable DIALOGRC


COMMENT


CANCEL_DIALOG=1
ESC_DIALOG=255
HEIGHT=0
WIDTH=0
DIALOGRC=~/.dialogrc

nics=$(ip link | grep -oP '(?<=: ).*(?=:)' | grep -vw lo)


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


# Function for Checking Selected NIC Existing Configuration and Return Result

existing_nic_config () {
  ip=$(ip addr show $1 | grep -w inet | awk '{print $2}' | cut -d '/' -f1)
  mask=$(ip addr show $1 | grep -w inet | awk '{print $2}' | cut -d '/' -f2)
  
}


# Fucntion for Main Menu

main_menu () {
    selected_nic=$(dialog --cancel-label "Quit" --title "NIC Selection" \
                            --menu "Select the desired NIC from the below List" $HEIGHT $WIDTH $WIDTH \
                            $(for nic in $nics; do echo $nic ">"; done) \
                            2>&1 1>&3)
}


# Function for Static or DHCP

static_or_dhcp () {
    exec 3>&1
    msg_box=$(echo "Pick IP Type from below List for $selected_nic")
    ip_type=$(dialog --cancel-label "Menu" --title "IP Type Selection" \
                        --menu "$msg_box" $HEIGHT $WIDTH $WIDTH \
                        "Static" ">" \
                        "DHCP" ">" \
                        2>&1 1>&3)

    if [ "$ip_type" == "Static" ]; then    # Input IP Address if the IP Type is Static
            exec 3>&1
            ip_addr_1=$(dialog --title "Existing IP: $ip" \
                                    --inputbox "Enter the IP ADDRESS for $selected_nic" $HEIGHT $WIDTH \
                                    2>&1 1>&3)
            exec 3>&1               
            nm=$(dialog --title "Existing Mask: $ip" \
                                    --inputbox "Enter the NETMASK for $selected_nic" $HEIGHT $WIDTH \
                                    2>&1 1>&3)
            exec 3>&1
            gw=$(dialog --title " " \
                                    --inputbox "Enter the Default Gateway for $selected_nic" $HEIGHT $WIDTH \
                                    2>&1 1>&3)
            exec 3>&1
            dns_1=$(dialog --title " " \
                                    --inputbox "Enter the DNS Server for $selected_nic" $HEIGHT $WIDTH \
                                    2>&1 1>&3)

            cat << EOF > /etc/systemd/network/$selected_nic.network
[Match]
Name=$selected_nic

[Network]
Address=$ip_addr_1/$nm
Gateway=$gw
DNS=$dns_1
EOF

            # Disabling and Stopping DHCPCD Service, Enabling and Starting Network Manager Service

            systemctl disable --now dhcpcd.service
            systemctl enable --now systemd-networkd.service

            # Dialog for Displaying File Content

            exec 3>&1
            sleep 10
            dialog --title "Configured Paramenters on $selected_nic" \
                    --textbox /etc/systemd/network/$selected_nic.network $HEIGHT $WIDTH \
                    2>&1 1>&3   
    
    # Configuring Selected NIC as DHCP

    elif [ "$ip_type" == "DHCP" ]; then
            ip addr flush dev $selected_nic
            rm -f /etc/systemd/network/$selected_nic*
            systemctl disable --now systemd-networkd.service
            systemctl enable --now dhcpcd.service  

            sleep 10
            existing_nic_config $selected_nic
            dialog --title "Configured Paramenters on $selected_nic" \
                    --msgbox "IP Address: $ip \
                              Subnet Mask: $mask \
                              Gateway: $gw \
                              DNS: $dns_1" $HEIGHT $WIDTH \
                              2>&1 1>&3
  fi
}


static_ip () {
    exec 3>&1
    msg_box=$(echo "Enter Static IP for $selected_nic")
    static_ip=$(dialog --title "Static IP" \
                        --inputbox "$msg_box" $HEIGHT $WIDTH \
                        2>&1 1>&3)
}


while true; do

    exec 3>&1
    main_menu
    escape_and_cancel

    existing_nic_config $selected_nic
    exec 3>&1

    # If Existing IP Found, Display it in the Menu

    if [ -n "$ip" ]; then
        msg_box=$(echo "Selected NIC $selected_nic has $ip and subnet mask $mask already Configured")
        decision=$(dialog --cancel-label "Menu" --title "Existing Configuration Found" \
                                  --menu "$msg_box" $HEIGHT $WIDTH $WIDTH \
                                      "Proceed" ">" \
                                      "Back" ">" \
                                      2>&1 1>&3)
        case $decision in
            "Proceed")
                static_or_dhcp
                escape_and_cancel
                ;;
            "Main Menu")
                main_menu
                ;;
        esac

    else
        static_or_dhcp
    fi

done



