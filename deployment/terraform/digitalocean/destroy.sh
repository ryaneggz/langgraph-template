#! /bin/bash

# Ask if they'd like to preview the changes OR destroy the resources
read -p "Would you like to preview the changes or destroy the resources? (preview/destroy): " confirm
if [[ $confirm == "preview" ]]; then
    terraform plan -destroy
fi
if [[ $confirm == "destroy" ]]; then
    terraform destroy
    rm .terraform.do.token
    rm .terraform.do.project
fi