# urh_project/ — URH プロジェクトファイル / URH Project File

## このフォルダの内容 / What this folder contains

`URHProject.xml` は **Universal Radio Hacker (URH) v2.10.0** で主録音
（`../iq_captures_1s/HackRF-Left backward-2_475GHz-2MSps-2MHz.complex16s` 等）を
開いて FSK 復調パラメータを設定した状態を保存したプロジェクトファイルです。

論文 表 2（測定・復調パラメータ）の
"フレーム整列基準 = プリアンブル検出点を基準に切り出し（URH 上で固定）"
が指す URH パラメータが本 XML に格納されています。

URH v2.10.0 project file capturing the FSK demodulation parameters used after loading
the primary IQ recording. Corresponds to 論文 表 2.

## 主要パラメータ / Key Parameters (signal element)

| 項目 / Item | 値 / Value |
|---|---:|
| 変調方式 / Modulation | FSK |
| Bits per symbol | 1 |
| Samples per symbol | 2 |
| Sample rate (URH 内 / internal) | 1,000,000 Hz |
| Pause threshold | 8 |
| Noise threshold | 1.4143 |
| Costas loop bandwidth | 0.1 |

## サポート復号 / Supported Decodings

`Non Return To Zero (NRZ)` / `NRZ + Invert` / `Manchester I` / `Manchester II` / `Differential Manchester`

## 注意事項 / Notes

- `<device_conf>` 内 `frequency=433920000`、`name=USRP` は URH のデフォルト値で、
  実際の取得には使用されていません。録音は **HackRF One @ 2.475 GHz** で `hackrf_transfer`
  等を介して独立に行われました（`../iq_captures_1s/README.md` 参照）。
- 本 XML は IQ ファイル読み込み**後**に URH 上で適用された解析設定を主に保存しています。

The `<device_conf>` block stores `name=USRP` and `frequency=433920000` (URH defaults),
**not** the parameters used for capture. Actual recordings used HackRF + 2.475 GHz via
standalone tools (e.g. `hackrf_transfer`).

## 再現方法 / How to Reproduce

1. URH v2.10.0 をインストール / Install URH v2.10.0
2. URH を起動 → `Project → Open` → `URHProject.xml` を選択
3. URH は IQ ファイルを相対パス `Data/HackRF-...complex16s` で参照するため:
   - `../iq_captures_1s/` 内の IQ ファイルを本 XML 横の `Data/` サブディレクトリへコピー、または
   - 各 `<signal filename="...">` および `<open_file name="...">` を絶対パスに編集
