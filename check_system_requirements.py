"""
Check system requirements for IPL ML training
"""
import psutil
import os
import numpy as np

def check_system_requirements():
    """Check if system can handle IPL training"""
    
    print("=" * 60)
    print("IPL ML TRAINING - SYSTEM REQUIREMENTS CHECK")
    print("=" * 60)
    print()
    
    # CPU
    cpu_count = psutil.cpu_count()
    cpu_freq = psutil.cpu_freq()
    print(f"CPU Cores: {cpu_count}")
    if cpu_freq:
        print(f"CPU Frequency: {cpu_freq.max:.2f} GHz")
    print()
    
    # Memory
    mem = psutil.virtual_memory()
    print(f"Total RAM: {mem.total / (1024**3):.2f} GB")
    print(f"Available RAM: {mem.available / (1024**3):.2f} GB")
    print(f"Memory Usage: {mem.percent}%")
    print()
    
    # Disk
    disk = psutil.disk_usage('/')
    print(f"Total Disk Space: {disk.total / (1024**3):.2f} GB")
    print(f"Available Disk Space: {disk.free / (1024**3):.2f} GB")
    print()
    
    # GPU (if available)
    try:
        import torch
        if torch.cuda.is_available():
            print(f"GPU: {torch.cuda.get_device_name(0)}")
            print(f"GPU Memory: {torch.cuda.get_device_properties(0).total_memory / (1024**3):.2f} GB")
        else:
            print("GPU: Not available (CPU-only training)")
    except ImportError:
        print("GPU: PyTorch not installed (CPU-only training)")
    print()
    
    # Assessment
    print("=" * 60)
    print("REQUIREMENTS ASSESSMENT")
    print("=" * 60)
    print()
    
    # Minimum requirements
    min_ram_gb = 8
    min_disk_gb = 10
    min_cpu_cores = 4
    
    ram_ok = mem.total / (1024**3) >= min_ram_gb
    disk_ok = disk.free / (1024**3) >= min_disk_gb
    cpu_ok = cpu_count >= min_cpu_cores
    
    print(f"Minimum RAM Required: {min_ram_gb} GB")
    print(f"Your RAM: {mem.total / (1024**3):.2f} GB")
    print(f"Status: {'✓ OK' if ram_ok else '❌ INSUFFICIENT'}")
    print()
    
    print(f"Minimum Disk Space Required: {min_disk_gb} GB")
    print(f"Your Available Disk: {disk.free / (1024**3):.2f} GB")
    print(f"Status: {'✓ OK' if disk_ok else '❌ INSUFFICIENT'}")
    print()
    
    print(f"Minimum CPU Cores Required: {min_cpu_cores}")
    print(f"Your CPU Cores: {cpu_count}")
    print(f"Status: {'✓ OK' if cpu_ok else '❌ INSUFFICIENT'}")
    print()
    
    if ram_ok and disk_ok and cpu_ok:
        print("✓ YOUR PC CAN HANDLE IPL TRAINING")
    else:
        print("❌ YOUR PC MAY STRUGGLE WITH IPL TRAINING")
    
    print()
    print("=" * 60)
    print("TRAINING TIME ESTIMATES")
    print("=" * 60)
    print()
    
    # Estimate training time based on CPU
    base_time_per_sample = 0.001  # 1ms per sample on reference CPU
    cpu_factor = 4.0 / cpu_count  # Normalize to 4 cores
    
    dataset_sizes = [1000, 10000, 50000, 100000]
    
    for size in dataset_sizes:
        estimated_time = size * base_time_per_sample * cpu_factor
        print(f"Dataset Size: {size:,} samples")
        print(f"Estimated Training Time: {estimated_time/60:.1f} minutes")
        print()

if __name__ == "__main__":
    check_system_requirements()
