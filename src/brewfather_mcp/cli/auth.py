"""Authentication management for the Brewfather CLI."""

import json
import os
from pathlib import Path

import click

CONFIG_DIR = Path.home() / ".config" / "brewfather-cli"
CONFIG_FILE = CONFIG_DIR / "auth.json"


def load_credentials() -> tuple[str, str]:
    """Load credentials from env vars or config file.

    Returns:
        Tuple of (user_id, api_key)

    Raises:
        click.ClickException: If credentials are not found.
    """
    user_id = os.getenv("BREWFATHER_API_USER_ID")
    api_key = os.getenv("BREWFATHER_API_KEY")

    if user_id and api_key:
        return user_id, api_key

    if CONFIG_FILE.exists():
        try:
            config = json.loads(CONFIG_FILE.read_text())
            user_id = config.get("user_id")
            api_key = config.get("api_key")
            if user_id and api_key:
                return user_id, api_key
        except (json.JSONDecodeError, OSError) as e:
            raise click.ClickException(f"Failed to read config file {CONFIG_FILE}: {e}")

    raise click.ClickException(
        "No credentials found. Set BREWFATHER_API_USER_ID and BREWFATHER_API_KEY "
        "environment variables, or run 'brewfather-cli auth configure'."
    )


def credential_source() -> str:
    """Return a string describing where credentials come from."""
    if os.getenv("BREWFATHER_API_USER_ID") and os.getenv("BREWFATHER_API_KEY"):
        return "environment variables"
    if CONFIG_FILE.exists():
        return f"config file ({CONFIG_FILE})"
    return "not configured"


@click.group()
def auth() -> None:
    """Manage Brewfather API credentials."""


@auth.command()
def configure() -> None:
    """Interactively configure API credentials."""
    click.echo("Brewfather API Credentials Setup")
    click.echo("=" * 40)
    click.echo("Get your credentials from https://web.brewfather.app/tabs/settings (API section)")
    click.echo()

    user_id = click.prompt("User ID")
    api_key = click.prompt("API Key")

    click.echo("\nValidating credentials...")
    try:
        import asyncio
        from brewfather_mcp.api import BrewfatherClient

        client = BrewfatherClient(user_id=user_id, api_key=api_key)
        # Validate by making a simple API call
        asyncio.run(client.get_batches_list())
        click.echo("✓ Credentials valid!")
    except Exception as e:
        raise click.ClickException(f"Credential validation failed: {e}")

    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(json.dumps({"user_id": user_id, "api_key": api_key}, indent=2))
    CONFIG_FILE.chmod(0o600)
    click.echo(f"✓ Credentials saved to {CONFIG_FILE}")


@auth.command()
def status() -> None:
    """Show authentication status and validate connection."""
    source = credential_source()
    click.echo(f"Credential source: {source}")

    if source == "not configured":
        click.echo("Status: NOT CONFIGURED")
        return

    try:
        user_id, api_key = load_credentials()
        click.echo(f"User ID: {user_id[:4]}...{user_id[-4:] if len(user_id) > 8 else ''}")
    except click.ClickException:
        click.echo("Status: ERROR loading credentials")
        return

    click.echo("Validating connection...")
    try:
        import asyncio
        from brewfather_mcp.api import BrewfatherClient

        client = BrewfatherClient(user_id=user_id, api_key=api_key)
        asyncio.run(client.get_batches_list())
        click.echo("Status: CONNECTED ✓")
    except Exception as e:
        click.echo(f"Status: FAILED - {e}")
