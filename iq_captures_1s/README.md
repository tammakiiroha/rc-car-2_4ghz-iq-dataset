# iq_captures_1s/ — HackRF 主録音 / Primary Raw IQ Recordings

## このフォルダの内容 / What this folder contains

論文で評価した 5 つの操作について、**HackRF One** で 2.475 GHz を約 1 秒ずつ録音した
生 IQ データ（論文 表 1: `取得長 ≈ 1 s/操作`、`フレーム数 ≈ 50 frame/操作`）。

各ファイル = 正規リモコンを ~1 秒押下しながら HackRF で受信し、`.complex16s` として保存。
1 ファイル内に **24-byte 完全フレームを複数含む**（論文 §4.1）。

Raw IQ data recorded with **HackRF One** for the 5 operations evaluated in the paper.
Each file is ~1 s of capture at 2.475 GHz containing multiple complete 24-byte frames.

## 録音パラメータ / Recording Parameters（全ファイル統一）

- 中心周波数 / Center frequency: **2.475 GHz**
- サンプリングレート / Sample rate: **2 Msps**
- 受信帯域幅 / Receive bandwidth: **2 MHz**
- RX Gain: **20 dB**
- データ形式 / Format: **interleaved signed 8-bit IQ**（1 byte/I + 1 byte/Q = **2 bytes/sample**）
  - 拡張子は `.complex16s` だが実体は 8-bit。`../scripts/verify_signal_captures.py` 内の
    コメントを参照。

## ファイル一覧（操作 → tail 対応）/ File List (Operation → tail mapping)

| ファイル / Filename | 操作 / Operation | tail (5 bytes) | 録音長 / Duration | サイズ / Size |
|---|---|---|---:|---:|
| `HackRF-Left forward-2_475GHz-2MSps-2MHz.complex16s`  | **左輪前進 / Left forward (LF)**  | `22 52 d8 57 80` | 4.194 s | 16,777,216 B |
| `HackRF-Left backward-2_475GHz-2MSps-2MHz.complex16s` | **左輪後退 / Left backward (LB)** | `24 54 9a 27 00` | 4.325 s | 17,301,504 B |
| `HackRF-Right forward-2_475GHz-2MSps-2MHz.complex16s` | **右輪前進 / Right forward (RF)** | `27 57 ff 17 00` | 3.932 s | 15,728,640 B |
| `HackRF-Right backward-2_475GHz-2MSps-2MHz.complex16s` | **右輪後退 / Right backward (RB)** | `26 d6 4d 8f 00` | 4.260 s | 17,039,360 B |
| `HackRF-Light-2_475GHz-2MSps-2MHz.complex16s`         | **ライト / Light**                | `06 36 b6 47 00` | 3.473 s | 13,893,632 B |
| `New1 HackRF-Left backward-...complex16s` | LB 切片（約 1 フレーム）/ LB cropped (~1 frame) | LB と同じ | 0.0002 s | 782 B |
| `New2 HackRF-Left backward-...complex16s` | LB 切片（約 1 フレーム）/ LB cropped (~1 frame) | LB と同じ | 0.0002 s | 786 B |

> `New1` / `New2` は LB 録音から切り出した単一フレーム規模のスニペットです。
> 論文では直接引用されていませんが、切り出し作業の中間生成物として保管しています。
> The `New1` / `New2` files are sub-frame snippets cut from the LB recording during early
> slicing experiments. Not directly cited in the paper.

## 録音日 / Recording Date

2025-07-16 (HackRF タイムスタンプ / HackRF timestamps)

## SHA-256 完整性確認 / Integrity

```bash
shasum -a 256 -c checksums.sha256
```

## IQ ファイルの読み込み / How to Read

```python
import numpy as np
raw = np.fromfile("HackRF-Left forward-2_475GHz-2MSps-2MHz.complex16s", dtype=np.int8)
iq  = raw.reshape(-1, 2).astype(np.float32)
samples = iq[:, 0] + 1j * iq[:, 1]   # complex baseband, fs=2 Msps, fc=2.475 GHz
```
