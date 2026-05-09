# iq_captures_1s/ — Primary Raw IQ Recordings (HackRF)

## What this folder contains

Raw IQ data recorded with **HackRF One** for the 5 operations evaluated in the paper.
論文 表1 lists `取得長 ≈ 1 s/操作` (recording length ≈ 1 s per operation) and `フレーム数 ≈ 50 frame/操作`
(approximately 50 frames per recording) — these files are exactly that data.

Each file = press a key on the legitimate remote for ~1 s while HackRF receives at 2.475 GHz
and saves the raw IQ stream as `.complex16s`.
The files contain **multiple complete 24-byte frames** (论文 §4.1).

## Recording Parameters (uniform across all files)

- Center frequency: **2.475 GHz**
- Sample rate: **2 Msps**
- Receive bandwidth: **2 MHz**
- RX Gain: **20 dB**
- Format: **interleaved signed 8-bit IQ** (1 byte/I + 1 byte/Q = **2 bytes/sample**)
  - Note: the `.complex16s` extension is misleading — payload is actually 8-bit.
    See comment in `../scripts/verify_signal_captures.py` for the correct decoding.

## File List — "Operation → tail" mapping

| Filename | Operation recorded | Expected tail (5 bytes) | Duration | File size |
|---|---|---|---:|---:|
| `HackRF-Left forward-2_475GHz-2MSps-2MHz.complex16s`  | **Left wheel forward (LF)**  | `22 52 d8 57 80` | 4.194 s | 16,777,216 B |
| `HackRF-Left backward-2_475GHz-2MSps-2MHz.complex16s` | **Left wheel backward (LB)** | `24 54 9a 27 00` | 4.325 s | 17,301,504 B |
| `HackRF-Right forward-2_475GHz-2MSps-2MHz.complex16s` | **Right wheel forward (RF)** | `27 57 ff 17 00` | 3.932 s | 15,728,640 B |
| `HackRF-Right backward-2_475GHz-2MSps-2MHz.complex16s` | **Right wheel backward (RB)** | `26 d6 4d 8f 00` | 4.260 s | 17,039,360 B |
| `HackRF-Light-2_475GHz-2MSps-2MHz.complex16s`         | **Light**                    | `06 36 b6 47 00` | 3.473 s | 13,893,632 B |
| `New1 HackRF-Left backward-...complex16s` | LB cropped to ~1 frame | same as LB | 0.0002 s | 782 B |
| `New2 HackRF-Left backward-...complex16s` | LB cropped to ~1 frame | same as LB | 0.0002 s | 786 B |

> The `New1` / `New2` files are sub-frame snippets cut from the LB recording during early
> slicing experiments. They are **not directly cited in the paper** but are kept here as
> intermediate cropping artifacts.

## Recording Date

2025-07-16 (HackRF timestamps).

## SHA-256 Integrity

See `checksums.sha256` in this folder. Verify with:

```bash
shasum -a 256 -c checksums.sha256
```

## How to Read These IQ Files

```python
import numpy as np
raw = np.fromfile("HackRF-Left forward-2_475GHz-2MSps-2MHz.complex16s", dtype=np.int8)
iq  = raw.reshape(-1, 2).astype(np.float32)
samples = iq[:, 0] + 1j * iq[:, 1]   # complex baseband, fs=2 Msps, fc=2.475 GHz
```
