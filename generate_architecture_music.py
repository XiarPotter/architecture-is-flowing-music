import math
import os
import wave
import struct
from array import array

SR = 22050
OUT_DIR = "/Users/lunxia/WorkBuddy/vibecoding/output"
os.makedirs(OUT_DIR, exist_ok=True)

NOTE_INDEX = {
    "C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3, "E": 4, "F": 5,
    "F#": 6, "Gb": 6, "G": 7, "G#": 8, "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11,
}


def freq(note):
    name = note[:-1]
    octave = int(note[-1])
    midi = 12 * (octave + 1) + NOTE_INDEX[name]
    return 440.0 * (2 ** ((midi - 69) / 12))


def envelope(kind, p):
    if p <= 0:
        return 0.0
    if p >= 1:
        return 0.0
    if kind == "pluck":
        if p < 0.03:
            return p / 0.03
        return math.exp(-4.6 * (p - 0.03))
    if kind == "bell":
        if p < 0.01:
            return p / 0.01
        return math.exp(-6.8 * (p - 0.01))
    if kind == "pad":
        if p < 0.18:
            return p / 0.18
        if p < 0.82:
            return 0.95
        return max(0.0, 0.95 * (1 - (p - 0.82) / 0.18))
    if kind == "bass":
        if p < 0.02:
            return p / 0.02
        if p < 0.7:
            return 0.8
        return max(0.0, 0.8 * (1 - (p - 0.7) / 0.3))
    return 1.0


PARTIALS = {
    "pluck": [(1.0, 0.95), (2.0, 0.18), (3.0, 0.08)],
    "bell": [(1.0, 0.75), (2.7, 0.35), (4.1, 0.22), (5.4, 0.12)],
    "pad": [(1.0, 0.6), (2.0, 0.18), (0.5, 0.12)],
    "bass": [(1.0, 0.9), (2.0, 0.25), (3.0, 0.12)],
}


def add_note(buf, start, dur, note, amp=0.4, kind="pluck"):
    if isinstance(note, str):
        f = freq(note)
    else:
        f = float(note)
    start_i = int(start * SR)
    n = int(dur * SR)
    partials = PARTIALS[kind]
    for i in range(n):
        idx = start_i + i
        if idx >= len(buf):
            break
        t = i / SR
        p = i / max(1, n - 1)
        env = envelope(kind, p)
        s = 0.0
        vibrato = 1.0 + 0.002 * math.sin(2 * math.pi * 4.2 * t) if kind == "pad" else 1.0
        for mult, weight in partials:
            s += weight * math.sin(2 * math.pi * f * mult * vibrato * t)
        buf[idx] += amp * env * s


def add_chord(buf, start, dur, notes, amp=0.22, kind="pad"):
    for n in notes:
        add_note(buf, start, dur, n, amp=amp, kind=kind)


def apply_echo(buf, delay=0.28, decay=0.32, repeats=3):
    delay_n = int(delay * SR)
    out = array("f", buf)
    for r in range(1, repeats + 1):
        gain = decay ** r
        shift = delay_n * r
        for i in range(len(buf) - shift):
            out[i + shift] += buf[i] * gain
    return out


def soft_clip(x):
    return math.tanh(x)


def save_wav(path, buf):
    peak = max(max(buf), abs(min(buf)), 1e-9)
    norm = 0.92 / peak
    with wave.open(path, "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        frames = bytearray()
        for x in buf:
            s = soft_clip(x * norm)
            frames.extend(struct.pack("<h", int(max(-1.0, min(1.0, s)) * 32767)))
        wf.writeframes(frames)


def build_pei():
    total = 24.0
    bpm = 84
    beat = 60.0 / bpm
    buf = array("f", [0.0] * int(total * SR))

    chords = [
        ["D3", "A3", "D4"],
        ["A2", "E3", "A3"],
        ["B2", "F#3", "E4"],
        ["G2", "D3", "A3"],
    ]
    for bar in range(6):
        chord = chords[bar % len(chords)]
        add_chord(buf, bar * 4 * beat, 4 * beat, chord, amp=0.13, kind="pad")

    motif = ["D4", "A4", "E5", "A4", "D5", "A4", "E5", "A4"]
    motif2 = ["D4", "F#4", "A4", "D5", "A4", "F#4", "E4", "D4"]
    for bar in range(6):
        notes = motif if bar % 2 == 0 else motif2
        for step, n in enumerate(notes):
            start = bar * 4 * beat + step * 0.5 * beat
            add_note(buf, start, 0.43 * beat, n, amp=0.25, kind="pluck")
        add_note(buf, bar * 4 * beat + 3.5 * beat, 0.8 * beat, "A5", amp=0.11, kind="bell")

    buf = apply_echo(buf, delay=0.22, decay=0.28, repeats=2)
    path = os.path.join(OUT_DIR, "01-pei-geometric-minimal.wav")
    save_wav(path, buf)
    return path


def build_mondrian():
    total = 22.0
    bpm = 118
    beat = 60.0 / bpm
    buf = array("f", [0.0] * int(total * SR))

    bass_prog = ["C2", "G1", "A1", "F1"]
    color_cells = [
        ["C4", "E4", "G4", "C5"],
        ["D4", "G4", "A4", "D5"],
        ["E4", "G4", "B4", "E5"],
        ["F4", "A4", "C5", "F5"],
    ]

    pattern = [0.0, 0.5, 1.0, 1.5, 2.5, 3.0, 3.5]
    for bar in range(10):
        root = bass_prog[bar % len(bass_prog)]
        add_note(buf, bar * 4 * beat, 3.6 * beat, root, amp=0.22, kind="bass")
        cells = color_cells[bar % len(color_cells)]
        for j, offset in enumerate(pattern):
            n = cells[j % len(cells)]
            dur = 0.22 * beat if j % 3 else 0.35 * beat
            add_note(buf, bar * 4 * beat + offset * beat, dur, n, amp=0.24, kind="pluck")
        add_note(buf, bar * 4 * beat + 1.75 * beat, 0.18 * beat, "C6", amp=0.09, kind="bell")
        if bar % 2 == 1:
            add_note(buf, bar * 4 * beat + 2.0 * beat, 0.18 * beat, "G5", amp=0.08, kind="bell")

    buf = apply_echo(buf, delay=0.16, decay=0.22, repeats=2)
    path = os.path.join(OUT_DIR, "02-mondrian-urban-grid.wav")
    save_wav(path, buf)
    return path


def build_aranya():
    total = 28.0
    bpm = 64
    beat = 60.0 / bpm
    buf = array("f", [0.0] * int(total * SR))

    pads = [
        ["A2", "E3", "A3", "C4"],
        ["F2", "C3", "A3", "C4"],
        ["C3", "G3", "C4", "E4"],
        ["G2", "D3", "B3", "D4"],
    ]
    for bar in range(7):
        chord = pads[bar % len(pads)]
        add_chord(buf, bar * 4 * beat, 4 * beat, chord, amp=0.14, kind="pad")

    steps = ["A3", "C4", "E4", "G4", "E4", "C4"]
    for i in range(12):
        base = i * 2 * beat
        if i % 3 == 0:
            add_note(buf, base, 1.8 * beat, steps[(i // 3) % len(steps)], amp=0.12, kind="bell")
        add_note(buf, base + 0.5 * beat, 1.1 * beat, steps[i % len(steps)], amp=0.15, kind="pluck")
        if i % 4 == 2:
            add_note(buf, base + 1.2 * beat, 1.4 * beat, "E5", amp=0.08, kind="bell")

    add_note(buf, 1.0, 3.0, "A4", amp=0.08, kind="bell")
    add_note(buf, 11.5, 3.4, "C5", amp=0.07, kind="bell")
    add_note(buf, 22.0, 4.2, "A4", amp=0.06, kind="bell")

    buf = apply_echo(buf, delay=0.34, decay=0.36, repeats=4)
    path = os.path.join(OUT_DIR, "03-aranya-dawn-chapel.wav")
    save_wav(path, buf)
    return path


def build_mad():
    """
    MAD 有机曲面（如长春龙嘉T3/哈尔滨大剧院）：
    - 建筑特征：巨型伞形曲面 / 放射状肋骨 / 中心柱+向外延展花瓣 / 鸟瞰对称 / 没有直角
    - 音乐人格：Organic Flow（有机流动）
        * 极慢呼吸（bpm 52）、不使用切分节奏
        * 中心"主音"持续存在（像建筑的中央粗柱）
        * 上方音符从低到高呈放射式扩散（像伞骨张开）
        * 所有音色都偏圆润（pad/bell），无 pluck 的锐感
        * 大量延迟/回响，让每一个音"漂浮"出去再慢慢落下
    """
    total = 32.0
    bpm = 52
    beat = 60.0 / bpm
    buf = array("f", [0.0] * int(total * SR))

    # 1. "中央柱"：极低的持续 pad，贯穿全曲（建筑的主茎）
    trunk = [
        ["D2", "A2", "D3"],
        ["D2", "A2", "F3"],
        ["C2", "G2", "E3"],
        ["D2", "A2", "F3"],
    ]
    for bar in range(8):
        chord = trunk[bar % len(trunk)]
        add_chord(buf, bar * 4 * beat, 4.2 * beat, chord, amp=0.11, kind="pad")

    # 2. "伞面展开"：从低到高的放射式音序，缓慢绽放
    bloom = ["D3", "F3", "A3", "D4", "F4", "A4", "D5", "F5"]
    for bar in range(6):
        base_start = bar * 5 * beat + 0.5 * beat
        for j, n in enumerate(bloom):
            # 每个音延迟 0.35 拍，形成从中心"向外张开"的时间差
            start = base_start + j * 0.35 * beat
            # 从中间最响、两端衰减（像伞骨受力）
            radial = 1.0 - abs(j - 3.5) / 3.5 * 0.45
            amp = 0.13 * radial
            add_note(buf, start, 2.2 * beat, n, amp=amp, kind="pad")

    # 3. "光点"：稀疏的 bell，从远到近，像鸟瞰里那些被夕阳照亮的飞机顶灯
    bell_seq = [
        (1.5, "A5", 0.09),
        (5.0, "D5", 0.10),
        (9.0, "F5", 0.08),
        (13.5, "A5", 0.09),
        (18.0, "C6", 0.07),
        (22.0, "D5", 0.08),
        (26.0, "A4", 0.08),
        (29.5, "F5", 0.06),
    ]
    for start, note, amp in bell_seq:
        add_note(buf, start, 3.6, note, amp=amp, kind="bell")

    # 4. "呼吸"：极低频 pad 一推一收（建筑的收缩感，对应鸟瞰图上曲面的"颈部"）
    breaths = [
        (0.0, 10.0, "D2"),
        (10.5, 10.0, "C2"),
        (21.5, 10.0, "D2"),
    ]
    for start, dur, n in breaths:
        add_note(buf, start, dur, n, amp=0.09, kind="pad")

    # 5. 长尾回响，让每个音都像在大空间里慢慢漂
    buf = apply_echo(buf, delay=0.42, decay=0.4, repeats=4)
    path = os.path.join(OUT_DIR, "04-mad-organic-flow.wav")
    save_wav(path, buf)
    return path


def main():
    paths = [build_pei(), build_mondrian(), build_aranya(), build_mad()]
    for p in paths:
        print(p)


if __name__ == "__main__":
    main()
