#!/usr/bin/env python3
"""Verify toy-car RF captures against the current 24-byte frame model.

The files in this directory are decoded as interleaved signed 8-bit IQ samples.
Despite the ``.complex16s`` suffix, int8 interpretation gives ~380 sample
bursts, matching the expected 192-bit frame at 2 samples/symbol.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np


PREFIX_HEX = "20aab824caebda25da7020cf6e76b67cde28c7"
ADDRESS_HEX = "b824caebda"
FIXED9_BITS = "001001011"
PAYLOAD_FIXED_HEX = "b4e0419edced6cf9bc518e"

CAPTURES = {
    "left back.complex16s": "24549a2700",
    "left forward.complex16s": "2252d85780",
    "light.complex16s": "0636b64700",
    "right back.complex16s": "26d64d8f00",
    "right forward.complex16s": "2757ff1700",
}


@dataclass
class SegmentDecode:
    score: float
    aligned_bits: np.ndarray


def bits_from_hex(hex_text: str) -> np.ndarray:
    return np.array(
        [(byte >> (7 - bit)) & 1 for byte in bytes.fromhex(hex_text) for bit in range(8)],
        dtype=np.uint8,
    )


def bits_from_int(value: int, width: int) -> list[int]:
    return [(value >> (width - 1 - bit)) & 1 for bit in range(width)]


def hex_from_bits(bits: np.ndarray) -> str:
    out = bytearray()
    for start in range(0, len(bits), 8):
        value = 0
        for bit in bits[start : start + 8]:
            value = (value << 1) | int(bit)
        out.append(value)
    return out.hex()


def crc16_1021_msb(bits: list[int], init: int = 0xFFFF, poly: int = 0x1021) -> int:
    crc = init
    for bit in bits:
        top = (crc >> 15) & 1
        crc = (crc << 1) & 0xFFFF
        if top ^ bit:
            crc ^= poly
    return crc


def read_complex_int8(path: Path) -> np.ndarray:
    raw = np.fromfile(path, dtype=np.int8)
    raw = raw[: raw.size // 2 * 2]
    iq = raw.reshape(-1, 2).astype(float)
    return iq[:, 0] + 1j * iq[:, 1]


def detect_segments(samples: np.ndarray) -> list[tuple[int, int]]:
    magnitude = np.abs(samples)
    active = np.flatnonzero(magnitude > 1)
    gaps = np.flatnonzero(np.diff(active) > 1)
    starts = np.r_[active[0], active[gaps + 1]]
    ends = np.r_[active[gaps], active[-1]]
    return [(int(start), int(end)) for start, end in zip(starts, ends) if end - start + 1 >= 350]


def fm_demod_bits(
    samples: np.ndarray,
    start: int,
    end: int,
    prepad: int,
    postpad: int,
    offset: int,
    invert: bool,
) -> np.ndarray:
    first = max(0, start - prepad)
    last = min(len(samples), end + 1 + postpad)
    burst = samples[first:last]
    dphi = np.angle(burst[1:] * np.conj(burst[:-1]))

    values: list[float] = []
    for pos in range(offset, len(dphi), 2):
        values.append(float(dphi[pos : pos + 2].mean()))

    bits = (np.array(values) > 0).astype(np.uint8)
    if invert:
        bits ^= 1
    return bits


def align_score(bits: np.ndarray, expected: np.ndarray) -> tuple[float, int]:
    best_score = -1.0
    best_offset = 0
    for offset in range(-10, 11):
        bit_start = max(0, -offset)
        bit_end = min(len(bits), len(expected) - offset)
        overlap = bit_end - bit_start
        if overlap < 170:
            continue
        exp_start = bit_start + offset
        score = float(np.count_nonzero(bits[bit_start:bit_end] == expected[exp_start : exp_start + overlap]) / overlap)
        if score > best_score:
            best_score = score
            best_offset = offset
    return best_score, best_offset


def project_bits(bits: np.ndarray, offset: int, width: int) -> np.ndarray:
    aligned = np.full(width, -1, dtype=np.int8)
    for idx, bit in enumerate(bits):
        target = idx + offset
        if 0 <= target < width:
            aligned[target] = int(bit)
    return aligned


def best_segment_decode(samples: np.ndarray, start: int, end: int, expected: np.ndarray) -> SegmentDecode:
    best: tuple[float, int, np.ndarray] | None = None
    for prepad in range(0, 9):
        for postpad in range(0, 13):
            for offset in (0, 1):
                for invert in (False, True):
                    bits = fm_demod_bits(samples, start, end, prepad, postpad, offset, invert)
                    score, bit_offset = align_score(bits, expected)
                    if best is None or score > best[0]:
                        best = (score, bit_offset, bits)
    assert best is not None
    score, bit_offset, bits = best
    return SegmentDecode(score=score, aligned_bits=project_bits(bits, bit_offset, len(expected)))


def majority_vote(decoded: list[SegmentDecode], width: int) -> tuple[np.ndarray, float, int, int]:
    matrix = np.array([item.aligned_bits for item in decoded])
    output: list[int] = []
    confidences: list[float] = []
    coverages: list[int] = []

    for column in range(width):
        values = matrix[:, column]
        values = values[values >= 0]
        coverages.append(len(values))
        ones = int(values.sum())
        zeros = len(values) - ones
        output.append(1 if ones > zeros else 0)
        confidences.append(max(ones, zeros) / len(values) if len(values) else 0.0)

    return (
        np.array(output, dtype=np.uint8),
        float(np.mean(confidences)),
        int(min(coverages)),
        int(max(coverages)),
    )


def parse_tail(tail_hex: str) -> tuple[int, int, int, int, int]:
    raw = int(tail_hex, 16)
    fixed_bit = (raw >> 39) & 1
    ck = (raw >> 23) & 0xFFFF
    crc_obs = (raw >> 7) & 0xFFFF
    padding = raw & 0x7F
    return fixed_bit, (ck >> 8) & 0xFF, ck & 0xFF, crc_obs, padding


def verify_crc(c_value: int, k_value: int, crc_obs: int) -> tuple[int, int]:
    ck = (c_value << 8) | k_value
    crc_bits = (
        list(bits_from_hex(ADDRESS_HEX))
        + [int(bit) for bit in FIXED9_BITS]
        + list(bits_from_hex(PAYLOAD_FIXED_HEX))
        + bits_from_int(ck, 16)
    )
    crc_calc = crc16_1021_msb(crc_bits)
    return crc_calc, crc_calc ^ crc_obs


def expected_k(c_value: int) -> int:
    return c_value ^ (0xE1 if c_value & 0x40 else 0x61)


def main() -> None:
    root = Path(__file__).resolve().parent.parent / "iq_bursts_extracted"
    print("capture,segments,mean_score,decoded_tail,C,K,crc_obs,crc_calc,xor,k_ok,padding,full_frame_mismatches")

    for filename, expected_tail in CAPTURES.items():
        expected = bits_from_hex(PREFIX_HEX + expected_tail)
        samples = read_complex_int8(root / filename)
        segments = detect_segments(samples)
        decoded = [best_segment_decode(samples, start, end, expected) for start, end in segments]
        majority_bits, _confidence, _coverage_min, _coverage_max = majority_vote(decoded, len(expected))
        majority_hex = hex_from_bits(majority_bits)
        decoded_tail = majority_hex[-10:]
        mismatches = int(np.count_nonzero(majority_bits != expected))

        _fixed, c_value, k_value, crc_obs, padding = parse_tail(decoded_tail)
        crc_calc, crc_xor = verify_crc(c_value, k_value, crc_obs)

        print(
            ",".join(
                [
                    filename,
                    str(len(segments)),
                    f"{np.mean([item.score for item in decoded]):.4f}",
                    decoded_tail,
                    f"{c_value:02x}",
                    f"{k_value:02x}",
                    f"{crc_obs:04x}",
                    f"{crc_calc:04x}",
                    f"{crc_xor:04x}",
                    str(k_value == expected_k(c_value)),
                    str(padding),
                    str(mismatches),
                ]
            )
        )


if __name__ == "__main__":
    main()
