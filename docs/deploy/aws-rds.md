# Setting up AWS RDS Database

This guide will walk you through setting up a PostgreSQL database using Amazon RDS.

## Prerequisites

- AWS Account with appropriate permissions
- AWS CLI installed (optional)
- Basic understanding of AWS services

## Creating an RDS Instance

1. Navigate to the RDS Dashboard:
   - Log into AWS Console
   - Search for "RDS" or find it under Services

2. Create a new database:
   - Click "Create database"
   - Choose "Standard create"
   - Select PostgreSQL as the engine type

3. Configure basic settings:
   ```
   Instance configuration:
   - DB instance identifier: your-app-db
   - Master username: postgres (or your preferred username)
   - Master password: (create a strong password)

   Instance specifications:
   - DB instance class: db.t3.micro (for development)
   - Storage: 20 GB (minimum)
   ```

4. Configure network settings:
   ```
   Network settings:
   - VPC: Choose your VPC
   - Public access: Yes (for development only)
   - VPC security group: Create new or select existing
   ```

5. Configure security group:
   - Create a new security group or modify existing
   - Add inbound rule for PostgreSQL (port 5432)
   - Limit source IP to your application's IP

## Connection Information

After your RDS instance is created, you'll need these details for your application: 

```
Host: your-db-instance.xxxxx.region.rds.amazonaws.com
Port: 5432
Database: postgres (or your database name)
Username: (your master username)
Password: (your master password)
```

## Security Considerations

- Never commit database credentials to version control
- Use environment variables for sensitive information
- In production:
  - Disable public access
  - Use AWS Secrets Manager for credentials
  - Implement proper VPC and security group rules

## Connection String Format

For most applications, your connection string will look like this:

```
postgresql://username:password@your-db-instance.xxxxx.region.rds.amazonaws.com:5432/database_name
```

## Cost Considerations

- RDS instances incur charges even when idle
- Consider stopping instances when not in use
- Monitor usage and costs regularly
- Use reserved instances for production workloads

## Best Practices

1. Regular backups (automated by RDS)
2. Monitor performance metrics
3. Use parameter groups for database configuration
4. Implement proper security measures
5. Use Multi-AZ deployment for production

## Cleanup

To avoid unnecessary charges:
1. Take final backup if needed
2. Delete the RDS instance
3. Delete associated security groups
4. Remove unused subnet groups