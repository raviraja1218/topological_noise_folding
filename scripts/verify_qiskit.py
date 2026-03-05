import sys
print(f"Python version: {sys.version}")

try:
    import qiskit
    print(f"✅ Qiskit version: {qiskit.__version__}")
except ImportError as e:
    print(f"❌ Qiskit import failed: {e}")

try:
    from qiskit import IBMQ
    print("✅ IBMQ module available")
except ImportError as e:
    print(f"❌ IBMQ import failed: {e}")

try:
    from qiskit.providers.ibmq import least_busy
    print("✅ least_busy function available")
except ImportError as e:
    print(f"❌ least_busy import failed: {e}")

try:
    import qiskit_aer
    print(f"✅ Aer version: {qiskit_aer.__version__}")
except ImportError as e:
    print(f"❌ Aer import failed: {e}")

print("\n📦 Installed packages:")
!pip list | grep qiskit
