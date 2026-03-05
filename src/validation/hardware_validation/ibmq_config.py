"""
IBM Quantum configuration - stores your token securely
"""

import os
from src.hardware_validation.pathlib import Path

# YOUR IBM QUANTUM TOKEN
IBM_TOKEN = "4KetLabdZi485z11ggi4xgz0rhoPv2oN7tkQUEFXS8k5"

def get_token():
    """Return the IBM Quantum token"""
    return IBM_TOKEN

def save_token_permanently():
    """Save token to IBMQ for permanent use"""
    from src.hardware_validation.qiskit import IBMQ
    
    try:
        IBMQ.save_account(IBM_TOKEN, overwrite=True)
        print("✅ Token saved permanently")
        return True
    except Exception as e:
        print(f"❌ Failed to save token: {e}")
        return False

def test_connection():
    """Test connection with saved token"""
    from src.hardware_validation.qiskit import IBMQ
    
    try:
        provider = IBMQ.load_account()
        print("✅ Connection successful")
        return provider
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return None

if __name__ == "__main__":
    print("="*60)
    print("IBM Quantum Token Configuration")
    print("="*60)
    
    # Save token
    save_token_permanently()
    
    # Test connection
    test_connection()
