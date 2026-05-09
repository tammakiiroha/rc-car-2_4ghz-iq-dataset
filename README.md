# Reverse Engineering of a 2.4 GHz RC Toy Car — Raw IQ Dataset

Companion dataset for the paper:

> **Reverse Engineering of a Commercial 2.4 GHz RC Toy Car Using Software Defined Radio**
> Meitou Ro (Tokyo City University), Jinxiao Zhu (Tokyo Denki University)

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

## What is in this repository

This repository contains the **raw IQ recordings**, **URH demodulation settings**, and a
**verification script** used to identify the 24-byte frame structure described in
§4.1 of the paper.

```
experiment_data/
├── README.md                         this file
├── EXPERIMENT_DATA_INDEX.md          detailed parameter / file index
├── COVERAGE.md                       which paper claims this release does (and does not) support
├── LICENSE                           CC BY 4.0
├── CITATION.cff                      citation metadata
├── .gitattributes / .gitignore       Git configuration
│
├── iq_captures_1s/                   primary HackRF recordings (~1 s per operation)
│   ├── README.md
│   ├── checksums.sha256
│   ├── HackRF-Left forward-...complex16s    (LF)
│   ├── HackRF-Left backward-...complex16s   (LB)
│   ├── HackRF-Right forward-...complex16s   (RF)
│   ├── HackRF-Right backward-...complex16s  (RB)
│   ├── HackRF-Light-...complex16s           (light)
│   └── New1 / New2 ...complex16s            (sub-frame snippets)
│
├── iq_bursts_extracted/              single-frame bursts for verification
│   ├── README.md
│   ├── checksums.sha256
│   └── {left,right} {forward,back}.complex16s, light.complex16s
│
├── urh_project/                      URH v2.10.0 project file
│   ├── README.md
│   └── URHProject.xml
│
└── scripts/                          verification script
    ├── README.md
    └── verify_signal_captures.py
```

## Recording parameters (uniform)

| | Value |
|---|---:|
| Center frequency `fc` | **2.475 GHz** |
| Sample rate `fs` | **2 Msps** |
| Receive bandwidth `BW` | **2 MHz** |
| Modulation | FSK (1 bit/sym, 2 sps) |
| File format | interleaved signed 8-bit IQ (`.complex16s` extension, 8-bit payload) |
| SDR | HackRF One (HW r10), Firmware 2024.02.1 |
| Software | URH v2.10.0 on Ubuntu 17.10 (kernel 4.13.0) |
| RX / TX gain | 20 dB / 20 dB |
| TX–RX distance | ~30 cm |

## Frame model verified by this release

```
1 frame = 24 bytes (192 bits)
        = [19-byte fixed header] || [5-byte operation-dependent tail]

Fixed header (common to all commands):
  20 aa b8 24 ca eb da 25 da 70 20 cf 6e 76 b6 7c de 28 c7

5-byte tails covered by this release:
  light                06 36 b6 47 00
  Left forward (LF)    22 52 d8 57 80
  Left backward (LB)   24 54 9a 27 00
  Right forward (RF)   27 57 ff 17 00
  Right backward (RB)  26 d6 4d 8f 00
```

> **Coverage notice.** This release supports paper §4.1 (frame structure) and
> §4.2 partial (`m_L`, `m_R`). It does **not** include raw IQ for `demo`,
> Both-Forward, Both-Backward, `LB+RF`, `RB+LF`, the non-accepted tail
> `t_inv`, the synthesised forgery tails, the replay/forgery trial logs, or
> the spectrum sweep. See [`COVERAGE.md`](COVERAGE.md) for full details.

## Quick start

### Requirements

- Python ≥ 3.9
- NumPy

### Verify integrity

```bash
cd iq_captures_1s        && shasum -a 256 -c checksums.sha256
cd ../iq_bursts_extracted && shasum -a 256 -c checksums.sha256
```

### Run the verification script

```bash
python3 scripts/verify_signal_captures.py
```

The script reads the bursts in `iq_bursts_extracted/`, demodulates them, aligns
to 24-byte frames, extracts the 5-byte tail and prints a comparison table.

### Read an IQ file from your own code

```python
import numpy as np

raw = np.fromfile("iq_captures_1s/HackRF-Left forward-2_475GHz-2MSps-2MHz.complex16s",
                  dtype=np.int8)
iq = raw.reshape(-1, 2).astype(np.float32)
samples = iq[:, 0] + 1j * iq[:, 1]   # complex baseband at fs = 2 Msps, fc = 2.475 GHz
```

## Repository size and Git LFS

The five primary recordings are 13–17 MB each (total ~78 MB).
Plain `git` handles these without issue, but **Git LFS is recommended** if you
plan to add more captures over time. To enable:

```bash
git lfs install
git lfs track "*.complex16s"
git add .gitattributes
```

## License

Released under [Creative Commons Attribution 4.0 International (CC BY 4.0)](LICENSE).

## Citation

See [`CITATION.cff`](CITATION.cff). If you use this dataset, please cite the
accompanying paper.
