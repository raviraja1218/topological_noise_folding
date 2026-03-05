#!/usr/bin/env python
"""
Test IBM Quantum connection using Qiskit 1.0+ Runtime API
"""

import sys
import subprocess

TOKEN = "4KetLabdZi485z11ggi4xgz0rhoPv2oN7tkQUEFXS8k5"

print("="*60)
print("IBM QUANTUM CONNECTION TEST (Qiskit 1.0+)")
print("="*60)
print(f"Token: {TOKEN[:10]}...{TOKEN[-5:]}")

try:
    from qiskit_ibm_runtime import QiskitRuntimeService
    print("✅ Qiskit Runtime imported")
except ImportError:
    print("❌ qiskit-ibm-runtime not found. Installing...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "qiskit-ibm-runtime"])
    from qiskit_ibm_runtime import QiskitRuntimeService

# Initialize service
print("\n🔌 Initializing IBM Quantum service...")
try:
    service = QiskitRuntimeService(
        channel="ibm_quantum",
        token=TOKEN
    )
    print("✅ Connected successfully!")
except Exception as e:
    print(f"❌ Connection failed: {e}")
    print("\nTroubleshooting:")
    print("  1. Check token validity at https://quantum-computing.ibm.com/")
    print("  2. Ensure internet connection")
    print("  3. Try: pip install --upgrade qiskit-ibm-runtime")
    exit(1)

# List backends
print("\n📡 Available backends:")
try:
    backends = service.backends(simulator=False, operational=True)
    if not backends:
        print("   No operational backends found")
    else:
        for backend in backends:
            try:
                print(f"   • {backend.name:20s}: {backend.num_qubits:3d} qubits")
            except:
                print(f"   • {backend.name}: info unavailable")
except Exception as e:
    print(f"   Error listing backends: {e}")

# Get least busy
if backends:
    try:
        # Sort by queue size
        backend = min(backends, key=lambda b: b.status().pending_jobs)
        print(f"\n✅ Least busy: {backend.name}")
        print(f"   Queue: {backend.status().pending_jobs} jobs")
    except Exception as e:
        print(f"\n❌ Could not determine least busy: {e}")

print("\n✅ Connection test complete!")
