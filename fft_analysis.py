import json
import os
import matplotlib
# Force background rendering engine to completely eliminate terminal pop-up freezes
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

print("==================================================")
print("     SMART MOTOR CONDITION MONITORING SYSTEM      ")
print("             TASK 6: FFT SPECTRUM ENGINE          ")
print("==================================================")
print("\n")

# ==========================================================
# 1. AUTOMATED DATA INGESTION ENGINE
# ==========================================================
CREDENTIALS_FILE = "firebase-credentials.json"

if os.path.exists(CREDENTIALS_FILE) and os.path.getsize(CREDENTIALS_FILE) > 2:
    print("Live Key Detected! Initializing Firestore cloud data stream...")
    import firebase_admin
    from firebase_admin import credentials, firestore
    
    if not firebase_admin._apps:
        cred = credentials.Certificate(CREDENTIALS_FILE)
        firebase_admin.initialize_app(cred)
        
    db = firestore.client()
    docs = db.collection("motor_telemetry").stream()
    real_json_data = [doc.to_dict() for doc in docs]
    print("Live database stream extraction successful.")
else:
    print("No live cloud keys found yet. Running specification simulation mode...")
    
    # ----------------------------------------------------------
    # HIGH-FREQUENCY METRIC WAVEFORM SIMULATION
    # Simulating a high-frequency sensor capture (1000 Hz Sampling Frequency)
    # ----------------------------------------------------------
    sampling_rate = 1000  # Samples taken per second (Hz)
    duration = 1.0        # Duration of wave window capture in seconds
    t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)
    
    # Target Waveform A: Healthy Baseline (Quiet, low-level white noise)
    np.random.seed(42)
    healthy_signal = 0.2 * np.sin(2 * np.pi * 50 * t) + np.random.normal(0, 0.1, len(t))
    
    # Target Waveform B: Misalignment (Severe 50 Hz fundamental and 100 Hz secondary harmonics)
    misalignment_signal = 2.5 * np.sin(2 * np.pi * 50 * t) + 1.2 * np.sin(2 * np.pi * 100 * t) + np.random.normal(0, 0.2, len(t))
    
    # Target Waveform C: Bearing Failure (High frequency structural shocks ringing at 320 Hz)
    bearing_signal = 0.4 * np.sin(2 * np.pi * 50 * t) + 1.8 * np.sin(2 * np.pi * 320 * t) + np.random.normal(0, 0.4, len(t))
    
    # Pack the simulated high-speed wave indices into lists
    mock_records = []
    for idx in range(len(t)):
        mock_records.append({
            "time_step": t[idx],
            "healthy_vib": healthy_signal[idx],
            "misalignment_vib": misalignment_signal[idx],
            "bearing_vib": bearing_signal[idx]
        })
    real_json_data = mock_records

# Unpack dataset matrix
df = pd.DataFrame(real_json_data)
N = len(df)
fs = 1000 # 1000 Hz Sampling Rate

print("Successfully loaded waveforms.")
print(f"Total Stream Window Datapoints: {df.shape} points captured.")
print("-" * 40 + "\n")

# ==========================================================
# 2. RUN FAST FOURIER TRANSFORMS (FFT)
# ==========================================================
print("Applying Fast Fourier Transform algorithms across fault classes...")

# Generate the frequency X-axis bins scale (Isolating positive spectrum)
frequencies = np.fft.fftfreq(N, 1/fs)[:N//2]

# Compute magnitudes for each operational classification
fft_healthy = (np.abs(np.fft.fft(df['healthy_vib'])) / N)[:N//2] * 2
fft_misalignment = (np.abs(np.fft.fft(df['misalignment_vib'])) / N)[:N//2] * 2
fft_bearing = (np.abs(np.fft.fft(df['bearing_vib'])) / N)[:N//2] * 2

# ==========================================================
# 3. IDENTIFY & DOCUMENT DOMINANT FREQUENCY SIGNATURES
# ==========================================================
print("\n--- IDENTIFYING DOMINANT FREQUENCY SIGNATURES ---")

# Find the peak index values in the frequency ranges
peak_h_idx = np.argmax(fft_healthy)
peak_m_idx = np.argmax(fft_misalignment)
peak_b_idx = np.argmax(fft_bearing)

print(f"Healthy Motor Peak Energy: {frequencies[peak_h_idx]:.1f} Hz (Amplitude: {fft_healthy[peak_h_idx]:.2f} mm/s)")
print(f"Misalignment Motor Peak Energy: {frequencies[peak_m_idx]:.1f} Hz (Amplitude: {fft_misalignment[peak_m_idx]:.2f} mm/s)")
print(f"Bearing Failure Motor Peak Energy: {frequencies[peak_b_idx]:.1f} Hz (Amplitude: {fft_bearing[peak_b_idx]:.2f} mm/s)")
print("-" * 40)

# Save signatures to a documentation table
signature_report = pd.DataFrame({
    'Fault_Classification': ['Healthy Baseline', 'Shaft Misalignment', 'Bearing Degradation'],
    'Dominant_Frequency_Hz': [frequencies[peak_h_idx], frequencies[peak_m_idx], frequencies[peak_b_idx]],
    'Peak_Vibration_Amplitude': [fft_healthy[peak_h_idx], fft_misalignment[peak_m_idx], fft_bearing[peak_b_idx]]
})

script_directory = os.path.dirname(os.path.abspath(__file__))
report_save_path = os.path.join(script_directory, 'dominant_frequency_signatures.csv')
signature_report.to_csv(report_save_path, index=False)
print(f"Analysis logs saved directly to: '{report_save_path}'")

# ==========================================================
# 4. GENERATE INDEPENDENT FFT STACKED PLOTS
# ==========================================================
print("\nRendering stacked FFT Frequency Spectrum charts...")
fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, ncols=1, figsize=(12, 10), sharex=True)

# Plot A: Healthy Spectrum
ax1.plot(frequencies, fft_healthy, color='teal', linewidth=1.5, label='Healthy Spectrum')
ax1.set_title('Profile A: Healthy Motor Frequency Spectrum (Low Energy Baseline)', fontsize=11, fontweight='bold', color='teal')
ax1.set_ylabel('Amplitude (mm/s)')
ax1.grid(True, linestyle='--', alpha=0.5)
ax1.set_xlim(0, 500) # Zooming into 0-500 Hz for high fidelity review

# Plot B: Shaft Misalignment Spectrum
ax2.plot(frequencies, fft_misalignment, color='darkorange', linewidth=1.5, label='Misalignment Spectrum')
ax2.set_title('Profile B: Shaft Misalignment Spectrum (Severe Fundamental & 2nd Harmonic Peaks)', fontsize=11, fontweight='bold', color='darkorange')
ax2.set_ylabel('Amplitude (mm/s)')
ax2.grid(True, linestyle='--', alpha=0.5)

# Plot C: Bearing Failure Spectrum
ax3.plot(frequencies, fft_bearing, color='crimson', linewidth=1.5, label='Bearing Crack Spectrum')
ax3.set_title('Profile C: Bearing Failure Spectrum (High-Frequency Component Degradation)', fontsize=11, fontweight='bold', color='crimson')
ax3.set_xlabel('Frequency (Hz / Cycles per Second)', fontsize=11)
ax3.set_ylabel('Amplitude (mm/s)')
ax3.grid(True, linestyle='--', alpha=0.5)

plt.tight_layout()

image_save_path = os.path.join(script_directory, 'motor_fft_frequency_spectra.png')
plt.savefig(image_save_path, dpi=300, bbox_inches='tight')
plt.close()

print(f"Success! Visual chart profile exported natively to: '{image_save_path}'")
print("==================================================")
