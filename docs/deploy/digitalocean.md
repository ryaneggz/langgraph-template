# Deploying to DigitalOcean

This guide walks you through deploying the application to DigitalOcean using Terraform.

## Prerequisites

1. [Install Terraform](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli)
2. Get your DigitalOcean API token
   - Go to [DigitalOcean Cloud Control Panel](https://cloud.digitalocean.com)
   - Navigate to API → Generate New Token
   - Create a token with both read and write access

3. Create Slack App
   - Go to [Slack API Apps page](https://api.slack.com/apps)
   - Click "Create New App" and choose "From scratch"
   - Name your app and select your workspace
   - Under "OAuth & Permissions":
     - Add Bot Token Scopes:
       - `app_mentions:read`
       - `chat:write`
       - `im:history` 
       - `im:read`
       - `im:write`
   - Under "Socket Mode":
     - Enable Socket Mode
     - Generate and save your App-Level Token
   - Install the app to your workspace
   - Save both the Bot User OAuth Token and App-Level Token for deployment

4. Gather required API keys:
   - Anthropic API key
   - OpenAI API key
   - Slack Bot Token
   - Slack App Token

## Deployment Steps

1. Navigate to the terraform directory:
   ```bash
   cd deployment/terraform/digitalocean
   ```

2. Run the deployment script:
   ```bash
   bash ./deploy.sh
   ```

3. The script will prompt you for:
   - DigitalOcean API token
   - Project name
   - Region selection
   - Droplet size
   - API keys (Anthropic, OpenAI)
   - Slack tokens
   - App version tag
   - App credentials

4. Review the deployment plan and confirm to proceed

5. After deployment completes, the script will:
   - Save server passwords to `.terraform.serveradmin_password` and `.terraform.aiuser_password`
   - Display SSH connection commands
   - Show the status page URL

## Accessing Your Deployment

- **Status Page**: `http://<droplet-ip>:8080`
- **API Endpoint**: `http://<droplet-ip>:8000`
- **Database Admin**: `http://<droplet-ip>:4040`

### SSH Access

```bash
## Admin Access
ssh aiuser@<droplet-ip>
```

## Monitoring

1. Connect to the server via SSH
2. View application logs:
   ```bash
   tmux attach -t agent_api
   ```
   (Use `Ctrl+B, D` to detach from tmux)

3. View Docker containers:
   ```bash
   docker ps
   ```

## Configuration Storage

Your deployment configuration is saved in `.terraform.config.json` for future deployments. This includes:
- Region selection
- Droplet size
- API keys
- Project settings

**Note**: Keep your `.terraform.config.json` and password files secure as they contain sensitive information.