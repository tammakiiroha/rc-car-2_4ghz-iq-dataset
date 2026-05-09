# scripts/ — 検証スクリプト / Verification Script

## このフォルダの内容 / What this folder contains

`verify_signal_captures.py` —
**24-byte フレームモデルの参照実装 / 自動検証スクリプト**

`../iq_bursts_extracted/` の 5 つの単一フレームバーストに対して以下を実行:
- 8-bit IQ 読み込み
- FM/FSK 復調
- ビット列整列
- 24-byte フレーム切り出し
- 5-byte tail 抽出と "期待 tail" との比較

論文 §4.1 のフレームモデル
**`24-byte = 19-byte 固定ヘッダ || 5-byte 操作依存 tail`**
を実証します。

Reference implementation / automatic verifier for the 24-byte frame model defined in
論文 §4.1.

## スクリプト内ハードコード参照値 / Hardcoded Reference Values

```python
PREFIX_HEX        = "20aab824caebda25da7020cf6e76b67cde28c7"  # 19-byte 固定ヘッダ / fixed header
ADDRESS_HEX       = "b824caebda"                              # ヘッダ内 5-byte アドレス
FIXED9_BITS       = "001001011"
PAYLOAD_FIXED_HEX = "b4e0419edced6cf9bc518e"

CAPTURES = {                  # 5 バースト → 期待 tail
    "left back.complex16s":     "24549a2700",   # LB
    "left forward.complex16s":  "2252d85780",   # LF
    "light.complex16s":         "0636b64700",   # light
    "right back.complex16s":    "26d64d8f00",   # RB
    "right forward.complex16s": "2757ff1700",   # RF
}
```

## 実行方法 / How to Run

```bash
cd experiment_data        # repository root
python3 scripts/verify_signal_captures.py
```

スクリプトは `../iq_bursts_extracted/*.complex16s` を相対パスで自動解決します。
依存 / Dependencies: `numpy`
