"""Database module for Supabase integration."""

from .supabase import get_supabase_client, supabase

__all__ = ["get_supabase_client", "supabase"]
