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

## Regenerating Clients from OpenAPI Specs

When OpenAPI specifications change, regenerate the clients:

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run generation script
./scripts/generate-clients.sh
```

The script uses `openapi-python-client` to generate typed clients from specs in `openapi/`.

**Source**
- `scripts/generate-clients.sh`

## GitHub Actions Workflow

The repository includes a GitHub Actions workflow that automatically regenerates clients when OpenAPI specs change.

**Trigger:** Push to `mainline` branch with changes to `openapi/**`

**Actions:**
1. Install `openapi-python-client`
2. Run `./scripts/generate-clients.sh`
3. Commit and push regenerated code

**Source**
- `.github/workflows/generate-clients.yaml`

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
