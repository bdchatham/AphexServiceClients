# Operations

## Installation

### From PyPI (when published)

```bash
pip install aphex-service-clients
```

### From Source

```bash
git clone https://github.com/bdchatham/AphexServiceClients.git
cd AphexServiceClients
pip install -e .
```

### With Development Dependencies

```bash
pip install -e ".[dev]"
```

## Kubernetes Deployment

When using these clients in Kubernetes pods, use cluster-internal service names:

### Typical Service URLs

```python
# Embedding service (in archon-knowledge-base namespace)
embedding_client = EmbeddingClient(
    base_url="http://embedding-svc.archon-knowledge-base:8000"
)

# Query service (in archon-knowledge-base namespace)
query_client = QueryClient(
    base_url="http://query.archon-knowledge-base:8080"
)
```

### Cross-Namespace Access

For services in different namespaces, use fully qualified service names:

```python
# From archon-orchestrator namespace accessing query service
query_client = QueryClient(
    base_url="http://query.archon-knowledge-base.svc.cluster.local:8080"
)
```

**Source**
- Kubernetes DNS naming conventions
- `manifests/` in consuming repositories (e.g., ArchonKnowledgeBaseInfrastructure)

## Regenerating Clients from OpenAPI Specs

When OpenAPI specifications change, regenerate the clients:

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Regenerate clients
make generate-clients

# Commit the changes
git add src/aphex_clients/generated/
git commit -m "chore: regenerate clients from updated specs"
```

**Important:** The CI workflow (`check-clients`) will fail if generated code doesn't match committed code. This ensures you consciously commit client changes when specs change.

**Source**
- `scripts/generate-clients.sh`
- `Makefile`
- `.github/workflows/check-clients.yaml`

## GitHub Actions Workflow

The repository includes a GitHub Actions workflow that verifies generated clients match the committed code.

**Trigger:** Push or PR to `mainline` branch

**Behavior:**
1. Regenerates clients from OpenAPI specs
2. Compares generated code to committed code
3. **Fails if they differ** - forces developers to commit client changes

This ensures OpenAPI specs and generated clients stay in sync.

**Source**
- `.github/workflows/check-clients.yaml`
- `Makefile` (check-clients target)

## Versioning

The package follows semantic versioning:
- **Major**: Breaking API changes
- **Minor**: New features, backward compatible
- **Patch**: Bug fixes, backward compatible

Current version is defined in `pyproject.toml`.

**Source**
- `pyproject.toml`

## Troubleshooting

### Connection Errors

If clients fail to connect to services:

1. Verify the service URL is correct
2. Check network connectivity to the service
3. Verify the service is running and healthy
4. Check for firewall or network policy issues

The client will automatically retry up to 5 times with exponential backoff.

### Timeout Errors

If requests timeout:

1. Check if the service is under heavy load
2. Consider increasing the timeout parameter:
   ```python
   client = EmbeddingClient(base_url="...", timeout=120.0)
   ```
3. For embedding requests, large batches may need longer timeouts

### Import Errors

If imports fail:

1. Verify the package is installed: `pip show aphex-service-clients`
2. Check Python version is 3.11+
3. Reinstall: `pip install --force-reinstall aphex-service-clients`

**Source**
- `src/aphex_clients/http.py` - Retry configuration
- `src/aphex_clients/embedding.py` - Timeout configuration
