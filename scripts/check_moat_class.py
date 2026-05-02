#!/usr/bin/env python3
"""Convenience alias kept for compatibility — delegates to check_moat_taxonomy.py"""
import os, sys, subprocess
sys.exit(subprocess.run(["python3", os.path.join(os.path.dirname(__file__), "check_moat_taxonomy.py"), *sys.argv[1:]]).returncode)
