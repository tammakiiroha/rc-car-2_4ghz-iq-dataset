# scripts/ — Verification Script

## What this folder contains

`verify_signal_captures.py` —
**reference implementation / automatic verifier** for the 24-byte frame model.

For each of the 5 single-frame bursts in `../iq_bursts_extracted/`, the script performs:
- 8-bit IQ read
- FM/FSK demodulation
- Bit-stream alignment
- 24-byte frame slicing
- 5-byte tail extraction and comparison with the "expected tail"

Together this confirms the frame model from 論文 §4.1:
**`24-byte frame = 19-byte fixed header || 5-byte operation-dependent tail`**.

## Hardcoded Reference Values (inside the script)

```python
PREFIX_HEX        = "20aab824caebda25da7020cf6e76b67cde28c7"  # 19-byte fixed header
ADDRESS_HEX       = "b824caebda"                              # 5-byte address inside header
FIXED9_BITS       = "001001011"
PAYLOAD_FIXED_HEX = "b4e0419edced6cf9bc518e"

CAPTURES = {                  # 5 burst files → expected tails
    "left back.complex16s":     "24549a2700",   # LB
    "left forward.complex16s":  "2252d85780",   # LF
    "light.complex16s":         "0636b64700",   # light
    "right back.complex16s":    "26d64d8f00",   # RB
    "right forward.complex16s": "2757ff1700",   # RF
}
```

## How to Run

```bash
cd experiment_data        # repository root
python3 scripts/verify_signal_captures.py
```

The script reads `../iq_bursts_extracted/*.complex16s` (paths are resolved relative to this
script's location).
Required dependencies: `numpy`.
