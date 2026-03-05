#!/usr/bin/env python
"""
Quick test of IBM Quantum connection with your token
Includes package installation check
"""

import sys
import subprocess
import time

# Check if qiskit is installed
try:
    from qiskit import IBMQ
    from qiskit.providers.ibmq import least_busy
    print("✅ Qiskit found")
except ImportError:
    print("❌ Qiskit not found. Installing now...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "qiskit", "qiskit-ibm-provider", "qiskit-aer"])
    from qiskit import IBMQ
    from qiskit.providers.ibmq import least_busy

TOKEN = "4KetLabdZi485z11ggi4xgz0rhoPv2oN7tkQUEFXS8k5"

print("="*60)
print("IBM QUANTUM CONNECTION TEST")
print("="*60)
print(f"Token: {TOKEN[:10]}...{TOKEN[-5:]}")

# Save token
print("\n📝 Saving token...")
try:
    IBMQ.save_account(TOKEN, overwrite=True)
    print("✅ Token saved")
except Exception as e:
    print(f"❌ Failed to save token: {e}")

# Load account
print("\n🔌 Loading account...")
try:
    provider = IBMQ.load_account()
    print("✅ Connected successfully!")
except Exception as e:
    print(f"❌ Connection failed: {e}")
    print("\nPossible issues:")
    print("   • Internet connection")
    print("   • Token validity (check IBM Quantum dashboard)")
    print("   • IBM Quantum service status")
    exit(1)

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
                print(f"   • {backend.name:20s}: {config.n_qubits:3d} qubits, {status.pending_jobs:3d} jobs pending")
            except:
                print(f"   • {backend.name}: status unavailable")
except Exception as e:
    print(f"   Error listing backends: {e}")

# Get least busy
if backends:
    try:
        backend = least_busy(backends)
        print(f"\n✅ Least busy: {backend.name}")
        print(f"   Queue: {backend.status().pending_jobs} jobs")
    except Exception as e:
        print(f"\n❌ Could not determine least busy: {e}")

print("\n✅ Connection test complete!")
