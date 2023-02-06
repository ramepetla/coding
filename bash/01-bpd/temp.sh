selected_nic=(dialog --title "Select NIC" \
--menu "Select the desired NIC from the below List" $HEIGHT $WIDTH $WIDTH \
$(for nic in $nics; do echo ">" $nic; done))




  exit_status=$?
  exec 3>&-
  case $exit_status in
    $DIALOG_CANCEL)
      clear
      echo "Program terminated."
      exit
      ;;
    $DIALOG_ESC)
      clear
      echo "Program aborted." >&2
      exit 1
      ;;
  esac


   # Get the IP Address of the Selected NIC

  ip_address=$(ip addr show $selected_nic | grep -oP '(?<=inet ).*(?=/)')

  # Get the Subnet Mask of the Selected NIC

  subnet_mask=$(ip addr show $selected_nic | grep -oP '(?<=inet ).*(?=/)' | cut -d '.' -f 1-3).0/24

  # Get the Default Gateway of the Selected NIC

  default_gateway=$(ip route show | grep -oP '(?<=default via ).*(?= dev)')

  # Get the DNS Server of the Selected NIC

  dns_server=$(cat /etc/resolv.conf | grep -oP '(?<=nameserver ).*')

  # Display the IP Address of the Selected NIC

  result="IP Address: $ip_address"
  display_result "IP Address"

  # Display the Subnet Mask of the Selected NIC

  result="Subnet Mask: $subnet_mask"
  display_result "Subnet Mask"

  # Display the Default Gateway of the Selected NIC

  result="Default Gateway: $default_gateway"
  display_result "Default Gateway"

  # Display the DNS Server of the Selected NIC

  result="DNS Server: $dns_server"
  display_result "DNS Server"



  DIALOG_CANCEL=1
DIALOG_ESC=255
HEIGHT=0
WIDTH=0


