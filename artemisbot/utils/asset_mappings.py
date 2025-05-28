import json
import os
from typing import Dict, Optional, List
from config import ASSET_MAPPINGS_FILE

# Global mappings dictionary
MAPPINGS = {
    "artemis_id_to_symbols": {},
    "symbol_to_artemis_id": {},
    "artemis_id_to_type": {},
    "symbol_to_type": {}
}

def load_mappings() -> None:
    """Load asset mappings from cache or API."""
    try:
        with open(ASSET_MAPPINGS_FILE, "r") as f:
            raw_mappings = json.load(f)
            
        # Copy all mappings directly from the file
        MAPPINGS["artemis_id_to_symbols"] = raw_mappings.get("artemis_id_to_symbols", {})
        MAPPINGS["artemis_id_to_type"] = raw_mappings.get("artemis_id_to_type", {})
        
        # Build symbol_to_artemis_id and symbol_to_type mappings
        MAPPINGS["symbol_to_artemis_id"] = {}
        MAPPINGS["symbol_to_type"] = {}
        
        for artemis_id, symbols in MAPPINGS["artemis_id_to_symbols"].items():
            if isinstance(symbols, list):
                for symbol in symbols:
                    MAPPINGS["symbol_to_artemis_id"][symbol.lower()] = artemis_id
                    MAPPINGS["symbol_to_type"][symbol.lower()] = MAPPINGS["artemis_id_to_type"].get(artemis_id, "unknown")
            else:
                MAPPINGS["symbol_to_artemis_id"][symbols.lower()] = artemis_id
                MAPPINGS["symbol_to_type"][symbols.lower()] = MAPPINGS["artemis_id_to_type"].get(artemis_id, "unknown")
            
    except FileNotFoundError:
        raise Exception(f"Could not find mappings file at {ASSET_MAPPINGS_FILE}")

def get_asset_by_symbol(symbol: str) -> Optional[Dict]:
    """Get asset info by symbol."""
    if not MAPPINGS["symbol_to_artemis_id"]:
        load_mappings()
        
    artemis_id = MAPPINGS["symbol_to_artemis_id"].get(symbol.lower())
    if not artemis_id:
        return None
        
    return {
        "id": artemis_id,
        "symbol": symbol.lower(),
        "type": MAPPINGS["symbol_to_type"].get(symbol.lower(), "unknown")
    }

def get_asset_by_id(artemis_id: str) -> Optional[Dict]:
    """Get asset info by Artemis ID."""
    if not MAPPINGS["artemis_id_to_symbols"]:
        load_mappings()
        
    symbols = MAPPINGS["artemis_id_to_symbols"].get(artemis_id)
    if not symbols:
        return None
        
    # Use the first symbol in the list
    symbol = symbols[0] if isinstance(symbols, list) else symbols
    
    return {
        "id": artemis_id,
        "symbol": symbol,
        "type": MAPPINGS["artemis_id_to_type"].get(artemis_id, "unknown")
    }

def clean_asset_params(asset: str, asset_type: str) -> Dict:
    """
    Clean and validate asset parameters.
    
    Args:
        asset: The asset symbol or ID
        asset_type: The type of asset
        
    Returns:
        Dictionary with cleaned asset parameters
        
    Raises:
        ValueError: If the asset is not found
    """
    # Try to get asset info
    asset_info = get_asset_by_symbol(asset) or get_asset_by_id(asset)
    if not asset_info:
        raise ValueError(f"Unknown asset: {asset}")
        
    return {
        "id": asset_info["id"],
        "type": asset_type.lower()
    }