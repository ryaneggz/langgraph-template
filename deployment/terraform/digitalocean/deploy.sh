#! /bin/bash

# Check if config file exists, otherwise create it
if [ -f .terraform.config.json ]; then
    # Read values from config file
    do_token=$(jq -r '.do_token' .terraform.config.json)
    project_name=$(jq -r '.project_name' .terraform.config.json)
    region=$(jq -r '.region' .terraform.config.json)
    size=$(jq -r '.size' .terraform.config.json)
fi

# Prompt for token if null or empty
if [ "$do_token" = "null" ] || [ -z "$do_token" ]; then
    read -p "Enter your DigitalOcean API token: " do_token
fi

# Prompt for project name if null or empty  
if [ "$project_name" = "null" ] || [ -z "$project_name" ]; then
    read -p "Enter the name of the project: " project_name
fi

# Prompt for region if null or empty
if [ "$region" = "null" ] || [ -z "$region" ]; then
    echo "Available regions:"
    echo "1) NYC1 - New York City, United States"
    echo "2) NYC3 - New York City, United States" 
    echo "3) SFO3 - San Francisco, United States"
    read -p "Select region (1-3): " region_choice
    case $region_choice in
        1) region="nyc1";;
        2) region="nyc3";;
        3) region="sfo3";;
        *) echo "Invalid choice, defaulting to nyc3"; region="nyc3";;
    esac
fi

# Prompt for size if null or empty
if [ "$size" = "null" ] || [ -z "$size" ]; then
    echo "Available sizes:"
    echo "1) s-1vcpu-1gb - 1GB RAM, 1 vCPU"
    echo "2) s-1vcpu-2gb - 2GB RAM, 1 vCPU"
    echo "3) s-2vcpu-2gb - 2GB RAM, 2 vCPU"
    read -p "Select size (1-3): " size_choice
    case $size_choice in
        1) size="s-1vcpu-1gb";;
        2) size="s-1vcpu-2gb";;
        3) size="s-2vcpu-2gb";;
        *) echo "Invalid choice, defaulting to s-1vcpu-1gb"; size="s-1vcpu-1gb";;
    esac
fi

# Create/update config file
cat > .terraform.config.json << EOF
{
    "do_token": "$do_token",
    "project_name": "$project_name",
    "region": "$region",
    "size": "$size"
}
EOF

# Ask if user would like to upgrade terraform
read -p "Would you like to upgrade terraform? (y/n): " upgrade
if [[ $upgrade == "y" ]]; then
    terraform init --upgrade
fi

# Confirm deployment
read -p "Are you sure you want to deploy? (y/n): " confirm
if [[ $confirm == "y" ]]; then
    terraform apply -var="do_token=$do_token" -var="project_name=$project_name" -var="region=$region" -var="size=$size"
fi

echo -e ""
echo -e "################################################################################"
echo "Outputting passwords"
echo "################################################################################"
# Confirm output
read -p "Would you like to output the passwords? (y/n): " confirm
if [[ $confirm == "y" ]]; then
    echo -e "\nserveradmin password:"
    terraform output -raw serveradmin_password
    echo -e ""
    echo -e "\naiuser password:"
    terraform output -raw aiuser_password
    echo -e ""
fi

echo -e ""
echo -e "################################################################################"
echo "Login to the server"
echo "################################################################################"
echo -e "ssh serveradmin@$(terraform output -raw droplet_ip)"
echo -e "ssh aiuser@$(terraform output -raw droplet_ip)"
