# PostgreSQL Development Environment

Shared PostgreSQL instance for local development using Podman and Kubernetes YAML.

## Understanding Container Names

When using `podman play kube`, containers are named using the pattern: `{pod-name}-{container-name}`

In this setup:
- **Pod name:** `postgres` (defined in metadata.name)
- **Container name:** `postgres` (defined in spec.containers[].name)
- **Resulting container name:** `postgres-postgres`

All `podman exec` and `podman logs` commands must use the full container name: `postgres-postgres`

## Quick Start

```bash
# Start PostgreSQL
podman play kube ~/.farhost/dev/services/postgres/postgres.yaml

# Stop PostgreSQL
podman play kube --down ~/.farhost/dev/services/postgres/postgres.yaml

# Recreate (clean restart)
podman play kube --down ~/.farhost/dev/services/postgres/postgres.yaml
podman play kube ~/.farhost/dev/services/postgres/postgres.yaml
```

**Note:** Commands must be run from your home directory, or adjust paths accordingly. The YAML file uses relative paths for init-scripts, so Podman will resolve them relative to the YAML file location.

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
podman exec -it postgres-postgres psql -U root -d postgres
```

### Create a new database
```bash
podman exec -it postgres-postgres psql -U root -d postgres -c "CREATE DATABASE your_db_name;"
```

### List all databases
```bash
podman exec -it postgres-postgres psql -U root -d postgres -c "\l"
```

### Drop a database
```bash
podman exec -it postgres-postgres psql -U root -d postgres -c "DROP DATABASE your_db_name;"
```

## Adding New Project Databases

Edit `init-scripts/01-init-databases.sql` and add:

```sql
CREATE DATABASE your_new_project_db;
```

**Note:** Init scripts only run on first container creation (when the data directory is empty). To apply changes to init scripts:

```bash
# Stop the pod
podman play kube --down ~/.farhost/dev/services/postgres/postgres.yaml

# Remove the volume to reset (WARNING: deletes all data)
podman volume rm postgres-data

# Recreate the pod
podman play kube ~/.farhost/dev/services/postgres/postgres.yaml
```

**Note about volumes:** Podman automatically creates the `postgres-data` volume when first running the pod. No manual volume creation is needed.

## Troubleshooting

### Check if PostgreSQL is running
```bash
podman pod ps
podman ps --pod
```

### View logs
```bash
podman logs postgres-postgres

# Follow logs in real-time
podman logs -f postgres-postgres
```

### Check volume
```bash
podman volume ls | grep postgres
podman volume inspect postgres-data
```

### Init scripts not running
If your initialization scripts aren't being executed:

1. **Check that the data directory is empty** - Init scripts only run on first startup when `/var/lib/postgresql/data` is empty
2. **Verify init-scripts directory exists** - The `init-scripts` directory must be in the same directory as `postgres.yaml`
3. **Check logs for initialization messages:**
   ```bash
   podman logs postgres-postgres | grep -i init
   ```
4. **Verify file permissions** - Init script files should be readable
5. **To force re-initialization** - Remove the volume and restart:
   ```bash
   podman play kube --down ~/.farhost/dev/services/postgres/postgres.yaml
   podman volume rm postgres-data
   podman play kube ~/.farhost/dev/services/postgres/postgres.yaml
   ```

### Complete cleanup
```bash
# Stop and remove pod
podman play kube --down ~/.farhost/dev/services/postgres/postgres.yaml

# Remove volume (WARNING: deletes all data)
podman volume rm postgres-data

# Start fresh
podman play kube ~/.farhost/dev/services/postgres/postgres.yaml
```

## Shell Aliases (Optional)

Add to your `~/.zshrc` or `~/.bashrc`:

```bash
# PostgreSQL aliases
alias pgstart='podman play kube ~/.farhost/dev/services/postgres/postgres.yaml'
alias pgstop='podman play kube --down ~/.farhost/dev/services/postgres/postgres.yaml'
alias pgrestart='pgstop && pgstart'
alias pgshell='podman exec -it postgres-postgres psql -U root -d postgres'
alias pglogs='podman logs -f postgres-postgres'
alias pgstatus='podman pod ps | grep postgres'
```

Then reload your shell:
```bash
source ~/.zshrc  # or source ~/.bashrc
```
