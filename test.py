from camCapture import (
    capture_entropy_blob_sha3_512,
    capture_entropy_blob_shake_256_1024
)
import math
from scipy.special import gammaincc
import matplotlib.pyplot as plt

# -------------------
# Utility functions
# -------------------
def bytes_to_bits(data: bytes):
    bits = []
    for b in data:
        for i in reversed(range(8)):
            bits.append((b >> i) & 1)
    return bits

def frequency_test(bits):
    n = len(bits)
    s = sum([1 if b==1 else -1 for b in bits])
    s_obs = abs(s)/math.sqrt(n)
    p_value = math.erfc(s_obs / math.sqrt(2))
    return p_value

def runs_test(bits):
    n = len(bits)
    pi = sum(bits)/n
    if abs(pi-0.5) > 2/math.sqrt(n):
        return 0.0
    Vn = 1
    for i in range(1, n):
        if bits[i] != bits[i-1]:
            Vn +=1
    p_value = math.erfc(abs(Vn - 2*n*pi*(1-pi))/(2*math.sqrt(2*n)*pi*(1-pi)))
    return p_value

def longest_run_ones(bits):
    max_run = run = 0
    for b in bits:
        if b == 1:
            run += 1
            max_run = max(max_run, run)
        else:
            run = 0
    p_value = math.exp(-max_run/10)
    return p_value

def block_frequency_test(bits, block_size=8):
    n = len(bits)
    num_blocks = n // block_size
    if num_blocks == 0:
        return 0.0
    sum_sq = 0.0
    for i in range(num_blocks):
        block = bits[i*block_size : (i+1)*block_size]
        pi = sum(block) / block_size
        sum_sq += (pi - 0.5) ** 2
    chi2 = 4.0 * block_size * sum_sq
    p_value = gammaincc(num_blocks / 2.0, chi2 / 2.0)
    return p_value

def approximate_entropy_test(bits, m=2):
    n = len(bits)
    def _pattern_freq(m):
        freq = {}
        for i in range(n):
            pattern = tuple(bits[i:i+m])
            if len(pattern)<m:
                pattern += tuple(bits[:m-len(pattern)])
            freq[pattern] = freq.get(pattern,0)+1
        for k in freq:
            freq[k] /= n
        return freq
    freq_m = _pattern_freq(m)
    freq_m1 = _pattern_freq(m+1)
    phi_m = sum([p*math.log(p) for p in freq_m.values()])
    phi_m1 = sum([p*math.log(p) for p in freq_m1.values()])
    ApEn = phi_m - phi_m1
    chi2 = 2*n*(math.log(2) - ApEn)
    p_value = math.exp(-chi2/2)
    return p_value

def run_all_tests(name, data_bytes):
    bits = bytes_to_bits(data_bytes)
    tests = {
        "Frequency Test": frequency_test(bits),
        "Runs Test": runs_test(bits),
        "Block Frequency Test": block_frequency_test(bits),
        "Longest Run of Ones": longest_run_ones(bits),
        "Approximate Entropy Test": approximate_entropy_test(bits)
    }
    print(f"\n===== NIST-like tests for {name} =====")
    for tname, p in tests.items():
        result = "PASS" if p>0.01 else "FAIL"
        print(f"{tname}: p-value={p:.5f} → {result}")
    return tests

# -------------------
# Run multiple iterations & collect data
# -------------------
NUM_RUNS = 20
test_names = ["Frequency Test", "Runs Test", "Block Frequency Test", "Longest Run of Ones", "Approximate Entropy Test"]

sha3_results = {t: [] for t in test_names}
shake_results = {t: [] for t in test_names}

for i in range(NUM_RUNS):
    print(f"\n----- RUN {i+1} -----")

    sha3_hash, err = capture_entropy_blob_sha3_512()
    if not err:
        res = run_all_tests("SHA3-512 Hash", bytes.fromhex(sha3_hash))
        for t in test_names:
            sha3_results[t].append(res[t])

    shake_hash, err = capture_entropy_blob_shake_256_1024()
    if not err:
        res = run_all_tests("SHAKE-256-1024 Hash", bytes.fromhex(shake_hash))
        for t in test_names:
            shake_results[t].append(res[t])

# -------------------
# Plot results
# -------------------
plt.figure(figsize=(15,7))

for i, tname in enumerate(test_names):
    plt.subplot(2, len(test_names)//2 + 1, i+1)
    plt.plot(range(1, NUM_RUNS+1), sha3_results[tname], marker='o', label="SHA3-512")
    plt.plot(range(1, NUM_RUNS+1), shake_results[tname], marker='x', label="SHAKE-256-1024")
    plt.axhline(y=0.01, color='r', linestyle='--', label="Fail Threshold")
    plt.title(tname)
    plt.xlabel("Run")
    plt.ylabel("p-value")
    plt.ylim(0, 1)
    plt.legend()

plt.tight_layout()
plt.show()
