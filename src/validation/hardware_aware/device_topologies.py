"""
Device coupling maps for major quantum hardware providers
"""

# IBM Heavy-Hex topologies
ibm_brisbane = {
    'name': 'ibm_brisbane',
    'qubits': 127,
    'coupling': [(i, i+1) for i in range(126)] + [(i, i+2) for i in range(0, 126, 2)]
}

ibm_kyoto = {
    'name': 'ibm_kyoto',
    'qubits': 127,
    'coupling': [(i, i+1) for i in range(126)] + [(i, i+2) for i in range(0, 126, 2)]
}

ibm_fez = {
    'name': 'ibm_fez',
    'qubits': 156,
    'coupling': [(i, i+1) for i in range(155)]
}

# Rigetti topologies
rigetti_aspen = {
    'name': 'rigetti_aspen',
    'qubits': 80,
    'coupling': [(i, i+1) for i in range(79)] + [(0, 79)]
}

# IonQ full connectivity
ionq_harmony = {
    'name': 'ionq_harmony',
    'qubits': 11,
    'coupling': [(i, j) for i in range(11) for j in range(i+1, 11)]  # All-to-all
}

# Get coupling map by name
def get_coupling_map(device_name='ibm_fez'):
    devices = {
        'ibm_brisbane': ibm_brisbane,
        'ibm_kyoto': ibm_kyoto,
        'ibm_fez': ibm_fez,
        'rigetti_aspen': rigetti_aspen,
        'ionq_harmony': ionq_harmony
    }
    return devices.get(device_name, ibm_fez)

# List available devices
def list_devices():
    return ['ibm_brisbane', 'ibm_kyoto', 'ibm_fez', 'rigetti_aspen', 'ionq_harmony']

if __name__ == "__main__":
    print("📡 Available devices:")
    for device in list_devices():
        coupling = get_coupling_map(device)
        print(f"  • {device}: {coupling['qubits']} qubits")
