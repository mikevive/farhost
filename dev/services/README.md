# Shared Development Services

Local development infrastructure using Podman and Kubernetes-compatible YAML.

## Available Services

### PostgreSQL
Location: `postgres/`

Shared PostgreSQL 14.7 instance for all local development databases.

**Quick commands:**
```bash
# Start
podman play kube ~/dev/shared-services/postgres/postgres.yaml

# Stop
podman play kube --down ~/dev/shared-services/postgres/postgres.yaml
```

See [postgres/README.md](postgres/README.md) for detailed documentation.

## Philosophy

This directory contains Kubernetes-compatible YAML definitions for local development services that are:

- **Shared across projects** - Single instance, multiple databases
- **Kubernetes-native** - Same YAML works in k8s clusters
- **Reproducible** - Easy to recreate from scratch
- **Version controlled** - Can be checked into git or backed up

## Adding New Services

Create a new directory for each service:

```bash
mkdir -p ~/dev/shared-services/redis
mkdir -p ~/dev/shared-services/rabbitmq
```

Follow the same pattern:
- `service-name-dev.yaml` - Kubernetes Pod definition
- `README.md` - Service-specific documentation
- `init-scripts/` or `config/` - Initialization files

## Best Practices

1. **Use Podman pods** for multi-container services
2. **Use named volumes** for data persistence
3. **Document connection strings** in service READMEs
4. **Add shell aliases** for common operations
5. **Keep it simple** - optimize for local development, not production
