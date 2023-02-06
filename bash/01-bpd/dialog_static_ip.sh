#!/bin/bash

# Bash Script  for Dialog Static IP


CANCEL_DIALOG=1
ESC_DIALOG=255
HEIGHT=0
WIDTH=0

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


# Choose one Available Network Interface from the NICS Array

while true; do
        exec 3>&1
        selected_nic=$(dialog --title "NIC Selection" \
                                --menu "Select the desired NIC from the below List" $HEIGHT $WIDTH $WIDTH \
                                $(for nic in $nics; do echo $nic ">"; done) \
                                2>&1 1>&3)

        # Main Menu should be having OK or Quit
        # All Subsequent Menus should be having Back or Quit

        escape_and_cancel
  
        msg_box=$(echo "Pick IP Type from below List for $selected_nic")

        exec 3>&1

        # Before below ip_type, it has to show ip configuratino if it is static or dynamic also. next screen also has to show the same thing just for reference. BACK button 
        # has to be to previous menus and 

        ip_type=$(dialog --title "Select the Address Type" \
                        --menu "$msg_box" $HEIGHT $WIDTH $WIDTH \
                        "Static" ">" \
                        "DHCP" ">" \
                        2>&1 1>&3)

        escape_and_cancel

        existing_nic_config $selected_nic

        exec 3>&1

        msg_box=$(echo "The selected NIC $selected_nic has IP $ip and Subnet $mask configured already. Do you want to reconfigure?")

        decision=$(dialog --title "NIC Selection" \
                                --menu "$msg_box" $HEIGHT $WIDTH $WIDTH \
                                "Proceed" ">" \
                                "Quit" ">" \
                                2>&1 1>&3)

        escape_and_cancel


        # Decision Whether to Proceed or Quit (Reconfigure or Retain)

        if [ $decision == "Quit" ]; then
                exit
        else                            
                if [ "$ip_type" = "Static" ]; then    # Input IP Address if the IP Type is Static
                        exec 3>&1
                        ip_addr_1=$(dialog --title "IP Address" \
                                                --inputbox "Enter the IP ADDRESS for $selected_nic" $HEIGHT $WIDTH \
                                                2>&1 1>&3)
                        exec 3>&1               
                        nm=$(dialog --title "Subnet Mask" \
                                                --inputbox "Enter the NETMASK for $selected_nic" $HEIGHT $WIDTH \
                                                2>&1 1>&3)
                        exec 3>&1
                        gw=$(dialog --title "Input Gateway IP" \
                                                --inputbox "Enter the Default Gateway for $selected_nic" $HEIGHT $WIDTH \
                                                2>&1 1>&3)
                        exec 3>&1
                        dns_1=$(dialog --title "DNS Server" \
                                                --inputbox "Enter the DNS Server for $selected_nic" $HEIGHT $WIDTH \
                                                2>&1 1>&3)

                        # Preparing the Network Interace Configuration File

                        cat << EOF > /etc/systemd/network/$selected_nic.network
[Match]
Name=$selected_nic

[Network]
Address=$ip_addr_1/$nm
Gateway=$gw
DNS=$dns_1
EOF
                        
                        # Disabling and Stopping DHCPCD Service

                        systemctl disable --now dhcpcd.service
                
                        # Enabling and Starting Network Manager Service

                        systemctl enable --now systemd-networkd.service


                # Configuring Selected NIC as DHCP

                elif [ "$ip_type" = "DHCP" ]; then
                        ip addr flush dev $selected_nic
                        rm -f /etc/systemd/network/$selected_nic*
                        systemctl disable --now systemd-networkd.service
                        systemctl enable --now dhcpcd.service         
                fi
        fi
done