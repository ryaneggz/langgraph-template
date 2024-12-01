#! /bin/bash

# Ask if they'd like to preview the changes OR destroy the resources
read -p "Would you like to preview the changes or destroy the resources? (preview/destroy): " confirm
if [[ $confirm == "preview" ]]; then
    terraform plan -destroy
fi

if [[ $confirm == "destroy" ]]; then
    terraform destroy
fi

# Ask if they'd like to delete the token and project
read -p "Would you like to delete the token and project? (y/n): " confirm
if [[ $confirm == "y" ]]; then
    rm .terraform.config.json
fi
