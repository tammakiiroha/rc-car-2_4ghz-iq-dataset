# EXPERIMENT_DATA_INDEX — Detailed Index

Paper: `../Reverse_Engineering/Reverse Engineering.tex`
Last updated: 2026-05-09

> This index lists every **raw IQ file**, **URH setting**, and **verification script**
> actually used in the submitted manuscript.
> Every file is annotated with its corresponding paper section, operation class,
> and recording parameters. Nothing unrelated to this paper is included.

---

## 1. iq_captures_1s/ — Primary Raw IQ Recordings

**What**: Raw IQ data captured by HackRF One at 2.475 GHz while the legitimate remote was held
for ~1 s on each of 5 operations (論文 表1: `取得長 ≈ 1 s/操作`).

**Paper reference**: §3.2 (測定環境と信号処理) + 表1 (Experimental conditions) + 表2 (Measurement parameters)

| # | Filename | Operation recorded | Tail (5 bytes) | Size | Duration | Recorded |
|---|---|---|---|---:|---:|---|
| 1 | `HackRF-Left forward-2_475GHz-2MSps-2MHz.complex16s`  | **Left forward (LF)**  | `22 52 d8 57 80` | 16,777,216 B | 4.194 s | 2025-07-16 10:59:12 |
| 2 | `HackRF-Left backward-2_475GHz-2MSps-2MHz.complex16s` | **Left backward (LB)** | `24 54 9a 27 00` | 17,301,504 B | 4.325 s | 2025-07-16 10:59:53 |
| 3 | `HackRF-Right forward-2_475GHz-2MSps-2MHz.complex16s` | **Right forward (RF)** | `27 57 ff 17 00` | 15,728,640 B | 3.932 s | 2025-07-16 11:00:45 |
| 4 | `HackRF-Right backward-2_475GHz-2MSps-2MHz.complex16s`| **Right backward (RB)**| `26 d6 4d 8f 00` | 17,039,360 B | 4.260 s | 2025-07-16 11:01:41 |
| 5 | `HackRF-Light-2_475GHz-2MSps-2MHz.complex16s`         | **Light**              | `06 36 b6 47 00` | 13,893,632 B | 3.473 s | 2025-07-16 10:58:21 |
| 6 | `New1 HackRF-Left backward-...complex16s` | LB cropped (~1 frame) | same as LB | 782 B | 0.0002 s | 2025-07-16 11:39:21 |
| 7 | `New2 HackRF-Left backward-...complex16s` | LB cropped (~1 frame) | same as LB | 786 B | 0.0002 s | 2025-07-16 11:39:16 |

Recording parameters (uniform across the 5 main files):
- fc = 2.475 GHz, fs = 2 Msps, BW = 2 MHz, RX Gain = 20 dB
- Format: interleaved signed 8-bit IQ (1 byte/I + 1 byte/Q = 2 bytes/sample)

SHA-256 file: `iq_captures_1s/checksums.sha256`

---

## 2. iq_bursts_extracted/ — Single-Frame Bursts (verification inputs)

**What**: Short bursts cropped from the recordings above; each file holds one (or a few)
complete 24-byte frames. Used to verify the `19-byte header || 5-byte tail` frame model.

**Paper reference**: §4.1 (フレーム構造の同定) — empirical confirmation of `f = h || t`.

| # | Filename | Operation | Expected `PREFIX_HEX || tail` | Size | Extracted |
|---|---|---|---|---:|---|
| 1 | `left forward.complex16s`  | **Left forward (LF)**  | `…cde28c7 \| 22 52 d8 57 80` | 41,598 B  | 2025-10-09 14:08:23 |
| 2 | `left back.complex16s`     | **Left backward (LB)** | `…cde28c7 \| 24 54 9a 27 00` | 231,132 B | 2025-10-09 14:09:30 |
| 3 | `right forward.complex16s` | **Right forward (RF)** | `…cde28c7 \| 27 57 ff 17 00` | 243,974 B | 2025-10-09 14:03:28 |
| 4 | `right back.complex16s`    | **Right backward (RB)**| `…cde28c7 \| 26 d6 4d 8f 00` | 21,998 B  | 2025-10-09 14:04:52 |
| 5 | `light.complex16s`         | **Light**              | `…cde28c7 \| 06 36 b6 47 00` | 247,722 B | 2025-10-09 13:58:31 |

Fixed 19-byte prefix: `20 aa b8 24 ca eb da 25 da 70 20 cf 6e 76 b6 7c de 28 c7`

SHA-256 file: `iq_bursts_extracted/checksums.sha256`

---

## 3. urh_project/URHProject.xml — URH Demodulation Settings

**What**: URH v2.10.0 project file capturing the FSK demodulation parameters.
**Paper reference**: 表2 (Measurement and demodulation parameters) + 図3 (URH analysis screen).

| Item | Value | Maps to 表2 row |
|---|---:|---|
| Modulation | FSK | "変調方式" |
| Bits/Symbol | 1 | "変調方式 (Bits/Symbol=1)" |
| Samples/Symbol | 2 | "Samples/Symbol" |
| Sample rate (URH internal) | 1,000,000 Hz | (internal analysis rate; capture was 2 Msps) |
| Pause threshold | 8 | — |
| Noise threshold | 1.4143 | — |
| Costas loop bandwidth | 0.1 | — |
| Decodings enabled | NRZ / NRZ+Inv / Manchester I/II / Differential Manchester | — |

> Note: the `<device_conf>` block stores `name=USRP` and `frequency=433920000` (URH defaults).
> The actual capture used HackRF + 2.475 GHz with `hackrf_transfer`-style tools, separate from
> this project file.

---

## 4. scripts/verify_signal_captures.py — Verification Script

**What**: Reads each burst in `iq_bursts_extracted/`, demodulates, aligns to 24-byte frames,
extracts the 5-byte tail, and matches against the expected tail.
**Paper reference**: §4.1 (frame structure identification).

Hardcoded reference values:

```python
PREFIX_HEX        = "20aab824caebda25da7020cf6e76b67cde28c7"   # 19-byte fixed header
ADDRESS_HEX       = "b824caebda"                               # 5-byte address inside header
FIXED9_BITS       = "001001011"
PAYLOAD_FIXED_HEX = "b4e0419edced6cf9bc518e"

CAPTURES = {
    "left back.complex16s":     "24549a2700",   # LB
    "left forward.complex16s":  "2252d85780",   # LF
    "light.complex16s":         "0636b64700",   # light
    "right back.complex16s":    "26d64d8f00",   # RB
    "right forward.complex16s": "2757ff1700",   # RF
}
```

Run:

```bash
cd experiment_data        # repository root
python3 scripts/verify_signal_captures.py
```

---

## 5. Recording Conditions Summary (論文 表1)

| Item | Value |
|---|---|
| OS | Linux Ubuntu 17.10 (kernel 4.13.0-generic) |
| URH | v2.10.0 |
| `hackrf_info` | 2023.01.1 |
| libhackrf | 2023.01.1 (0.8) |
| HackRF Firmware | 2024.02.1 (API 1.08) |
| SDR HW | HackRF One (HW rev r10) |
| RX / TX Gain | 20 dB / 20 dB |
| TX–RX distance | ~30 cm |
| Antenna height | ~40 cm |
| Antenna | 2.4 GHz whip (model unspecified) |
| Capture environment | Outdoor (low noise) |
| Replay environment | Indoor lab (noise/interference present) |
| Capture duration | ~1 s/operation |
| Frames per recording | ~50 frames (target) |

## 6. Measurement / Demodulation Parameters (論文 表2)

| Item | Value |
|---|---|
| Center frequency fc | 2.475 GHz |
| Modulation | FSK (Bits/Symbol=1) |
| Sample rate fs | 2 Msps |
| Samples/Symbol | 2 |
| Receive bandwidth BW | 2 MHz |
| URH frequency deviation | 101.562 kHz / 203.125 kHz |
| Estimated symbol rate | ~1 Msym/s (fs/SPS) |
| Frame alignment | preamble-detection point |

---

## 7. Frame Model (論文 §4.1)

```
1 frame = 24 bytes (192 bits) = h || t

  h (19-byte fixed header, common to all commands):
     20 aa b8 24 ca eb da 25 da 70 20 cf 6e 76 b6 7c de 28 c7

  t (5-byte variable tail):
     light                  06 36 b6 47 00
     demo                   36 46 cd 45 00
     Left forward (LF)      22 52 d8 57 80
     Left backward (LB)     24 54 9a 27 00
     Right forward (RF)     27 57 ff 17 00
     Right backward (RB)    26 d6 4d 8f 00
     Both forward           23 53 fb 47 80
     Both backward          24 d4 0b af 00
     LB+RF (CCW)            25 55 b9 37 00
     RB+LF (CW)             22 d2 49 df 80
```

Differential masks extracted (論文 §4.2):
- m_L (left wheel reversal) = `06 06 42 70 80`
- m_R (right wheel reversal) = `01 81 b2 98 00`
- m_B (both wheel reversal) = `07 87 f0 e8 80` = m_L ⊕ m_R
- v_light (light vector) = `20 60 6a 40 00`

---

## 8. Provenance

All files in this repository were collated from the author's local working directories
on 2026-05-09. Original local copies are retained outside this repository. Raw IQ data
were captured on 2025-07-16; verification bursts were extracted on 2025-10-09.

---

## 9. IQ File Reading Reference Code

```python
import numpy as np

# Read interleaved signed 8-bit IQ
raw = np.fromfile("iq_captures_1s/HackRF-Left forward-2_475GHz-2MSps-2MHz.complex16s",
                  dtype=np.int8)
iq = raw.reshape(-1, 2).astype(np.float32)
samples = iq[:, 0] + 1j * iq[:, 1]
# fs = 2 Msps, fc = 2.475 GHz
```
