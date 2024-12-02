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
variable "app_username" {}
variable "app_password" {}

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
            APP_USERNAME="${var.app_username}"
            APP_PASSWORD="${var.app_password}"
            ANTHROPIC_API_KEY="${var.anthropic_api_key}"
            HOST_IP=$(hostname -I | awk '{print $1}')
            OPENAI_API_KEY="${var.openai_api_key}"
            SLACK_BOT_TOKEN="${var.slack_bot_token}"
            SLACK_APP_TOKEN="${var.slack_app_token}"
            SLACK_AGENT_IMAGE_NAME="ryaneggz/slack-agent:latest"

            # Create log file
            SETUP_LOG="/home/$AI_USER/done/setup.log"
            touch $SETUP_LOG
            exec 1> >(tee -a "$SETUP_LOG")
            exec 2> >(tee -a "$SETUP_LOG" >&2)

            echo "Starting setup at $(date)" >> $SETUP_LOG
            echo "AI_USER: $AI_USER" >> $SETUP_LOG

            # Create serveradmin user with sudo access
            useradd -m -s /bin/bash $ADMIN_USER || echo "Error creating admin user" >> $SETUP_LOG
            echo "$ADMIN_USER:$ADMIN_PASSWORD" | chpasswd
            usermod -aG sudo $ADMIN_USER || echo "Error adding admin to sudo group" >> $SETUP_LOG

            # Create aiuser user
            useradd -m -s /bin/bash $AI_USER || echo "Error creating AI user" >> $SETUP_LOG
            echo "$AI_USER:$AI_PASSWORD" | chpasswd
            # usermod -aG sudo $AI_USER

            # Install Docker
            apt-get update || echo "Error updating apt" >> $SETUP_LOG
            apt-get install -y apt-transport-https ca-certificates curl software-properties-common python3-pip python3-venv pipx tmux || echo "Error installing prerequisites" >> $SETUP_LOG
            curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add - || echo "Error adding Docker GPG key" >> $SETUP_LOG
            add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" || echo "Error adding Docker repository" >> $SETUP_LOG
            apt-get update || echo "Error updating apt after Docker repo add" >> $SETUP_LOG
            apt-get install -y docker-ce || echo "Error installing Docker" >> $SETUP_LOG
            usermod -aG docker $ADMIN_USER || echo "Error adding admin to docker group" >> $SETUP_LOG
            usermod -aG docker $AI_USER || echo "Error adding AI user to docker group" >> $SETUP_LOG
    
            # Install Docker Compose
            curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose || echo "Error downloading Docker Compose" >> $SETUP_LOG
            chmod +x /usr/local/bin/docker-compose || echo "Error setting Docker Compose permissions" >> $SETUP_LOG

            # Install GitHub CLI
            type -p curl >/dev/null || apt install curl -y
            curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg || echo "Error downloading GitHub CLI key" >> $SETUP_LOG
            sudo chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg || echo "Error setting GitHub CLI key permissions" >> $SETUP_LOG
            echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null || echo "Error adding GitHub CLI repo" >> $SETUP_LOG
            sudo apt update || echo "Error updating apt after GitHub CLI repo add" >> $SETUP_LOG
            sudo apt install gh -y || echo "Error installing GitHub CLI" >> $SETUP_LOG

            # Clone the repository
            cd /home/$AI_USER || echo "Error changing to AI user home directory" >> $SETUP_LOG
            sudo -u $AI_USER git clone https://github.com/ryaneggz/langgraph-template agent_api || echo "Error cloning repository" >> $SETUP_LOG
            cd agent_api || echo "Error changing to agent_api directory" >> $SETUP_LOG
            
            # Create .env file
            cat > /home/$AI_USER/agent_api/.env << EOL || echo "Error creating .env file" >> $SETUP_LOG
            OPENAI_API_KEY=$OPENAI_API_KEY
            ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY
            POSTGRES_CONNECTION_STRING="postgresql://admin:test1234@localhost:5432/lg_template_dev?sslmode=disable"
            EOL

            # Create .env.slack file
            cat > /home/$AI_USER/agent_api/.env.slack << EOL || echo "Error creating .env.slack file" >> $SETUP_LOG
            SLACK_BOT_TOKEN=$SLACK_BOT_TOKEN
            SLACK_APP_TOKEN=$SLACK_APP_TOKEN
            BASE_API_URL=http://localhost:8000
            EOL

            # Set up Database
            docker compose up -d || echo "Error starting Docker containers" >> $SETUP_LOG

            # Start the agent API
            sudo -u $AI_USER git fetch --all --tags
            sudo -u $AI_USER git checkout $APP_TAG -f 
            
            echo 'Checking for existing agent_api sessions...' >> $SETUP_LOG
            sudo -u $AI_USER tmux ls 2>/dev/null | grep '^agent_api' | cut -d: -f1 | xargs -I{} tmux kill-session -t {} || echo 'No existing agent_api sessions found' >> $SETUP_LOG

            # Ownership of home directory
            chown -R $AI_USER:$AI_USER /home/$AI_USER

            ## Install uv
            # sudo -u $AI_USER pipx install uv || echo "Error installing uv" >> $SETUP_LOG
            # sudo -u $AI_USER tmux new-session -d -s "agent_api" -c "/home/$AI_USER/agent_api" "uv venv && source .venv/bin/activate && uv pip install -r requirements.txt && python3 main.py"

            sudo -u $AI_USER tmux new-session -d -s "agent_api" '
                python3 -m venv .venv
                source .venv/bin/activate
                pip install -r requirements.txt
                python main.py
            '

            # Create done directory and html file
            sudo -u $AI_USER mkdir -p /home/$AI_USER/done || echo "Error creating done directory" >> $SETUP_LOG
            sudo -u $AI_USER cat > /home/$AI_USER/done/index.html << EOL || echo "Error creating index.html" >> $SETUP_LOG
            <!DOCTYPE html>
            <html>
            <head>
                <title>Setup Complete</title>
                <style>
                    body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
                    .info-box { background: #f5f5f5; padding: 15px; border-radius: 5px; margin: 10px 0; }
                </style>
            </head>
            <body>
                <h1>Setup Completed Successfully!</h1>
                <div class="info-box">
                    <h2>Deployment Information</h2>
                    <ul>
                        <li>Setup Completed: $(date)</li>
                        <li>Hostname: ${var.host_name}</li>
                        <li>Region: ${var.region}</li>
                        <li>Droplet Size: ${var.size}</li>
                        <li>Project: ${var.project_name}</li>
                        <li>App Version: ${var.app_tag}</li>
                    </ul>
                </div>
                <div class="info-box">
                    <h2>Services Status</h2>
                    <ul>
                        <li>Agent API: Running on port <a href="http://$HOST_IP:8000">http://$HOST_IP:8000</a></li>
                        <li>Database: Running on port <a href="http://$HOST_IP:4040">http://$HOST_IP:4040</a></li>
                        <li>Status Page: Running on port <a href="http://$HOST_IP:8080">http://$HOST_IP:8080</a></li>
                    </ul>
                </div>
                <div class="info-box">
                    <h2>Next Steps</h2>
                    <ul>
                        <li>Check the setup logs at: <a href="http://$HOST_IP:8080/setup.log">http://$HOST_IP:8080/setup.log</a></li>
                        <li>Monitor the API using: tmux attach -t agent_api</li>
                        <li>View Docker containers: docker ps</li>
                    </ul>
                </div>
            </body>
            </html>
            EOL

            # Start Python HTTP server in tmux
            sudo -u $AI_USER tmux new-session -d -s "done_server" "cd /home/$AI_USER/done && python3 -m http.server 8080"

            echo "Setup completed at $(date)" >> $SETUP_LOG
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