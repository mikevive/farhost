# PostgreSQL Development Environment

Shared PostgreSQL instance for local development using Podman and Kubernetes YAML.

## Quick Start

```bash
# Start PostgreSQL
podman play kube ~/dev/shared-services/postgres/postgres.yaml

# Stop PostgreSQL
podman play kube --down ~/dev/shared-services/postgres/postgres.yaml

# Recreate (clean restart)
podman play kube --down ~/dev/shared-services/postgres/postgres.yaml
podman play kube ~/dev/shared-services/postgres/postgres.yaml
```

## Connection Details

- **Host:** `localhost` or `127.0.0.1`
- **Port:** `5432`
- **User:** `root`
- **Password:** (empty)
- **Default Database:** `postgres`

## Connection String Format

```bash
postgresql://root@127.0.0.1:5432/your_database_name
```

**Examples:**
```bash
# Connect to default postgres database
postgresql://root@127.0.0.1:5432/postgres

# Connect to a project-specific database
postgresql://root@127.0.0.1:5432/myproject
```

## Managing Databases

### Connect to PostgreSQL shell
```bash
podman exec -it dev-services-postgres psql -U root -d postgres
```

### Create a new database
```bash
podman exec -it dev-services-postgres psql -U root -d postgres -c "CREATE DATABASE your_db_name;"
```

### List all databases
```bash
podman exec -it dev-services-postgres psql -U root -d postgres -c "\l"
```

### Drop a database
```bash
podman exec -it dev-services-postgres psql -U root -d postgres -c "DROP DATABASE your_db_name;"
```

## Adding New Project Databases

Edit `init-scripts/01-init-databases.sql` and add:

```sql
CREATE DATABASE your_new_project_db;
```

Note: Init scripts only run on first container creation. To apply changes:

```bash
# Remove the volume to reset
podman volume rm postgres-data

# Recreate the pod
podman play kube --down ~/dev/shared-services/postgres/postgres.yaml
podman play kube ~/dev/shared-services/postgres/postgres.yaml
```

## Troubleshooting

### Check if PostgreSQL is running
```bash
podman pod ps
podman ps --pod
```

### View logs
```bash
podman logs dev-services-postgres
```

### Check volume
```bash
podman volume ls | grep postgres
podman volume inspect postgres-data
```

### Complete cleanup
```bash
# Stop and remove pod
podman play kube --down ~/dev/shared-services/postgres/postgres.yaml

# Remove volume (WARNING: deletes all data)
podman volume rm postgres-data

# Start fresh
podman play kube ~/dev/shared-services/postgres/postgres.yaml
```

## Shell Aliases (Optional)

Add to your `~/.zshrc` or `~/.bashrc`:

```bash
# PostgreSQL aliases
alias pgstart='podman play kube ~/dev/shared-services/postgres/postgres.yaml'
alias pgstop='podman play kube --down ~/dev/shared-services/postgres/postgres.yaml'
alias pgrestart='pgstop && pgstart'
alias pgshell='podman exec -it dev-services-postgres psql -U root -d postgres'
alias pglogs='podman logs -f dev-services-postgres'
alias pgstatus='podman pod ps | grep dev-services'
```

Then reload your shell:
```bash
source ~/.zshrc  # or source ~/.bashrc
```
