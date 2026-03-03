import asyncio
import ssl
from urllib.parse import urlparse

import asyncpg

from app.core.config import settings


async def probe(label: str, ssl_arg):
    parsed = urlparse(settings.DATABASE_URL)
    host = parsed.hostname
    port = parsed.port or 5432
    user = parsed.username
    database = (parsed.path or "/postgres").lstrip("/") or "postgres"
    password = parsed.password

    try:
        connection = await asyncpg.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            timeout=8,
            ssl=ssl_arg,
        )
        value = await connection.fetchval("select 1")
        print(f"{label}: OK -> {value}")
        await connection.close()
    except Exception as exc:
        print(f"{label}: {type(exc).__name__}: {exc}")


async def probe_custom(label: str, host: str, port: int, user: str, password: str, database: str, ssl_arg):
    try:
        connection = await asyncpg.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            timeout=8,
            ssl=ssl_arg,
        )
        value = await connection.fetchval("select 1")
        print(f"{label}: OK -> {value}")
        await connection.close()
    except Exception as exc:
        print(f"{label}: {type(exc).__name__}: {exc}")


async def main():
    parsed = urlparse(settings.DATABASE_URL)
    print(f"host={parsed.hostname}")
    print(f"port={parsed.port or 5432}")
    print(f"user={parsed.username}")
    print(f"db={(parsed.path or '/postgres').lstrip('/') or 'postgres'}")
    project_ref = (parsed.username or "").split(".")[-1]
    print(f"project_ref={project_ref}")

    await probe("ssl=None", None)
    await probe("ssl=True", True)
    await probe("ssl=context", ssl.create_default_context())

    if project_ref:
        direct_host = f"db.{project_ref}.supabase.co"
        print(f"direct_host={direct_host}")
        await probe_custom(
            "direct-5432-ssl-context",
            host=direct_host,
            port=5432,
            user=parsed.username,
            password=parsed.password,
            database=(parsed.path or "/postgres").lstrip("/") or "postgres",
            ssl_arg=ssl.create_default_context(),
        )


if __name__ == "__main__":
    asyncio.run(main())
