terraform {
  required_providers {
    digitalocean = {
      source = "digitalocean/digitalocean"
      version = "~> 2.0"
    }
    random = {
      source = "hashicorp/random"
      version = "~> 3.0"
    }
  }
}

variable "do_token" {}
variable "project_name" {}

provider "digitalocean" {
  token = var.do_token
}

data "digitalocean_project" "project" {
  name = var.project_name
}

resource "random_password" "serveradmin_password" {
  length           = 32
  special          = false
}

resource "random_password" "aiuser_password" {
  length           = 32
  special          = false
}

// https://www.perplexity.ai/search/terraform-ubuntu-template-digi-Vuo6tX2iRreg_yx.ESWjvg
resource "digitalocean_droplet" "web" {
  image  = "ubuntu-20-04-x64"
  name   = "slack-agent-B"
  region = "nyc3"
  size   = "s-1vcpu-1gb"
  user_data = <<-EOF
            #!/bin/bash

            # Create serveradmin user with sudo access
            ADMIN_USER="serveradmin"
            ADMIN_PASSWORD="${random_password.serveradmin_password.result}"
            useradd -m -s /bin/bash $ADMIN_USER
            echo "$ADMIN_USER:$ADMIN_PASSWORD" | chpasswd
            usermod -aG sudo $ADMIN_USER

            # Create aiuser user
            AI_USER="aiuser"
            AI_PASSWORD="${random_password.aiuser_password.result}"
            useradd -m -s /bin/bash $AI_USER
            echo "$AI_USER:$AI_PASSWORD" | chpasswd
            # usermod -aG sudo $AI_USER

            # Install Docker
            apt-get update
            apt-get install -y apt-transport-https ca-certificates curl software-properties-common
            curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
            add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
            apt-get update
            apt-get install -y docker-ce
            usermod -aG docker $ADMIN_USER
            usermod -aG docker $AI_USER
    
            # Install Docker Compose
            curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
            chmod +x /usr/local/bin/docker-compose

            # Install GitHub CLI
            type -p curl >/dev/null || apt install curl -y
            curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg \
            && sudo chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg \
            && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null \
            && sudo apt update \
            && sudo apt install gh -y
            EOF
}

resource "digitalocean_project_resources" "project_resources" {
  project = data.digitalocean_project.project.id
  resources = [
    digitalocean_droplet.web.urn
  ]
}

output "droplet_ip" {
  value = digitalocean_droplet.web.ipv4_address
}

output "serveradmin_password" {
  value = random_password.serveradmin_password.result
  sensitive = true
}

output "aiuser_password" {
  value = random_password.aiuser_password.result
  sensitive = true
}