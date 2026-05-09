# iq_bursts_extracted/ — フレーム検証用 単一バースト / Single-Frame Bursts for Verification

## このフォルダの内容 / What this folder contains

`../iq_captures_1s/` の主録音から切り出した代表バースト。各ファイルには
1 つ（または数個）の完全な 24-byte フレームのみを含み、以下の用途に使用:

- 論文のフレームモデル `19-byte 固定ヘッダ || 5-byte tail` の検証
- 参照実装 `../scripts/verify_signal_captures.py` のテスト入力

Short bursts cropped from the primary recordings in `../iq_captures_1s/`.
Each file holds only one (or a few) complete 24-byte frame(s), used to verify
the paper's frame model `19-byte header || 5-byte tail`.

論文対応 / Paper reference: §4.1（フレーム構造の同定）

## ファイル一覧（操作 → 期待 tail）/ File List (Operation → expected tail)

`verify_signal_captures.py` は各ファイルを復調・整列・24-byte フレーム切り出し・
5-byte tail 抽出を行い、下表の "期待 tail" と比較します。

| ファイル / Filename | 操作 / Operation | 期待 tail (5 bytes) | サイズ / Size |
|---|---|---|---:|
| `left forward.complex16s`  | **左輪前進 / Left forward (LF)**  | `22 52 d8 57 80` | 41,598 B  |
| `left back.complex16s`     | **左輪後退 / Left backward (LB)** | `24 54 9a 27 00` | 231,132 B |
| `right forward.complex16s` | **右輪前進 / Right forward (RF)** | `27 57 ff 17 00` | 243,974 B |
| `right back.complex16s`    | **右輪後退 / Right backward (RB)**| `26 d6 4d 8f 00` | 21,998 B  |
| `light.complex16s`         | **ライト / Light**                | `06 36 b6 47 00` | 247,722 B |

固定 19-byte ヘッダ（全コマンド共通）/ Fixed 19-byte prefix (common to all):
`20 aa b8 24 ca eb da 25 da 70 20 cf 6e 76 b6 7c de 28 c7`

## ファイル形式 / File Format

`iq_captures_1s/` と同じ: **interleaved signed 8-bit IQ**, 2 Msps, 2 bytes/sample.

## 抽出日 / Extraction Date

2025-10-09

## SHA-256 完整性確認 / Integrity

```bash
shasum -a 256 -c checksums.sha256
```

## 実行 / Usage

```bash
cd ../scripts
python3 verify_signal_captures.py
```

スクリプトは本フォルダの 5 ファイルを順次読み込み、復調・整列を行い、
"期待 tail" との比較結果を出力します。最良セグメントスコアが 1.0 に近ければ
フレームモデルが成立していることを示します。

The script reads all 5 files, demodulates, aligns to 24-byte frames, extracts the tail,
and compares against the expected values. A "best segment score" near 1.0 indicates the
frame model holds.
