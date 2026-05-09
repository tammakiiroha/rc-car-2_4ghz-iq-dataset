# urh_project/ — URH Project File (Demodulation & Alignment Settings)

## What this folder contains

`URHProject.xml` is the **Universal Radio Hacker (URH) v2.10.0** project file
saved after opening the primary IQ recording
(`../iq_captures_1s/HackRF-Left backward-2_475GHz-2MSps-2MHz.complex16s` and others)
and configuring the FSK demodulation parameters.

論文 表2 (測定・復調パラメータ) describes
"フレーム整列基準 = プリアンブル検出点を基準に切り出し（URH 上で固定）" —
the fixed URH parameters referenced there are stored in this XML.

## Key Parameters (signal element)

| Item | Value |
|---|---:|
| Modulation | FSK |
| Bits per symbol | 1 |
| Samples per symbol | 2 |
| Sample rate (URH internal) | 1,000,000 Hz |
| Pause threshold | 8 |
| Noise threshold | 1.4143 |
| Costas loop bandwidth | 0.1 |

## Supported Decodings

URH project enables:
`Non Return To Zero (NRZ)` / `NRZ + Invert` / `Manchester I` / `Manchester II` / `Differential Manchester`

## Notes / Caveats

- The `<device_conf>` block stores `frequency=433920000` and `name=USRP` — these are URH's
  default values, **not** the parameters used for capture. The actual recordings were made
  with **HackRF One @ 2.475 GHz** via standalone tools (e.g. `hackrf_transfer`); see
  `../iq_captures_1s/README.md`.
- This XML primarily records the demodulation/analysis settings applied **after** loading the
  IQ files into URH.

## How to Reproduce

1. Install URH v2.10.0.
2. Open URH → `Project → Open` → select `URHProject.xml`.
3. URH references IQ files via the relative path `Data/HackRF-...complex16s`.
   Either:
   - Copy the files from `../iq_captures_1s/` into a `Data/` subdirectory next to this XML, or
   - Edit each `<signal filename="...">` and `<open_file name="...">` to point to absolute paths.
