# 詳細索引 / Detailed Index

論文 / Paper: 「ソフトウェア無線を用いた市販 2.4 GHz 車型玩具のリバースエンジニアリング」
最終更新 / Last updated: 2026-05-10

> 本索引は、提出論文で実際に使用した**生 IQ ファイル**、**URH 設定**、および
> **検証スクリプト**を網羅的に列挙します。各ファイルは対応する論文章節、操作種別、
> 録音パラメータとともに注記しています。論文に無関係な内容は含まれません。
>
> This index lists every **raw IQ file**, **URH setting**, and **verification script**
> used in the submitted manuscript. Each file is annotated with its corresponding
> paper section, operation class, and recording parameters.

---

## 1. iq_captures_1s/ — 主録音 / Primary Raw IQ Recordings

**内容 / What**: HackRF One により 2.475 GHz で正規リモコンを ~1 秒押下しながら
受信した生 IQ データ（論文 表 1: `取得長 ≈ 1 s/操作`）。

**論文位置 / Paper reference**: §3.2（測定環境と信号処理）+ 表 1 + 表 2

| # | ファイル / Filename | 操作 / Operation | tail (5 bytes) | サイズ / Size | 録音長 / Duration | 録音日 / Recorded |
|---|---|---|---|---:|---:|---|
| 1 | `HackRF-Left forward-2_475GHz-2MSps-2MHz.complex16s`  | **左輪前進 / LF**  | `22 52 d8 57 80` | 16,777,216 B | 4.194 s | 2025-07-16 10:59:12 |
| 2 | `HackRF-Left backward-2_475GHz-2MSps-2MHz.complex16s` | **左輪後退 / LB** | `24 54 9a 27 00` | 17,301,504 B | 4.325 s | 2025-07-16 10:59:53 |
| 3 | `HackRF-Right forward-2_475GHz-2MSps-2MHz.complex16s` | **右輪前進 / RF** | `27 57 ff 17 00` | 15,728,640 B | 3.932 s | 2025-07-16 11:00:45 |
| 4 | `HackRF-Right backward-2_475GHz-2MSps-2MHz.complex16s`| **右輪後退 / RB** | `26 d6 4d 8f 00` | 17,039,360 B | 4.260 s | 2025-07-16 11:01:41 |
| 5 | `HackRF-Light-2_475GHz-2MSps-2MHz.complex16s`         | **ライト / light** | `06 36 b6 47 00` | 13,893,632 B | 3.473 s | 2025-07-16 10:58:21 |
| 6 | `New1 HackRF-Left backward-...complex16s` | LB 切片 (~1 frame) | LB と同じ | 782 B | 0.0002 s | 2025-07-16 11:39:21 |
| 7 | `New2 HackRF-Left backward-...complex16s` | LB 切片 (~1 frame) | LB と同じ | 786 B | 0.0002 s | 2025-07-16 11:39:16 |

録音パラメータ（5 主ファイル統一）/ Recording parameters (uniform):
- fc = 2.475 GHz, fs = 2 Msps, BW = 2 MHz, RX Gain = 20 dB
- 形式 / Format: interleaved signed 8-bit IQ (1 byte/I + 1 byte/Q = 2 bytes/sample)

SHA-256: `iq_captures_1s/checksums.sha256`

---

## 2. iq_bursts_extracted/ — フレーム検証用 単一バースト / Single-Frame Bursts

**内容 / What**: 上記主録音から切り出した代表バースト。各ファイルは 1 つ
（または数個）の完全な 24-byte フレームを含み、`19-byte ヘッダ || 5-byte tail`
モデルの検証に使用。

**論文位置 / Paper reference**: §4.1（フレーム構造の同定）

| # | ファイル | 操作 / Operation | 期待 `PREFIX_HEX || tail` | サイズ | 抽出日 |
|---|---|---|---|---:|---|
| 1 | `left forward.complex16s`  | **LF**  | `…cde28c7 \| 22 52 d8 57 80` | 41,598 B  | 2025-10-09 14:08:23 |
| 2 | `left back.complex16s`     | **LB**  | `…cde28c7 \| 24 54 9a 27 00` | 231,132 B | 2025-10-09 14:09:30 |
| 3 | `right forward.complex16s` | **RF**  | `…cde28c7 \| 27 57 ff 17 00` | 243,974 B | 2025-10-09 14:03:28 |
| 4 | `right back.complex16s`    | **RB**  | `…cde28c7 \| 26 d6 4d 8f 00` | 21,998 B  | 2025-10-09 14:04:52 |
| 5 | `light.complex16s`         | **light**| `…cde28c7 \| 06 36 b6 47 00` | 247,722 B | 2025-10-09 13:58:31 |

固定 19-byte ヘッダ / Fixed 19-byte prefix:
`20 aa b8 24 ca eb da 25 da 70 20 cf 6e 76 b6 7c de 28 c7`

SHA-256: `iq_bursts_extracted/checksums.sha256`

---

## 3. urh_project/URHProject.xml — URH 復調設定 / URH Demodulation Settings

**内容 / What**: URH v2.10.0 プロジェクトファイル（FSK 復調パラメータを保存）。
**論文位置 / Paper reference**: 表 2 + 図 3（URH 解析画面例）

| 項目 / Item | 値 / Value | 表 2 対応行 |
|---|---:|---|
| 変調方式 / Modulation | FSK | 「変調方式」 |
| Bits/Symbol | 1 | 「変調方式 (Bits/Symbol=1)」 |
| Samples/Symbol | 2 | 「Samples/Symbol」 |
| Sample rate (URH 内) | 1,000,000 Hz | （内部解析用、録音は 2 Msps） |
| Pause threshold | 8 | — |
| Noise threshold | 1.4143 | — |
| Costas loop bandwidth | 0.1 | — |
| 復号方式 / Decodings | NRZ / NRZ+Inv / Manchester I/II / Differential Manchester | — |

> 注: `<device_conf>` 内 `name=USRP`、`frequency=433920000` は URH のデフォルト値。
> 実際の録音は HackRF + 2.475 GHz で `hackrf_transfer` 等を介して独立に行われた。

---

## 4. scripts/verify_signal_captures.py — 検証スクリプト / Verification Script

**内容 / What**: `iq_bursts_extracted/` の各バーストを復調・整列・24-byte フレーム
切り出し・5-byte tail 抽出を行い、期待値と比較。

**論文位置 / Paper reference**: §4.1（フレーム構造の同定）

ハードコード参照値 / Hardcoded reference values:

```python
PREFIX_HEX        = "20aab824caebda25da7020cf6e76b67cde28c7"   # 19-byte 固定ヘッダ
ADDRESS_HEX       = "b824caebda"                               # ヘッダ内 5-byte アドレス
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

実行 / Run:

```bash
cd experiment_data        # repository root
python3 scripts/verify_signal_captures.py
```

---

## 5. 録音条件総覧 / Recording Conditions（論文 表 1）

| 項目 / Item | 値 / Value |
|---|---|
| OS | Linux Ubuntu 17.10 (kernel 4.13.0-generic) |
| URH | v2.10.0 |
| `hackrf_info` | 2023.01.1 |
| libhackrf | 2023.01.1 (0.8) |
| HackRF Firmware | 2024.02.1 (API 1.08) |
| SDR HW | HackRF One (HW rev r10) |
| RX / TX Gain | 20 dB / 20 dB |
| TX–RX 距離 / distance | 約 30 cm |
| アンテナ高さ / Antenna height | 約 40 cm |
| アンテナ / Antenna | 付属 2.4 GHz whip（型番記載なし）|
| 取得環境 / Capture environment | 屋外（低雑音）/ Outdoor (low noise) |
| 送信攻撃環境 / Replay environment | 室内実験室（雑音・干渉あり）/ Indoor lab |
| 取得長 / Capture duration | 約 1 s/操作 |
| フレーム数 / Frames | 約 50 frame/操作 |

## 6. 測定・復調パラメータ / Measurement Parameters（論文 表 2）

| 項目 / Item | 値 / Value |
|---|---|
| 中心周波数 fc | 2.475 GHz |
| 変調方式 / Modulation | FSK (Bits/Symbol=1) |
| サンプリングレート fs | 2 Msps |
| Samples/Symbol | 2 |
| 受信帯域幅 BW | 2 MHz |
| 周波数偏移 / URH freq deviation | 101.562 kHz / 203.125 kHz |
| 推定シンボルレート / Symbol rate | 約 1 Msym/s (fs/SPS) |
| フレーム整列基準 / Frame alignment | プリアンブル検出点 / preamble-detection point |

---

## 7. フレームモデル / Frame Model（論文 §4.1）

```
1 フレーム / frame = 24 bytes (192 bits) = h || t

  h (19 bytes 固定ヘッダ / fixed header, 全コマンド共通 / common to all commands):
     20 aa b8 24 ca eb da 25 da 70 20 cf 6e 76 b6 7c de 28 c7

  t (5 bytes 可変 tail / variable tail):
     light                  06 36 b6 47 00
     demo                   36 46 cd 45 00
     左輪前進 / LF           22 52 d8 57 80
     左輪後退 / LB           24 54 9a 27 00
     右輪前進 / RF           27 57 ff 17 00
     右輪後退 / RB           26 d6 4d 8f 00
     両輪前進 / Both Fwd     23 53 fb 47 80
     両輪後退 / Both Back    24 d4 0b af 00
     LB+RF（逆時計回り / CCW）25 55 b9 37 00
     RB+LF（時計回り / CW）   22 d2 49 df 80
```

抽出された差分マスク / Differential masks（論文 §4.2）:
- m_L (左輪反転 / left wheel reversal) = `06 06 42 70 80`
- m_R (右輪反転 / right wheel reversal) = `01 81 b2 98 00`
- m_B (両輪反転 / both wheel reversal) = `07 87 f0 e8 80` = m_L ⊕ m_R
- v_light (ライトベクトル / light vector) = `20 60 6a 40 00`

---

## 8. データ来歴 / Provenance

本リポジトリのファイルは 2026-05-09 に著者ローカル作業ディレクトリから集約されました。
原 IQ データは 2025-07-16 取得、検証バーストは 2025-10-09 抽出。

All files in this repository were collated from the author's local working directories
on 2026-05-09. Raw IQ data were captured on 2025-07-16; verification bursts were
extracted on 2025-10-09.

---

## 9. IQ ファイル読み込み参考コード / IQ File Reading Reference

```python
import numpy as np

# interleaved signed 8-bit IQ
raw = np.fromfile("iq_captures_1s/HackRF-Left forward-2_475GHz-2MSps-2MHz.complex16s",
                  dtype=np.int8)
iq = raw.reshape(-1, 2).astype(np.float32)
samples = iq[:, 0] + 1j * iq[:, 1]
# fs = 2 Msps, fc = 2.475 GHz
```
