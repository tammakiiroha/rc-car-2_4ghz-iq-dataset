# データ範囲声明 / Data Coverage Statement

本文書は、本データセットが論文のどの主張を**直接支持するか**、および
**生 IQ として保存されていない**観測に依拠する主張がどれかを明示します。
学術的な透明性のために提供します。

This document discloses **which paper claims this dataset directly supports** and
**which claims rely on observations not preserved as raw IQ in this release**.
Provided in the spirit of academic transparency.

論文 / Paper: 「ソフトウェア無線を用いた市販 2.4 GHz 車型玩具のリバースエンジニアリング」
("Reverse Engineering of a Commercial 2.4 GHz RC Toy Car Using Software Defined Radio")

---

## ✓ 本リポジトリが直接支持する主張 / Directly Supported

| 論文の主張 / Paper claim | 対応ファイル / Supporting file(s) |
|---|---|
| §3.2 / 表 1: HackRF + URH 取得条件 | `iq_captures_1s/*.complex16s` |
| §3.2 / 表 2: FSK 復調パラメータ | `urh_project/URHProject.xml` |
| §4.1: 24-byte フレームモデル `f = h \|\| t` | `iq_bursts_extracted/*.complex16s` + `scripts/verify_signal_captures.py` |
| §4.1 / 固定ヘッダ `h` (19 bytes) | `iq_bursts_extracted/` 内全ファイル |
| §4.1 / tail `light` (`06 36 b6 47 00`) | `light.complex16s`（両フォルダ）|
| §4.1 / tail `LF` (`22 52 d8 57 80`) | Left forward 録音 |
| §4.1 / tail `LB` (`24 54 9a 27 00`) | Left backward 録音 |
| §4.1 / tail `RF` (`27 57 ff 17 00`) | Right forward 録音 |
| §4.1 / tail `RB` (`26 d6 4d 8f 00`) | Right backward 録音 |
| §4.2: m_L = t_LF ⊕ t_LB = `06 06 42 70 80` | LF と LB 録音から再計算可能 |
| §4.2: m_R = t_RF ⊕ t_RB = `01 81 b2 98 00` | RF と RB 録音から再計算可能 |

---

## ✗ 本リポジトリには含まれない観測 / Not Directly Supported

以下の項目は論文中で**観測された**と記述されていますが、
**生の IQ / 試行ログ / 動画が本リリースに含まれていません**。
多くは私的作業フォルダに中間メモとしてのみ存在しており、
整備が完了次第別途公開する可能性があります。

The following are **stated in the paper as observed** but the raw IQ / log / video
evidence is **not included** in this release. Most exist only as intermediate
notes in private working folders.

| 論文の主張 / Paper claim | 不足している証拠 / Missing | 状況 / Status |
|---|---|---|
| §4.1 / `demo` tail (`36 46 cd 45 00`) | demo 録音なし | ローカルに録音済みだが本リリース未整備 |
| §4.1 / 両輪前進 (`23 53 fb 47 80`) | Both Fwd 録音なし | 同上 |
| §4.1 / 両輪後退 (`24 d4 0b af 00`) | Both Back 録音なし | 同上 |
| §4.1 / `LB+RF` (`25 55 b9 37 00`) | 旋回録音なし | 同上 |
| §4.1 / `RB+LF` (`22 d2 49 df 80`) | 旋回録音なし | 同上 |
| §4.2: m_B = `07 87 f0 e8 80` | 入力（BF, BB の IQ）が未収録 | BF/BB 公開後に再計算可能 |
| §3.3 / §4.3: 合成 tail `03 33 91 07 80`, `02 32 b2 17 80`, `07 37 95 57 00`（ライト+走行 forgery）| TX 側 IQ モニタ・試行ログ・動画なし | TX 波形は URH ランタイム生成、未保存 |
| §4.4: 非受理 tail `t_inv = 26 56 dc 07 00` | TX 側キャプチャ・試行ログ・動画なし | 同上 |
| §4.3 / v_light = `20 60 6a 40 00` | t_light + t_inv に依拠（t_inv 未収録）| 数値関係のみ、生証拠は未収録 |
| §5.1: Replay 攻撃 45/50, Wilson CI [0.79, 0.96] | 試行ごとのログ・動画・TX 側 IQ なし | 集計値のみ、生試行証拠は未整備 |
| §5.2: Forgery 攻撃 20/20 | 試行ごとのログ・動画・TX 側 IQ なし | 同上 |
| §3.2: 2.475 GHz を選定したスペクトラムスイープ | スペクトラムスキャン IQ なし | URH 上でライブ実施、未保存 |

---

## まとめ / Summary

本リリースは §4.1（フレーム構造の同定）および §4.2 部分（`m_L`, `m_R` の導出）を
**完全にカバー**しています。以下は**独立に再現できません**:

- 表 3 の全 tail 集合（10 行中 5 行が生 IQ 未収録）
- 両輪反転マスク `m_B`（BF / BB が未収録のため）
- forgery / replay 統計（§5）
- 非受理 tail の観測（§4.4）

This release **fully covers** §4.1 and §4.2 partial. It **does not** independently
reproduce: full tail table (5 of 10 rows missing), `m_B` (depends on missing BF/BB),
forgery/replay statistics (§5), and the non-accepted tail observation (§4.4).

支持される項目の検証は `scripts/verify_signal_captures.py` を直接実行することで可能です。
未収録項目の再現には別途キャプチャと試行ログが必要です。

Re-using this release to verify the supported items above is straightforward via
`scripts/verify_signal_captures.py`. Reproducing the unsupported items requires
additional captures and trial logs not curated here.
