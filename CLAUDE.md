# CLAUDE.md

This file provides comprehensive guidance to Claude Code (claude.ai/code) when working with the Freqtrade GCP Deployment project.

# Freqtrade Multi-Bot GCP Deployment

## Project Overview

**GitHub Repository**: https://github.com/myownipgit/freqtrade-gcp-deployment
**Live Dashboards**:
- Multi-Bot Dashboard: http://35.185.177.130:5000
- FreqUI Interface: http://35.185.177.130:3000

This project deploys 12 independent Freqtrade trading bots to Google Cloud Platform with:
- Containerized deployment using Docker Compose
- Unified multi-bot dashboard for monitoring
- Individual bot management capabilities
- Automated health checks and monitoring
- Network isolation and security

## Architecture Summary

```
GCP VM Instance (freqtrade-cluster)
├── 12 Freqtrade Bot Containers (ports 8080-8091)
├── FreqUI Dashboard (port 3000)
├── Multi-Bot Dashboard (port 5000)
└── Health Monitoring & Management Scripts
```

## Project Structure

```
freqtrade-gcp-deployment/
├── configs/                    # Bot configurations
│   └── config-bot-XX.json      # Individual bot configs (01-12)
├── dashboard/                  # Multi-bot dashboard
│   ├── app/
│   │   ├── dashboard.py        # Flask backend
│   │   └── templates/
│   │       └── dashboard.html  # Frontend template
│   ├── Dockerfile              # Dashboard container
│   └── requirements.txt
├── docker/                     # Docker configurations
│   ├── docker-compose-with-ui.yml  # Main deployment file
│   ├── docker-compose.yml      # Basic deployment
│   └── strategies/             # Trading strategies
├── scripts/                    # Management and deployment
│   ├── manage_cluster.sh       # Primary management script
│   ├── health_check_cluster.sh # Health monitoring
│   ├── deploy_dashboard.sh     # Dashboard deployment
│   └── startup-script-*.sh     # VM startup scripts
├── monitoring/                 # Monitoring configurations
├── terraform/                  # Infrastructure as code
├── README.md                   # Project documentation
└── CLAUDE.md                   # This file
```

## Common Commands and Workflows

### Primary Management Script: `./scripts/manage_cluster.sh`

```bash
# Cluster-wide operations
./scripts/manage_cluster.sh start           # Start entire cluster
./scripts/manage_cluster.sh stop            # Stop entire cluster
./scripts/manage_cluster.sh restart         # Restart all containers
./scripts/manage_cluster.sh status          # Show status and URLs

# Individual bot management
./scripts/manage_cluster.sh start-bot 01    # Start specific bot
./scripts/manage_cluster.sh stop-bot 01     # Stop specific bot
./scripts/manage_cluster.sh restart-bot 01  # Restart specific bot

# Logging and debugging
./scripts/manage_cluster.sh logs all        # All container logs
./scripts/manage_cluster.sh logs 01         # Specific bot logs
./scripts/manage_cluster.sh logs dashboard  # Dashboard logs
./scripts/manage_cluster.sh logs ui         # FreqUI logs

# Dashboard management
./scripts/manage_cluster.sh dashboard-restart
./scripts/manage_cluster.sh dashboard-logs

# FreqUI management
./scripts/manage_cluster.sh ui-restart
./scripts/manage_cluster.sh ui-logs

# System access
./scripts/manage_cluster.sh ssh             # SSH into VM
```

### Health Monitoring: `./scripts/health_check_cluster.sh`

```bash
./scripts/health_check_cluster.sh
```

Checks:
- VM instance status
- All 12 bot API endpoints (ports 8080-8091)
- FreqUI dashboard (port 3000)
- Multi-bot dashboard (port 5000)
- Container health status

## GCP Configuration

### Environment Variables
```bash
export PROJECT_ID="analog-patrol-458417-b5"
export ZONE="asia-southeast1-a"
export REGION="asia-southeast1"
export VM_NAME="freqtrade-cluster"
```

### Network Infrastructure
- **VPC**: `freqtrade-network`
- **Subnet**: `freqtrade-subnet` (10.0.0.0/24)
- **Firewall Rules**: 
  - `freqtrade-api-access`: TCP 8080-8091,3000,5000,22
  - `freqtrade-dashboard-allow-5000`: TCP 5000

### VM Instance
- **Name**: `freqtrade-cluster`
- **Type**: `e2-standard-4`
- **OS**: Ubuntu 20.04 LTS
- **Disk**: 50GB
- **External IP**: 35.185.177.130

## Container Architecture

### Docker Compose Services (docker-compose-with-ui.yml)

1. **Freqtrade Bots (freqtrade-bot-01 to freqtrade-bot-12)**
   - Image: `freqtradeorg/freqtrade:stable`
   - Ports: 8080-8091 (mapped to host)
   - Config: Individual JSON files
   - Health checks: API ping endpoints

2. **FreqUI Dashboard (frequi)**
   - Image: `freqtradeorg/frequi:latest`
   - Port: 3000
   - Official Freqtrade web interface

3. **Multi-Bot Dashboard (dashboard)**
   - Custom Flask application
   - Port: 5000
   - Real-time monitoring of all bots

### Bot Configuration Structure

Each bot has a configuration file `configs/config-bot-XX.json`:

```json
{
  "max_open_trades": 3,
  "stake_currency": "USDT",
  "stake_amount": 100,
  "dry_run": true,
  "api_server": {
    "enabled": true,
    "listen_port": 8080,
    "username": "freqtrader",
    "password": "botXXpass"
  },
  "exchange": {
    "name": "binance"
  }
}
```

## Dashboard Implementation

### Multi-Bot Dashboard (`dashboard/app/dashboard.py`)

**Key Features**:
- Async data fetching from all 12 bots
- Real-time status monitoring
- Portfolio-wide analytics
- Auto-refresh every 10 seconds

**API Endpoints**:
- `/api/bots` - All bot statuses
- `/api/summary` - Portfolio summary
- `/api/bot/<bot_id>` - Individual bot data

**Status Detection Logic**:
```python
status='running' if status_data is not None else 'error'
```

## Development and Troubleshooting

### Common Issues and Solutions

1. **Dashboard Not Accessible**
   - Check firewall rules: Ensure dashboard port is allowed
   - Verify container status: `docker-compose ps`
   - Check VM external IP

2. **Bots Showing as Error**
   - API connectivity issues (rate limiting, auth)
   - Container startup problems
   - Configuration errors

3. **FreqUI Connection Issues**
   - Bot API server settings
   - Authentication configuration
   - Network connectivity

### Debugging Steps

1. **Check VM Status**:
   ```bash
   gcloud compute instances describe freqtrade-cluster --zone=asia-southeast1-a
   ```

2. **SSH and Check Containers**:
   ```bash
   ./scripts/manage_cluster.sh ssh
   cd /app/freqtrade-cluster
   sudo docker-compose ps
   sudo docker-compose logs <service_name>
   ```

3. **Test API Endpoints**:
   ```bash
   curl http://35.185.177.130:8080/api/v1/ping
   curl http://35.185.177.130:5000/api/summary
   ```

## Development Workflows

### Making Changes to Dashboard

1. Edit `dashboard/app/dashboard.py` or templates
2. Rebuild and redeploy:
   ```bash
   ./scripts/deploy_dashboard.sh
   ```
3. Monitor logs:
   ```bash
   ./scripts/manage_cluster.sh dashboard-logs
   ```

### Updating Bot Configurations

1. Edit configuration files in `configs/`
2. Upload to VM and restart:
   ```bash
   gcloud compute scp configs/config-bot-XX.json freqtrade-cluster:/app/freqtrade-cluster/configs/
   ./scripts/manage_cluster.sh restart-bot XX
   ```

### Adding New Bots

1. Create new configuration file
2. Add service to `docker-compose-with-ui.yml`
3. Update dashboard to include new bot
4. Redeploy cluster

## Security Considerations

- Network isolation with custom VPC
- Firewall rules restricting access
- Individual bot authentication
- Container isolation
- No root SSH access by default

## Backup and Recovery

Files to backup:
- All configuration files (`configs/`)
- Bot databases (`user_data/bot-XX/`)
- Trading logs
- Custom strategies

## Performance Monitoring

### Key Metrics to Monitor

- Bot API response times
- Container resource usage
- Trading performance
- Error rates
- Network connectivity

### Health Check Indicators

- ✅ All 12 bots responding on API
- ✅ Dashboard accessibility
- ✅ FreqUI functionality
- ✅ Container health status

## Claude Code Best Practices

### When Working on This Project

1. **Always use management scripts** instead of direct docker commands
2. **Check health status** before making changes
3. **Use SSH access** via management script for debugging
4. **Monitor logs** when troubleshooting issues
5. **Test changes** on individual bots before cluster-wide updates

### Common Tasks for Claude

1. **Status Checks**: Use health check script first
2. **Log Analysis**: Use management script log commands
3. **Configuration Updates**: Edit configs and restart specific bots
4. **Dashboard Changes**: Update dashboard code and redeploy
5. **Troubleshooting**: Follow debugging steps systematically

### File Editing Guidelines

- **Bot Configs**: Edit individual files in `configs/`
- **Dashboard**: Primary file is `dashboard/app/dashboard.py`
- **Docker Compose**: Main file is `docker/docker-compose-with-ui.yml`
- **Management**: Scripts in `scripts/` directory

## External Dependencies

- **Freqtrade**: Core trading bot framework
- **FreqUI**: Official web interface
- **Binance API**: Exchange integration
- **GCP Services**: Compute, networking, storage

## Useful URLs and References

- **GitHub Repo**: https://github.com/myownipgit/freqtrade-gcp-deployment
- **Live Dashboard**: http://35.185.177.130:5000
- **FreqUI**: http://35.185.177.130:3000
- **Freqtrade Docs**: https://www.freqtrade.io/en/stable/
- **GCP Console**: https://console.cloud.google.com/

---

**Note for Claude Code**: This project is designed for defensive trading bot deployment and monitoring. Always prioritize security, proper testing, and responsible trading practices.