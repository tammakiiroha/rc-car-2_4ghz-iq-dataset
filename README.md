# 2.4 GHz リモコン玩具カー リバースエンジニアリング — 生 IQ データセット

論文付属データ:

> **ソフトウェア無線を用いた市販 2.4 GHz 車型玩具のリバースエンジニアリング**
> ロ メイトウ（東京都市大学）, 朱 金暁（東京電機大学）

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

[English version below ↓](#english-version)

---

## 概要

本リポジトリは論文 §4.1（フレーム構造の同定）で用いた **HackRF による生 IQ 録音**、
**URH 復調設定**、および **検証スクリプト** を含みます。

## ディレクトリ構成

```
experiment_data/
├── README.md                         本ファイル（概要）
├── EXPERIMENT_DATA_INDEX.md          詳細索引（パラメータ・SHA-256 一覧）
├── COVERAGE.md                       本データセットが論文のどの主張を支持するか
├── LICENSE                           CC BY 4.0
├── CITATION.cff                      引用メタデータ
│
├── iq_captures_1s/                   主録音（HackRF, 約 1 秒/操作）
│   ├── README.md
│   ├── checksums.sha256
│   ├── HackRF-Left forward-...complex16s    左輪前進 (LF)
│   ├── HackRF-Left backward-...complex16s   左輪後退 (LB)
│   ├── HackRF-Right forward-...complex16s   右輪前進 (RF)
│   ├── HackRF-Right backward-...complex16s  右輪後退 (RB)
│   ├── HackRF-Light-...complex16s           ライト (light)
│   └── New1 / New2 ...complex16s            単一フレーム規模の切片
│
├── iq_bursts_extracted/              フレーム検証用 単一バースト
│   ├── README.md
│   ├── checksums.sha256
│   └── {left,right} {forward,back}.complex16s, light.complex16s
│
├── urh_project/                      URH v2.10.0 プロジェクトファイル
│   ├── README.md
│   └── URHProject.xml
│
└── scripts/                          検証スクリプト
    ├── README.md
    └── verify_signal_captures.py
```

## 録音条件（全ファイル共通）

| 項目 | 値 |
|---|---:|
| 中心周波数 fc | **2.475 GHz** |
| サンプリングレート fs | **2 Msps** |
| 受信帯域幅 BW | **2 MHz** |
| 変調方式 | FSK (1 bit/symbol, 2 sps) |
| データ形式 | interleaved signed 8-bit IQ（拡張子 `.complex16s`、実体は 8-bit）|
| SDR | HackRF One (HW r10), Firmware 2024.02.1 |
| ソフトウェア | URH v2.10.0 / Ubuntu 17.10 (kernel 4.13.0) |
| RX / TX Gain | 20 dB / 20 dB |
| TX–RX 距離 | 約 30 cm |

## フレームモデル（本リポジトリで検証可能）

```
1 フレーム = 24 bytes (192 bits)
          = [固定ヘッダ 19 bytes] || [操作依存 tail 5 bytes]

固定ヘッダ（全コマンド共通）:
  20 aa b8 24 ca eb da 25 da 70 20 cf 6e 76 b6 7c de 28 c7

本リポジトリで提供する 5 つの tail:
  light                06 36 b6 47 00
  左輪前進 (LF)         22 52 d8 57 80
  左輪後退 (LB)         24 54 9a 27 00
  右輪前進 (RF)         27 57 ff 17 00
  右輪後退 (RB)         26 d6 4d 8f 00
```

> **本データセットの範囲について**
> 本リリースは論文 §4.1（フレーム構造）および §4.2（`m_L`, `m_R` の差分マスク導出）を
> 直接支持します。`demo`、両輪前進・後退、`LB+RF` / `RB+LF`（合成回転）、非受理 tail
> `t_inv`、合成 forgery tail、replay/forgery 試行ログ、スペクトラムスイープは
> **含まれていません**。詳細は [`COVERAGE.md`](COVERAGE.md) を参照。

## クイックスタート

### 必要環境
- Python ≥ 3.9
- NumPy

### 完整性確認

```bash
cd iq_captures_1s        && shasum -a 256 -c checksums.sha256
cd ../iq_bursts_extracted && shasum -a 256 -c checksums.sha256
```

### 検証スクリプト実行

```bash
python3 scripts/verify_signal_captures.py
```

スクリプトは `iq_bursts_extracted/` の各バーストを復調・整列・24 bytes フレーム切り出し・
5 bytes tail 抽出を行い、期待値との比較表を出力します。

### IQ ファイルの読み込み（参考コード）

```python
import numpy as np

raw = np.fromfile("iq_captures_1s/HackRF-Left forward-2_475GHz-2MSps-2MHz.complex16s",
                  dtype=np.int8)
iq = raw.reshape(-1, 2).astype(np.float32)
samples = iq[:, 0] + 1j * iq[:, 1]   # complex baseband, fs = 2 Msps, fc = 2.475 GHz
```

## リポジトリ容量と Git LFS について

主録音 5 ファイルは各 13–17 MB（合計約 78 MB）。標準の `git` でも問題ありませんが、
今後録音を追加する場合は **Git LFS の使用を推奨** します:

```bash
git lfs install
git lfs track "*.complex16s"
git add .gitattributes
```

## ライセンス

[Creative Commons Attribution 4.0 International (CC BY 4.0)](LICENSE)

## 引用

[`CITATION.cff`](CITATION.cff) を参照。本データセットを用いる場合は付属論文を引用してください。

---

<a id="english-version"></a>
## English Version

This repository contains the **raw IQ recordings**, **URH demodulation settings**, and a
**verification script** used to identify the 24-byte frame structure described in §4.1
of the paper:

> **Reverse Engineering of a Commercial 2.4 GHz RC Toy Car Using Software Defined Radio**
> Meitou Ro (Tokyo City University), Jinxiao Zhu (Tokyo Denki University)

### Folder structure

```
experiment_data/
├── README.md                         this file
├── EXPERIMENT_DATA_INDEX.md          detailed parameter / file index
├── COVERAGE.md                       which paper claims this release does (and does not) support
├── LICENSE                           CC BY 4.0
├── CITATION.cff                      citation metadata
│
├── iq_captures_1s/                   primary HackRF recordings (~1 s per operation)
├── iq_bursts_extracted/              single-frame bursts for verification
├── urh_project/                      URH v2.10.0 project file
└── scripts/                          verification script
```

### Recording parameters (uniform)

| | Value |
|---|---:|
| Center frequency `fc` | **2.475 GHz** |
| Sample rate `fs` | **2 Msps** |
| Receive bandwidth `BW` | **2 MHz** |
| Modulation | FSK (1 bit/sym, 2 sps) |
| File format | interleaved signed 8-bit IQ (`.complex16s`) |
| SDR | HackRF One (HW r10), Firmware 2024.02.1 |
| Software | URH v2.10.0 on Ubuntu 17.10 (kernel 4.13.0) |
| RX / TX gain | 20 dB / 20 dB |
| TX–RX distance | ~30 cm |

### Frame model verified by this release

```
1 frame = 24 bytes (192 bits)
        = [19-byte fixed header] || [5-byte operation-dependent tail]

Fixed header (common to all commands):
  20 aa b8 24 ca eb da 25 da 70 20 cf 6e 76 b6 7c de 28 c7

Tails covered by this release:
  light                06 36 b6 47 00
  Left forward (LF)    22 52 d8 57 80
  Left backward (LB)   24 54 9a 27 00
  Right forward (RF)   27 57 ff 17 00
  Right backward (RB)  26 d6 4d 8f 00
```

> **Coverage notice.** This release supports paper §4.1 (frame structure) and §4.2 partial.
> It does **not** include raw IQ for `demo`, Both-Forward/Backward, `LB+RF`, `RB+LF`,
> the non-accepted tail `t_inv`, synthesised forgery tails, replay/forgery trial logs, or
> the spectrum sweep. See [`COVERAGE.md`](COVERAGE.md) for full details.

### Quick start

```bash
# integrity check
cd iq_captures_1s        && shasum -a 256 -c checksums.sha256
cd ../iq_bursts_extracted && shasum -a 256 -c checksums.sha256

# run the verification script
python3 scripts/verify_signal_captures.py
```

### Read an IQ file from your own code

```python
import numpy as np
raw = np.fromfile("iq_captures_1s/HackRF-Left forward-2_475GHz-2MSps-2MHz.complex16s",
                  dtype=np.int8)
iq = raw.reshape(-1, 2).astype(np.float32)
samples = iq[:, 0] + 1j * iq[:, 1]   # complex baseband at fs = 2 Msps, fc = 2.475 GHz
```

### License

Released under [Creative Commons Attribution 4.0 International (CC BY 4.0)](LICENSE).

### Citation

See [`CITATION.cff`](CITATION.cff). If you use this dataset, please cite the
accompanying paper.
