# iq_bursts_extracted/ — Extracted Single-Frame Bursts

## What this folder contains

Short bursts **cropped from the primary recordings in `../iq_captures_1s/`**.
Each file contains only one (or a few) complete 24-byte frame(s) and is used to:

- Verify the paper's frame model: **`19-byte fixed header || 5-byte tail`**
- Provide test inputs for `../scripts/verify_signal_captures.py` (the reference implementation)

Paper reference: 論文 §4.1 (フレーム構造の同定).

## File List — "Operation → expected tail" mapping

`verify_signal_captures.py` decodes each file, aligns to the 24-byte frame,
extracts the 5-byte tail, and compares it against the "expected tail" column below:

| Filename | Operation | Expected tail (5 bytes) | File size |
|---|---|---|---:|
| `left forward.complex16s`  | **Left wheel forward (LF)**  | `22 52 d8 57 80` | 41,598 B  |
| `left back.complex16s`     | **Left wheel backward (LB)** | `24 54 9a 27 00` | 231,132 B |
| `right forward.complex16s` | **Right wheel forward (RF)** | `27 57 ff 17 00` | 243,974 B |
| `right back.complex16s`    | **Right wheel backward (RB)**| `26 d6 4d 8f 00` | 21,998 B  |
| `light.complex16s`         | **Light**                    | `06 36 b6 47 00` | 247,722 B |

Fixed 19-byte header (common to all commands):
`20 aa b8 24 ca eb da 25 da 70 20 cf 6e 76 b6 7c de 28 c7`

## File Format

Same as `iq_captures_1s/`: **interleaved signed 8-bit IQ**, 2 Msps, 2 bytes/sample.

## Extraction Date

2025-10-09.

## SHA-256 Integrity

See `checksums.sha256`.

## Usage — run the verification script

```bash
cd ../scripts
python3 verify_signal_captures.py
```

The script reads all 5 files in this folder, demodulates them, aligns to 24-byte frames,
extracts the tail, and compares against the expected values.
A "best segment score" near 1.0 indicates the frame model holds.
