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
variable "host_name" {}
variable "region" {}
variable "size" {}
variable "anthropic_api_key" {}
variable "openai_api_key" {}
variable "slack_bot_token" {}
variable "slack_app_token" {}
variable "app_tag" {}

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
  image  = "ubuntu-24-04-x64"
  name   = var.host_name
  region = var.region
  size   = var.size
  user_data = <<-EOF
            #!/bin/bash

            # Set environment variables
            ADMIN_USER="serveradmin"
            ADMIN_PASSWORD="${random_password.serveradmin_password.result}"
            AI_USER="aiuser"
            AI_PASSWORD="${random_password.aiuser_password.result}"
            APP_TAG="${var.app_tag}"
            ANTHROPIC_API_KEY="${var.anthropic_api_key}"
            OPENAI_API_KEY="${var.openai_api_key}"
            SLACK_BOT_TOKEN="${var.slack_bot_token}"
            SLACK_APP_TOKEN="${var.slack_app_token}"
            SLACK_AGENT_IMAGE_NAME="ryaneggz/slack-agent:latest"

            # Create serveradmin user with sudo access
            useradd -m -s /bin/bash $ADMIN_USER
            echo "$ADMIN_USER:$ADMIN_PASSWORD" | chpasswd
            usermod -aG sudo $ADMIN_USER

            # Create aiuser user
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

            # Clone the repository
            cd /home/$AI_USER
            git clone https://github.com/ryaneggz/langgraph-template agent_api
            cd agent_api
            
            # Create .env file
            cat > /home/$AI_USER/agent_api/.env << EOL
            OPENAI_API_KEY=$OPENAI_API_KEY
            ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY
            POSTGRES_CONNECTION_STRING="postgresql://admin:test1234@localhost:5432/lg_template_dev?sslmode=disable"
            EOL

            # Create .env.slack file
            cat > /home/$AI_USER/agent_api/.env.slack << EOL
            SLACK_BOT_TOKEN=$SLACK_BOT_TOKEN
            SLACK_APP_TOKEN=$SLACK_APP_TOKEN
            BASE_API_URL=http://localhost:8000
            EOL

            # Set up Database
            docker compose up -d

            # Start the agent API
            git fetch --all --tags
            git checkout $APP_TAG -f 
            
            echo 'Checking for existing agent_api sessions...'
            tmux ls 2>/dev/null | grep '^agent_api' | cut -d: -f1 | xargs -I{} tmux kill-session -t {} || echo 'No existing agent_api sessions found'

            # Create new tmux session with version in name
            SESSION_NAME="agent_api_$APP_TAG"
            tmux new-session -d -s "$SESSION_NAME" '
                source .venv/bin/activate
                uv pip install -r requirements.txt
                python main.py
            '
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