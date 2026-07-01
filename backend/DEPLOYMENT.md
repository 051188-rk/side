# Deployment Guide

## Prerequisites

- Python 3.12+
- Docker and Docker Compose
- Firebase project with Firestore
- API keys for Groq, Gemini, Cognee
- Service accounts for integrations

## Environment Setup

### 1. Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

Required variables:
- `FIREBASE_PROJECT_ID`
- `FIREBASE_PRIVATE_KEY`
- `GROQ_API_KEY`
- `GEMINI_API_KEY`
- `COGNEE_API_KEY`
- `DISCORD_BOT_TOKEN` (optional)
- `TELEGRAM_BOT_TOKEN` (optional)
- `GITHUB_ACCESS_TOKEN` (optional)

### 2. Firebase Setup

1. Go to Firebase Console
2. Create a new project or select existing
3. Enable Firestore Database
4. Enable Authentication
5. Go to Project Settings > Service Accounts
6. Generate a new private key
7. Save the JSON file securely
8. Copy the contents to your `.env` file

### 3. Groq Setup

1. Visit https://console.groq.com
2. Create an account
3. Generate an API key
4. Add to `.env` as `GROQ_API_KEY`

### 4. Gemini Setup

1. Visit https://makersuite.google.com/app/apikey
2. Create a new API key
3. Add to `.env` as `GEMINI_API_KEY`

### 5. Cognee Setup

1. Sign up at Cognee
2. Get API key
3. Configure vector database (Weaviate)
4. Configure knowledge graph (Neo4j)
5. Add credentials to `.env`

## Local Development

### Using uv

```bash
# Install dependencies
uv pip install -r requirements.txt

# Run development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Using Docker

```bash
# Build image
docker build -t side-backend .

# Run container
docker run -p 8000:8000 --env-file .env side-backend
```

### Using Docker Compose

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## Production Deployment

### Option 1: Docker Compose

```bash
# Build and start
docker-compose up -d

# Check health
curl http://localhost:8000/health
```

### Option 2: Kubernetes

Create `k8s-deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: side-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: side-backend
  template:
    metadata:
      labels:
        app: side-backend
    spec:
      containers:
      - name: side-backend
        image: side-backend:latest
        ports:
        - containerPort: 8000
        env:
        - name: APP_ENV
          value: "production"
        envFrom:
        - secretRef:
            name: side-secrets
---
apiVersion: v1
kind: Service
metadata:
  name: side-backend
spec:
  selector:
    app: side-backend
  ports:
  - port: 80
    targetPort: 8000
  type: LoadBalancer
```

Create secrets:

```bash
kubectl create secret generic side-secrets \
  --from-literal=FIREBASE_PROJECT_ID=your-project \
  --from-literal=GROQ_API_KEY=your-key \
  --from-literal=GEMINI_API_KEY=your-key
```

Deploy:

```bash
kubectl apply -f k8s-deployment.yaml
```

### Option 3: Cloud Run

```bash
# Build and push
gcloud builds submit --tag gcr.io/PROJECT_ID/side-backend

# Deploy
gcloud run deploy side-backend \
  --image gcr.io/PROJECT_ID/side-backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

## Monitoring

### Health Checks

```bash
# Health check
curl http://localhost:8000/health

# Readiness check
curl http://localhost:8000/health/ready

# Liveness check
curl http://localhost:8000/health/live
```

### Logs

```bash
# Docker logs
docker-compose logs -f side-backend

# Kubernetes logs
kubectl logs -f deployment/side-backend
```

### Metrics

The application exposes metrics at `/metrics` (if configured).

## Scaling

### Horizontal Scaling

```bash
# Docker Compose
docker-compose up --scale side-backend=3

# Kubernetes
kubectl scale deployment side-backend --replicas=5
```

### Load Balancing

Use a load balancer (Nginx, HAProxy, or cloud provider LB) in front of multiple instances.

## Security

### SSL/TLS

Use a reverse proxy with SSL termination:

```nginx
server {
    listen 443 ssl;
    server_name api.side.ai;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Firewall

Allow only necessary ports:
- 80/443 for HTTP/HTTPS
- 8000 for internal API communication

### Secrets Management

Use a secrets manager:
- AWS Secrets Manager
- Google Secret Manager
- HashiCorp Vault

## Backup

### Firestore Backup

Use Firebase Console or gcloud CLI:

```bash
gcloud firestore export gs://backup-bucket
```

### Application Backup

Backup:
- `.env` file
- Any local data
- Configuration files

## Troubleshooting

### Common Issues

1. **Firebase Connection Error**
   - Verify credentials in `.env`
   - Check Firebase project status
   - Ensure Firestore is enabled

2. **LLM API Errors**
   - Verify API keys
   - Check rate limits
   - Review billing status

3. **Webhook Failures**
   - Verify webhook URLs
   - Check signature verification
   - Review webhook logs

### Debug Mode

Enable debug mode in `.env`:

```env
DEBUG=true
LOG_LEVEL=DEBUG
```

## Performance Tuning

### Database

- Use Firestore indexes for frequently queried fields
- Implement caching for read-heavy operations
- Optimize query patterns

### Application

- Increase worker count in `docker-compose.yml`
- Enable connection pooling
- Use async operations throughout

### LLM

- Implement request batching
- Use streaming for long responses
- Cache common queries

## CI/CD

### GitHub Actions

```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Build Docker image
      run: docker build -t side-backend .
    - name: Deploy
      run: docker-compose up -d
```

## Rollback

### Docker

```bash
# Stop current
docker-compose down

# Start previous version
docker-compose up -d
```

### Kubernetes

```bash
# Rollback to previous revision
kubectl rollout undo deployment/side-backend
```

## Maintenance

### Updates

1. Pull latest code
2. Update dependencies
3. Run tests
4. Deploy new version
5. Monitor for issues

### Database Maintenance

- Regular backups
- Index optimization
- Data cleanup

## Support

For deployment issues, contact:
- DevOps team: devops@side.ai
- Engineering team: engineering@side.ai
