# Freqtrade GCP Deployment

Deploy 12 independent Freqtrade trading bots to Google Cloud Platform with a unified dashboard and monitoring system.

## 🚀 Project Overview

This project provides a complete solution for deploying multiple Freqtrade cryptocurrency trading bots on Google Cloud Platform (GCP). It includes:

- **12 Independent Trading Bots**: Each bot runs in its own container with isolated configuration
- **Unified Multi-Bot Dashboard**: Real-time monitoring of all bots with portfolio analytics
- **FreqUI Interface**: Official Freqtrade web interface for detailed bot management
- **Automated Deployment**: Single-command deployment and management scripts
- **Health Monitoring**: Built-in health checks and logging
- **Security**: Proper network isolation and firewall rules

## 📊 Live Dashboards

- **Multi-Bot Dashboard**: http://35.185.177.130:5000 - Custom dashboard showing all bots
- **FreqUI Interface**: http://35.185.177.130:3000 - Official Freqtrade interface

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    GCP VM Instance                          │
│                  (freqtrade-cluster)                        │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐           │
│  │ Bot 01      │ │ Bot 02      │ │     ...     │           │
│  │ Port: 8080  │ │ Port: 8081  │ │ Bot 12: 8091│           │
│  └─────────────┘ └─────────────┘ └─────────────┘           │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐           │
│  │ FreqUI      │ │ Dashboard   │ │ Monitoring  │           │
│  │ Port: 3000  │ │ Port: 5000  │ │             │           │
│  └─────────────┘ └─────────────┘ └─────────────┘           │
└─────────────────────────────────────────────────────────────┘
```

## 🔧 Project Structure

```
freqtrade-gcp-deployment/
├── configs/                    # Bot-specific configurations
│   ├── config-bot-01.json      # Individual bot configs
│   └── ...
├── dashboard/                  # Multi-bot dashboard
│   ├── app/dashboard.py        # Flask backend
│   ├── templates/              # HTML templates
│   └── Dockerfile
├── docker/                     # Docker configurations
│   ├── docker-compose-with-ui.yml  # Main compose file
│   └── strategies/             # Trading strategies
├── scripts/                    # Management scripts
│   ├── manage_cluster.sh       # Main management script
│   ├── health_check_cluster.sh # Health monitoring
│   └── deploy_dashboard.sh     # Dashboard deployment
└── CLAUDE.md                   # Claude Code instructions
```

## 🚀 Quick Start

### Prerequisites

- Google Cloud Platform account
- `gcloud` CLI installed and configured
- Docker (for local development)

### 1. Setup Environment

```bash
export PROJECT_ID="your-project-id"
export ZONE="asia-southeast1-a"
export REGION="asia-southeast1"
```

### 2. Deploy Infrastructure

```bash
# Clone the repository
git clone https://github.com/myownipgit/freqtrade-gcp-deployment.git
cd freqtrade-gcp-deployment

# Enable required GCP APIs
gcloud services enable compute.googleapis.com
gcloud services enable container.googleapis.com
gcloud services enable storage.googleapis.com

# Create network infrastructure
gcloud compute networks create freqtrade-network --subnet-mode custom
gcloud compute networks subnets create freqtrade-subnet \
    --network freqtrade-network \
    --range 10.0.0.0/24 \
    --region $REGION

# Create firewall rules
gcloud compute firewall-rules create freqtrade-api-access \
    --network freqtrade-network \
    --allow tcp:8080-8091,tcp:3000,tcp:5000,tcp:22 \
    --source-ranges 0.0.0.0/0
```

### 3. Deploy Cluster

```bash
# Create VM instance with startup script
gcloud compute instances create freqtrade-cluster \
    --zone=$ZONE \
    --machine-type=e2-standard-4 \
    --network-interface=network-tier=PREMIUM,subnet=freqtrade-subnet \
    --tags=freqtrade-cluster \
    --image-family=ubuntu-2004-lts \
    --image-project=ubuntu-os-cloud \
    --boot-disk-size=50GB \
    --metadata-from-file startup-script=scripts/startup-script-multibot.sh
```

### 4. Monitor Deployment

```bash
# Check cluster status
./scripts/manage_cluster.sh status

# Run health check
./scripts/health_check_cluster.sh

# View logs
./scripts/manage_cluster.sh logs all
```

## 📋 Management Commands

### Cluster Management

```bash
# Start/stop entire cluster
./scripts/manage_cluster.sh start
./scripts/manage_cluster.sh stop
./scripts/manage_cluster.sh restart

# Check status
./scripts/manage_cluster.sh status

# SSH into cluster
./scripts/manage_cluster.sh ssh
```

### Individual Bot Management

```bash
# Start/stop specific bot
./scripts/manage_cluster.sh start-bot 01
./scripts/manage_cluster.sh stop-bot 01
./scripts/manage_cluster.sh restart-bot 01

# View bot logs
./scripts/manage_cluster.sh logs 01
```

### Dashboard Management

```bash
# Restart dashboard
./scripts/manage_cluster.sh dashboard-restart

# View dashboard logs
./scripts/manage_cluster.sh dashboard-logs
```

## 🔍 Monitoring & Health Checks

### Health Check Script

```bash
./scripts/health_check_cluster.sh
```

This will check:
- ✅ VM instance status
- ✅ All 12 bot API endpoints
- ✅ FreqUI dashboard
- ✅ Multi-bot dashboard
- ✅ Container health

### Dashboard Features

The multi-bot dashboard provides:
- Real-time bot status monitoring
- Portfolio-wide profit/loss tracking
- Trade count and open positions
- Individual bot performance metrics
- Auto-refresh every 10 seconds

## 🔧 Configuration

### Bot Configuration

Each bot has its own configuration file in `configs/config-bot-XX.json`:

```json
{
  "max_open_trades": 3,
  "stake_currency": "USDT",
  "stake_amount": 100,
  "dry_run": true,
  "exchange": {
    "name": "binance",
    "key": "",
    "secret": ""
  },
  "api_server": {
    "enabled": true,
    "listen_port": 8080,
    "username": "freqtrader",
    "password": "botXXpass"
  }
}
```

### Exchange Setup

To connect to real exchanges:
1. Edit bot configuration files
2. Add API keys and secrets
3. Set `"dry_run": false`
4. Restart affected bots

## 🚨 Troubleshooting

### Common Issues

1. **Dashboard showing error bots**
   - Check API authentication in bot configs
   - Verify containers are running: `docker-compose ps`
   - Check firewall rules

2. **Bots not responding**
   - Check container logs: `./scripts/manage_cluster.sh logs XX`
   - Restart specific bot: `./scripts/manage_cluster.sh restart-bot XX`

3. **FreqUI connection issues**
   - Verify bot API server settings
   - Check network connectivity
   - Restart FreqUI: `./scripts/manage_cluster.sh ui-restart`

### Log Analysis

```bash
# View all logs
./scripts/manage_cluster.sh logs all

# View specific bot
./scripts/manage_cluster.sh logs 01

# View dashboard logs
./scripts/manage_cluster.sh logs dashboard

# View FreqUI logs
./scripts/manage_cluster.sh logs ui
```

## 💰 Cost Estimation

- **Compute**: ~$120/month (e2-standard-4)
- **Storage**: ~$10/month (50GB persistent disk)
- **Network**: ~$5/month (egress traffic)
- **Total**: ~$135/month

## 🔒 Security Features

- Custom VPC network with isolated subnet
- Firewall rules restricting access to necessary ports
- Individual bot authentication
- Container isolation
- No root SSH access by default

## 🔄 Backup & Recovery

The project includes automated backup scripts:

```bash
# Backup all configurations and data
./scripts/backup_restore.sh backup

# Restore from backup
./scripts/backup_restore.sh restore <timestamp>
```

## 📚 Claude Code Integration

This project is designed to work seamlessly with Claude Code. See [CLAUDE.md](CLAUDE.md) for detailed instructions on:

- Project structure and conventions
- Common development commands
- Deployment procedures
- Troubleshooting guides

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [Freqtrade](https://github.com/freqtrade/freqtrade) - The awesome trading bot framework
- [FreqUI](https://github.com/freqtrade/frequi) - Official Freqtrade web interface
- Google Cloud Platform for reliable infrastructure

## 📞 Support

For issues and questions:
1. Check the troubleshooting section
2. Review the logs using provided scripts
3. Open an issue on GitHub
4. Check Freqtrade documentation: https://www.freqtrade.io/

---

**⚠️ Disclaimer**: Trading cryptocurrencies involves risk. This software is for educational purposes. Always test with dry-run mode before using real funds.