# JupyterHub Simple Configuration for Development

c = get_config()

# Network configuration
c.JupyterHub.ip = '0.0.0.0'
c.JupyterHub.port = 12000

# Use DummyAuthenticator for development (no password required)
from jupyterhub.auth import DummyAuthenticator
c.JupyterHub.authenticator_class = DummyAuthenticator
c.DummyAuthenticator.password = ""

# Use SimpleLocalProcessSpawner - simpler than LocalProcessSpawner
from jupyterhub.spawner import SimpleLocalProcessSpawner
c.JupyterHub.spawner_class = SimpleLocalProcessSpawner

# Database configuration (use SQLite for development)
c.JupyterHub.db_url = 'sqlite:///jupyterhub.sqlite'

# Admin users
c.Authenticator.admin_users = {'admin'}

# Allow named servers
c.JupyterHub.allow_named_servers = True

# Timeout settings
c.Spawner.start_timeout = 60
c.Spawner.http_timeout = 30

# Log level
c.Application.log_level = 'INFO'

# Hub configuration
c.JupyterHub.hub_ip = '0.0.0.0'

# Proxy configuration
c.ConfigurableHTTPProxy.should_start = True

# Allow iframe embedding
c.JupyterHub.tornado_settings = {
    'headers': {
        'Content-Security-Policy': "frame-ancestors 'self' *"
    }
}

print("JupyterHub simple configuration loaded successfully!")
print(f"Server will run on: http://0.0.0.0:{c.JupyterHub.port}")
print("Authentication: DummyAuthenticator (any username, no password)")
print("Spawner: SimpleLocalProcessSpawner")