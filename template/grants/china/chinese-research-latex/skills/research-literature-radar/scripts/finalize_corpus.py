#!/usr/bin/env python3
"""Compatibility entry point for the idempotent integrity reconciler."""
from reconcile_integrity import main


if __name__ == "__main__":
    raise SystemExit(main())
