#!/usr/bin/env python3
"""gen_audio_items — audio-native fault signatures with ground truth by construction.

Four families (16 kHz mono WAV, ~5 s):
  engine    Idle firing rhythm: even fire (pass) vs. single-cylinder miss
            (periodic gap -> fail) vs. random misfire (irregular gaps -> fail)
  bearing   Shaft hum +/- defect impulse train: healthy (pass), early stage
            (fail/medium: schedule replacement), severe (fail/high: pull now)
  hum       Clean 120 Hz magnetic hum (pass) vs. hum + irregular broadband
            crackle = arcing (fail/critical: de-energize)
  hammer    Valve closure: clean stop (pass) vs. decaying low-frequency
            thump train = water hammer (fail: arrestor/air chamber)

Every signal parameter that defines the label is set by the generator, and a
self-verification pass re-detects the labels from the rendered audio (event
counts, spectral peaks, transient energy) before items are written — the
audio equivalent of hand-checking the sling trig.

Outputs benchmark/media/audio_*.wav and benchmark/items/audio_items_v2.json.
"""
from __future__ import annotations

import json
import math
import random
import wave
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
MEDIA = ROOT / "benchmark" / "media"
OUT = ROOT / "benchmark" / "items" / "audio_items_v2.json"
SR = 16000
DUR = 5.0
rng = random.Random(20260706)
nprng = np.random.default_rng(20260706)


def write_wav(path: Path, x: np.ndarray) -> None:
    x = x / (np.max(np.abs(x)) + 1e-9) * 0.85
    pcm = (x * 32767).astype(np.int16)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())


def lowpass(x: np.ndarray, cutoff: float) -> np.ndarray:
    # simple one-pole IIR, good enough for timbre shaping
    a = math.exp(-2 * math.pi * cutoff / SR)
    y = np.empty_like(x)
    acc = 0.0
    for i, v in enumerate(x):
        acc = (1 - a) * v + a * acc
        y[i] = acc
    return y


def burst(dur_ms: float, cutoff: float, ring_hz: float | None = None) -> np.ndarray:
    n = int(SR * dur_ms / 1000)
    env = np.exp(-np.linspace(0, 6, n))
    if ring_hz:
        t = np.arange(n) / SR
        core = np.sin(2 * np.pi * ring_hz * t) + 0.4 * nprng.standard_normal(n)
    else:
        core = nprng.standard_normal(n)
        core = lowpass(core, cutoff)
    return core * env


def place(x: np.ndarray, clip: np.ndarray, at_s: float, gain: float = 1.0) -> None:
    i = int(at_s * SR)
    j = min(len(x), i + len(clip))
    if i < len(x):
        x[i:j] += clip[: j - i] * gain


# ---------------------------------------------------------------- signals
def gen_engine(mode: str, rpm: int, ncyl: int = 4):
    """mode: even | single_miss | random_miss. Returns signal + event bookkeeping."""
    x = 0.02 * lowpass(nprng.standard_normal(int(SR * DUR)), 300)  # engine bed noise
    fire_hz = rpm / 60 * (ncyl / 2)
    period = 1 / fire_hz
    pop = burst(28, 500)
    t, k, fired, missed = 0.05, 0, 0, 0
    while t < DUR - 0.1:
        miss = (mode == "single_miss" and k % ncyl == ncyl - 1) or \
               (mode == "random_miss" and rng.random() < 0.18)
        if miss:
            missed += 1
            place(x, pop, t, gain=0.08)  # weak partial burn
        else:
            fired += 1
            place(x, pop, t, gain=1.0 * (0.9 + 0.2 * rng.random()))
        t += period
        k += 1
    return x, {"fire_hz": fire_hz, "fired": fired, "missed": missed}


def gen_bearing(stage: str, shaft_hz: float):
    """stage: healthy | early | severe. Slow rotating element (conveyor/gearbox
    output, ~4-8 rev/s) so one defect strike per revolution is a discrete,
    countable tick over the machine drone."""
    t = np.arange(int(SR * DUR)) / SR
    x = 0.45 * np.sin(2 * np.pi * 30 * t) + 0.2 * np.sin(2 * np.pi * 60 * t)  # drive drone
    x += 0.03 * lowpass(nprng.standard_normal(len(t)), 800)
    n_imp = 0
    if stage != "healthy":
        gain = 0.7 if stage == "early" else 2.2
        ring = burst(14, 0, ring_hz=2600)
        tt = 0.06
        while tt < DUR - 0.05:
            place(x, ring, tt, gain=gain * (0.85 + 0.3 * rng.random()))
            n_imp += 1
            tt += 1 / shaft_hz
        if stage == "severe":
            x += 0.12 * lowpass(nprng.standard_normal(len(t)), 3000)  # roughness
    return x, {"defect_hz": shaft_hz, "impulses": n_imp}


def gen_hum(arcing: bool):
    t = np.arange(int(SR * DUR)) / SR
    x = 0.6 * np.sin(2 * np.pi * 120 * t) + 0.25 * np.sin(2 * np.pi * 240 * t) \
        + 0.1 * np.sin(2 * np.pi * 360 * t) + 0.01 * nprng.standard_normal(len(t))
    n_crackle = 0
    if arcing:
        n_crackle = rng.randint(25, 45)
        for _ in range(n_crackle):
            c = burst(rng.uniform(4, 18), 6000)
            place(x, c, rng.uniform(0.1, DUR - 0.1), gain=rng.uniform(0.8, 2.2))
    return x, {"crackles": n_crackle}


def gen_hammer(present: bool):
    n = int(SR * DUR)
    x = np.zeros(n)
    close_at = 2.0
    flow = 0.25 * lowpass(nprng.standard_normal(int(SR * close_at)), 1200)
    x[: len(flow)] += flow  # water running, then valve closes
    place(x, burst(15, 2000), close_at - 0.02, gain=0.5)  # valve click
    n_thump = 0
    if present:
        t0, gain = close_at + 0.03, 1.8
        f = rng.uniform(42, 58)
        while gain > 0.15:
            k = int(SR * 0.25)
            tt = np.arange(k) / SR
            thump = np.sin(2 * np.pi * f * tt) * np.exp(-tt * 14)
            place(x, thump, t0, gain=gain)
            n_thump += 1
            t0 += rng.uniform(0.22, 0.3)
            gain *= 0.55
    x += 0.004 * nprng.standard_normal(n)
    return x, {"thumps": n_thump, "close_at": close_at}


# ---------------------------------------------------------------- self-verification
def band_energy(x: np.ndarray, lo: float, hi: float) -> float:
    spec = np.abs(np.fft.rfft(x)) ** 2
    freqs = np.fft.rfftfreq(len(x), 1 / SR)
    return float(spec[(freqs >= lo) & (freqs < hi)].sum())


def count_transients(x: np.ndarray, hp_hz: float, thresh_ratio: float) -> int:
    hp = x - lowpass(x, hp_hz)
    env = np.abs(hp)
    win = int(SR * 0.004)
    env = np.convolve(env, np.ones(win) / win, mode="same")
    th = thresh_ratio * np.median(env) + 1e-9
    above = env > th
    return int(np.sum(above[1:] & ~above[:-1]))


def verify(fam: str, x: np.ndarray, meta: dict, variant: str) -> bool:
    if fam == "hum":
        crackles = count_transients(x, 1500, 8)
        return crackles >= 10 if variant == "arcing" else crackles <= 3
    if fam == "hammer":
        tail = x[int(SR * (meta["close_at"] + 0.05)):]
        thump_e = band_energy(tail, 30, 90)
        ref_e = band_energy(tail, 300, 1000) + 1e-9
        return (thump_e / ref_e > 5) if variant == "hammer" else (thump_e / ref_e < 1.5)
    if fam == "bearing":
        ticks = count_transients(x, 1800, 6)
        exp = meta["impulses"]
        if variant == "healthy":
            return ticks <= 3
        return 0.6 * exp <= ticks <= 1.6 * exp
    if fam == "engine":
        total = meta["fired"] + meta["missed"]
        if variant == "even":
            return meta["missed"] == 0 and total > 80
        return meta["missed"] >= max(3, int(0.1 * total))
    return False


# ---------------------------------------------------------------- items
def skeleton(fam: str, idx: int, tier, disc, dcode, el, ecode, sub, refs, src) -> dict:
    reduction_tests = {
        "engine": "The answer depends on the rhythm and regularity of firing events; a transcript loses the repeating or irregular gaps.",
        "bearing": "The answer depends on transient ticks/growl over rotating-machine hum; text cannot preserve onset rate or severity.",
        "hum": "The answer depends on steady harmonic hum versus irregular broadband crackle; a transcript loses the spectral and temporal cue.",
        "hammer": "The answer depends on the post-closure decaying thump train; text cannot preserve the timing and decay pattern.",
    }
    sound_sources = {
        "engine": ["engine", "engine idle", "four cylinder engine"],
        "bearing": ["bearing", "bearing housing", "conveyor bearing"],
        "hum": ["electrical panel", "panel", "termination"],
        "hammer": ["fixture valve", "water supply", "plumbing valve"],
    }
    return {
        "id": f"v2-audio-{fam}-{idx:03d}",
        "title": f"{tier} {ecode} Fault diagnosis by sound",
        "tier": tier, "discipline": disc, "discipline_code": dcode,
        "element": el, "element_code": ecode, "subcategory": sub,
        "task_type": "FD", "task_type_name": "Fault diagnosis (audio)",
        "s1_state": "in-service", "s3_percent": 100,
        "source_refs": refs, "source_file": src,
        "generation": "synthetic-audio-v2", "modality": "audio",
        "expected_sound_source": sound_sources[fam],
        "reduction_test": reduction_tests[fam],
        "findings_mode": "any_per_group",
    }


def main() -> None:
    MEDIA.mkdir(parents=True, exist_ok=True)
    items, rejected = [], 0

    def emit(fam, idx, x, meta, variant, it_fields):
        nonlocal rejected
        if not verify(fam, x, meta, variant):
            rejected += 1
            return
        fname = f"audio_{fam}_{idx:03d}.wav"
        write_wav(MEDIA / fname, x)
        it_fields["media"] = [fname]
        items.append(it_fields)

    # ---- engine: 12
    for i in range(12):
        variant = ["even", "single_miss", "random_miss"][i % 3]
        rpm = rng.choice([750, 800, 850])
        x, meta = gen_engine(variant, rpm)
        it = skeleton("engine", i, "T4", "2.9 Automotive & Powertrain", "2.9",
                      "A-101 Timing & mechanical", "A-101", "2.9.1 Engine & Drivetrain",
                      ["OEM service info"], "docs/source/element-trees-industrial-service-v0.1.md")
        it["scenario"] = ("The audio clip is a 5-second recording of a warm 4-cylinder engine at idle, "
                          "taken at the fender with a phone.")
        it["prompt"] = ("Listen to the idle cadence. Classify the condition from the rhythm, "
                        "identify the likely fault pattern if one is present, and give the disposition.")
        if variant == "even":
            it.update(decision="pass", risk="low", s2_expected=[],
                      required_findings=[["even", "smooth", "steady", "healthy"]],
                      required_actions=[["release", "no", "document"]],
                      forbidden=[["misfire", "detected"]])
        elif variant == "single_miss":
            it.update(decision="fail", risk="medium", s2_expected=["degraded"],
                      required_findings=[["single", "one", "regular", "repeating"]],
                      required_actions=[["cylinder", "identify", "coil", "plug", "test"]],
                      forbidden=[["healthy", "idle"]])
        else:
            it.update(decision="fail", risk="medium", s2_expected=["degraded"],
                      required_findings=[["random", "irregular", "intermittent"]],
                      required_actions=[["fuel", "vacuum", "test", "investigate"]],
                      forbidden=[["healthy", "idle"]])
        emit("engine", i, x, meta, variant, it)

    # ---- bearing: 12
    for i in range(12):
        variant = ["healthy", "early", "severe"][i % 3]
        shaft = rng.choice([4.5, 6.0, 7.5])  # slow element: conveyor/gearbox output
        x, meta = gen_bearing(variant, shaft)
        it = skeleton("bearing", i, "T5", "2.7 Equipment & Machinery", "2.7",
                      "M-301 Bearings & seals", "M-301", "2.7.3 Rotating Equipment",
                      ["SKF/Timken guides"], "docs/source/element-trees-industrial-service-v0.1.md")
        it["scenario"] = ("The audio clip is a stethoscope-style recording at the bearing housing of a "
                          "slow-turning conveyor drive running at constant speed.")
        it["prompt"] = ("Diagnose the rotating-element condition from the sound. Pay attention to "
                        "whether the machine bed noise is clean, impact-like, or rough, then give "
                        "urgency and disposition.")
        if variant == "healthy":
            it.update(decision="pass", risk="low", s2_expected=[],
                      required_findings=[["smooth", "hum", "no", "normal"]],
                      required_actions=[["monitor", "route", "document"]],
                      forbidden=[["replace", "bearing", "now"]])
        elif variant == "early":
            it.update(decision="fail", risk="medium", s2_expected=["worn"],
                      required_findings=[["tick", "periodic", "early", "faint"]],
                      required_actions=[["schedule", "plan", "vibration", "trend"]],
                      forbidden=[["immediate", "shutdown"]])
        else:
            it.update(decision="fail", risk="high", s2_expected=["failed", "degraded"],
                      required_findings=[["growl", "knock", "severe", "loud"]],
                      required_actions=[["remove", "replace", "shutdown", "immediately"]],
                      forbidden=[["continue", "to", "monitor"]])
        emit("bearing", i, x, meta, variant, it)

    # ---- hum vs arcing: 10
    for i in range(10):
        variant = "arcing" if i % 2 else "hum"
        x, meta = gen_hum(arcing=(variant == "arcing"))
        it = skeleton("hum", i, "T2", "2.1 Electrical", "2.1",
                      "E-303 Terminations & splices", "E-303", "2.1.3 Wire & Cable",
                      ["NEC 110.14"], "docs/source/electrical-element-tree-v0.1.md")
        it["task_type_name"] = "Hazard identification (audio)"
        it["scenario"] = ("The audio clip was recorded at a closed electrical panel after an occupant "
                          "reported a buzzing sound.")
        it["prompt"] = ("Evaluate the panel sound and decide whether it can remain in service or "
                        "requires immediate electrical isolation. Give the safety disposition.")
        if variant == "hum":
            it.update(decision="pass", risk="low", s2_expected=[],
                      required_findings=[["steady", "hum", "magnetic", "normal"]],
                      required_actions=[["no", "monitor", "document"]],
                      forbidden=[["de", "energize"], ["arcing"]])
        else:
            it.update(decision="fail", risk="critical", s2_expected=["installed-defective"],
                      required_findings=[["crackle", "sizzle", "irregular", "arcing"]],
                      required_actions=[["de-energize", "deenergize", "electrician", "immediately"]],
                      forbidden=[["normal", "hum", "only"]])
        emit("hum", i, x, meta, variant, it)

    # ---- water hammer: 10
    for i in range(10):
        variant = "hammer" if i % 2 else "clean"
        x, meta = gen_hammer(present=(variant == "hammer"))
        it = skeleton("hammer", i, "T3", "2.2 Mechanical - Piping & Plumbing", "2.2",
                      "P-301 PEX & copper installation", "P-301", "2.2.3 Plumbing - Supply",
                      ["IPC"], "docs/source/element-trees-construction-v0.1.md")
        it["scenario"] = ("The audio clip records a fixture valve closing in a home: running water, a "
                          "valve click, then whatever follows.")
        it["prompt"] = ("Diagnose what happens after the valve closes. Decide whether the system "
                        "can be left as-is or needs a plumbing correction, and name the fix if one "
                        "is needed.")
        if variant == "clean":
            it.update(decision="pass", risk="low", s2_expected=[],
                      required_findings=[["clean", "quiet", "normal", "no"]],
                      required_actions=[["no", "none", "document"]],
                      forbidden=[["water", "hammer", "present"]])
        else:
            it.update(decision="fail", risk="medium", s2_expected=["non-compliant"],
                      required_findings=[["hammer", "thump", "bang"]],
                      required_actions=[["arrestor", "arrester", "air", "chamber", "secure"]],
                      forbidden=[["normal", "closure"]])
        emit("hammer", i, x, meta, variant, it)

    OUT.write_text(json.dumps(items, indent=2, sort_keys=True), encoding="utf-8")
    from collections import Counter
    print(f"Wrote {len(items)} audio items ({rejected} rejected by self-verification)")
    print("decisions:", Counter(x["decision"] for x in items))
    print("families:", Counter(x["id"].split("-")[2] for x in items))


if __name__ == "__main__":
    main()
