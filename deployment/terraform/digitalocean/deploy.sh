#! /bin/bash

# Check if token file exists, otherwise prompt for token
if [ -f .terraform.do.token ]; then
    do_token=$(cat .terraform.do.token)
else
    read -p "Enter your DigitalOcean API token: " do_token
    echo "$do_token" > .terraform.do.token
fi

# Check if project name file exists, otherwise prompt for project name
if [ -f .terraform.do.project ]; then
    project_name=$(cat .terraform.do.project)
else
    read -p "Enter the name of the project: " project_name
    echo "$project_name" > .terraform.do.project
fi

# Ask if user would like to upgrade terraform
read -p "Would you like to upgrade terraform? (y/n): " upgrade
if [[ $upgrade == "y" ]]; then
    terraform init --upgrade
fi

# Confirm deployment
read -p "Are you sure you want to deploy? (y/n): " confirm
if [[ $confirm == "y" ]]; then
    terraform apply -var="do_token=$do_token" -var="project_name=$project_name"
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
    # echo -e "\naiuser password:"
    # terraform output -raw aiuser_password
    # echo -e ""
fi

echo -e ""
echo -e "################################################################################"
echo "Login to the server"
echo "################################################################################"
echo -e "ssh serveradmin@$(terraform output -raw droplet_ip)"
echo -e "ssh aiuser@$(terraform output -raw droplet_ip)"
