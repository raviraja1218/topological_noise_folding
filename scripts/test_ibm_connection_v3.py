#!/usr/bin/env python
"""
Test IBM Quantum connection using Qiskit 0.45 (stable)
"""

import sys
import subprocess

TOKEN = "4KetLabdZi485z11ggi4xgz0rhoPv2oN7tkQUEFXS8k5"

print("="*60)
print("IBM QUANTUM CONNECTION TEST (Qiskit 0.45)")
print("="*60)
print(f"Token: {TOKEN[:10]}...{TOKEN[-5:]}")

# Ensure pkg_resources is available
try:
    import pkg_resources
    print("✅ pkg_resources found")
except ImportError:
    print("📦 Installing setuptools...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "setuptools==69.0.0"])
    import pkg_resources

# Try different import approaches
try:
    # Method 1: Direct IBMQ import (Qiskit 0.45 style)
    from qiskit import IBMQ
    print("✅ IBMQ imported directly")
    
    # Save token
    IBMQ.save_account(TOKEN, overwrite=True)
    print("✅ Token saved")
    
    # Load account
    provider = IBMQ.load_account()
    print("✅ Connected successfully!")
    
except ImportError:
    try:
        # Method 2: Runtime service (alternative)
        from qiskit_ibm_runtime import QiskitRuntimeService
        
        service = QiskitRuntimeService(
            channel="ibm_quantum",
            token=TOKEN
        )
        provider = service
        print("✅ Connected via RuntimeService")
        
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        print("\nTrying to install missing packages...")
        
        # Install missing packages
        subprocess.check_call([sys.executable, "-m", "pip", "install", "qiskit-ibm-provider"])
        
        # Try again
        from qiskit import IBMQ
        IBMQ.save_account(TOKEN, overwrite=True)
        provider = IBMQ.load_account()
        print("✅ Connected after installation")

# List backends
print("\n📡 Available backends:")
try:
    backends = provider.backends(simulator=False, operational=True)
    if not backends:
        print("   No operational backends found")
    else:
        for backend in backends:
            try:
                status = backend.status()
                config = backend.configuration()
                print(f"   • {backend.name:20s}: {config.n_qubits:3d} qubits, {status.pending_jobs:3d} jobs")
            except:
                print(f"   • {backend.name}: info unavailable")
except Exception as e:
    print(f"   Error listing backends: {e}")

# Get least busy
if backends:
    try:
        from qiskit.providers.ibmq import least_busy
        backend = least_busy(backends)
        print(f"\n✅ Least busy: {backend.name}")
        print(f"   Queue: {backend.status().pending_jobs} jobs")
    except Exception as e:
        print(f"\n❌ Could not determine least busy: {e}")

print("\n✅ Connection test complete!")
