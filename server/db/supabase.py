"""Supabase client singleton."""

import os
from functools import lru_cache

from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables (override=True to use .env over shell vars)
load_dotenv(override=True)


@lru_cache()
def get_supabase_client() -> Client:
    """Get or create Supabase client singleton."""
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")

    if not url or not key:
        raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set")

    return create_client(url, key)


# Convenience export
supabase = get_supabase_client
