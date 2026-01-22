"""
MAPA-RD: Official CLI Entry Point
---------------------------------
Author: Antigravity AI / Senior Python standards
Version: 2.3.0 (Pro)

Purpose:
    This is the primary interface for the MAPA-RD system. It initializes the 
    core engine (Orchestrator), validates user input, and triggers the 
    end-to-end intelligence lifecycle.

Architecture:
    This script acts as a 'Lightweight Wrapper'. All business logic is 
    encapsulated within the Orchestrator to ensure the CLI remains clean 
    and maintainable.
"""

import os
import sys
import argparse
import logging
from datetime import datetime
from typing import Optional

# ---------------------------------------------------------
# ENVIRONMENT SETUP
# Ensuring the Source directory is in the system path for seamless
# cross-module imports within the MAPA-RD ecosystem.
# ---------------------------------------------------------
SOURCE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '07_Src')
sys.path.append(SOURCE_DIR)

# Core MAPA-RD Imports
try:
    from orchestrator import Orchestrator
    from state_manager import StateManager
except ImportError as e:
    print(f"[CRITICAL] Failed to load core modules from {SOURCE_DIR}: {e}")
    sys.exit(1)

def main() -> None:
    """Professional CLI Entry point for the MAPA-RD Intelligence Pipeline."""
    
    # ---------------------------------------------------------
    # ARGUMENT PARSING
    # ---------------------------------------------------------
    parser = argparse.ArgumentParser(
        description="MAPA-RD: Professional Digital Intelligence & Privacy OSINT Pipeline",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument(
        "--client", 
        required=True, 
        help="Target Client ID or slug (e.g. 'ana-flores')."
    )
    parser.add_argument(
        "--type", 
        choices=["BASELINE", "FREQUENCY", "INCIDENT", "RESCUE"], 
        default="BASELINE", 
        help="Strategy for intelligence gathering."
    )
    parser.add_argument(
        "--debug", 
        action="store_true", 
        help="Enable full tracebacks and verbose debug logging."
    )

    args = parser.parse_args()
    
    # ---------------------------------------------------------
    # LOGGING CONFIGURATION
    # Using the standard library logging for enterprise observability.
    # ---------------------------------------------------------
    log_level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    logger = logging.getLogger("MAPA-RD")

    # Visual Branding Header
    print(f"\n{'='*70}")
    print(f" MAPA-RD INTELLIGENCE SYSTEM v2.3 | SESSION: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*70}\n")

    try:
        # 1. INITIALIZE CORE ENGINE
        # The Orchestrator manages the pipeline, while StateManager handles persistence.
        orchestrator = Orchestrator()
        sm = StateManager()
        
        # 2. CLIENT VALIDATION
        # We allow identification by ID or by human-readable Name Slug.
        client_id = args.client
        client = sm.get_client(client_id)
        
        if not client:
             logger.warning(f"ID '{client_id}' not found. Searching registry for matching slug...")
             
             # Reverse lookup in the client database
             found_id = None
             for cid, cdata in sm.data.get("clients", {}).items():
                 if cdata.get("client_name_slug") == client_id:
                     found_id = cid
                     break
             
             if found_id:
                 client_id = found_id
                 logger.info(f"Target identified via slug: {client_id}")
             else:
                 logger.info(f"ID '{client_id}' not found in registry. Proceeding to create new record...")

        # 3. TRIGGER LIFECYCLE
        # orchestrate() is the atomic entry point for the entire backend flow.
        logger.info(f"Starting pipeline for Client: {client_id} (Strategy: {args.type})")
        
        # This call handles: Intake -> Scan -> Process -> Report -> QC -> Notif
        intake_id, _ = orchestrator.orchestrate(client_id, analysis_type=args.type)
        
        # SUCCESS FOOTER
        print(f"\n{'*'*70}")
        print(f" [SUCCESS] Lifecycle finished for Job: {intake_id}")
        print(f" [OUTPUT] Reports saved in: 04_Data/reports/")
        print(f"{'*'*70}\n")

    except Exception as e:
        # Critical failure catch-all
        logger.critical(f"FATAL: Pipeline execution crashed: {str(e)}", exc_info=args.debug)
        print(f"\n[ERROR] El sistema se detuvo debido a un error crítico: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Standard Python entry block
    main()
