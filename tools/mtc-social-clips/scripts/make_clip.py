#!/usr/bin/env python3
"""Build a branded 1080x1920 My Time Capsule clip from a Zoom recording.

Layouts
  D  cream, one full-width video (single camera that cuts between speakers)
  E  cream, guest on top and Mike below (side-by-side Zoom recording)
  A  second-clip look: deep green, artwork tile at top left
  B  second-clip look: orange, framed video, artwork badge bottom left

Example
  python3 make_clip.py --video zoom.mp4 --start 12:03 --end 12:55 \
      --layout E --guest "Dame Evelyn Glennie" \
      --desc "World-renowned percussionist" --ep 616 --out clip.mp4

The first run transcribes the clip and saves <out>.words.json beside the
output. Fix any misheard words or names in that file, then run the same
command again with --words <out>.words.json to rebuild with your corrections.

Needs: ffmpeg, Pillow, and faster-whisper (pip install faster-whisper) for
the transcription step.
"""
import argparse, json, os, subprocess, sys, tempfile

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FONTS = os.path.join(ROOT, "fonts")
ARTWORK = os.path.join(ROOT, "assets", "artwork.jpg")

W, H = 1080, 1920
GREEN, TEAL, ORANGE, PAPER = "#355C45", "#22B1AB", "#FEA634", "#F2EEE6"
INK = "#1f1f1f"
HL = {}  # second Dig look colours (layout H), set in main from --dig-look
ACCENT = LINE = ORANGE  # name box / button, and thin lines (pinks in The Dig palette)
DIG = False  # set by --dig: The Dig palette and artwork


# ---------- helpers ----------

def font(name, size):
    if name == "wordmark":
        f = ImageFont.truetype(os.path.join(FONTS, "Fraunces.ttf"), size)
        try:
            f.set_variation_by_axes([36, 900, 100, 0])  # opsz, wght, SOFT, WONK
        except Exception:
            pass
        return f
    return ImageFont.truetype(os.path.join(FONTS, f"Poppins-{name}.ttf"), size)


def tsec(v):
    """'12:03.5' or '1:02:03' or '723.5' -> seconds"""
    if v is None:
        return None
    parts = [float(p) for p in str(v).split(":")]
    s = 0.0
    for p in parts:
        s = s * 60 + p
    return s


def text_w(draw, text, f):
    l, t, r, b = draw.textbbox((0, 0), text, font=f)
    return r - l


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.stderr.write(r.stderr[-3000:])
        raise SystemExit(f"Command failed: {' '.join(cmd[:4])} ...")
    return r


# ---------- layout geometry ----------

def layout_spec(layout):
    """Video windows (x, y, w, h, radius) plus where the overlays go."""
    if layout == "D":
        return dict(bg=PAPER, windows=[(0, 260, 1080, 1000, 0)], guest_win=0,
                    cap=dict(mode="box", top=1282, size=58, chars=27, maxlines=2),
                    cta=dict(x=200, y=1532, w=680, fill=GREEN, ink=PAPER))
    if layout == "E":
        return dict(bg=PAPER, windows=[(0, 250, 1080, 578, 0), (0, 834, 1080, 576, 0)],
                    guest_win=0,
                    cap=dict(mode="seam", seam=831, size=56, chars=27, maxlines=2),
                    cta=dict(x=200, y=1462, w=680, fill=GREEN, ink=PAPER))
    if layout == "A":
        return dict(bg=GREEN, windows=[(0, 300, 1080, 960, 0)], guest_win=0,
                    cap=dict(mode="box", top=1282, size=58, chars=27, maxlines=2),
                    cta=dict(x=200, y=1532, w=680, fill=ACCENT, ink=GREEN))
    if layout == "B":
        return dict(bg=ORANGE, windows=[(68, 278, 944, 994, 32)], guest_win=0,
                    cap=dict(mode="over", bottom=1280 - 150, size=62),
                    cta=dict(x=330, y=1310, w=560, fill=GREEN, ink=PAPER))
    if layout == "G":  # Look A (green) with the guest and Mike stacked
        return dict(bg=GREEN, windows=[(0, 290, 1080, 576, 0), (0, 872, 1080, 576, 0)],
                    guest_win=0,
                    cap=dict(mode="seam", seam=869, size=56, chars=27, maxlines=2),
                    cta=dict(x=200, y=1490, w=680, fill=ACCENT, ink=GREEN))
    if layout == "H":  # second Dig look: rounded video frame on a coloured background
        return dict(bg=HL["bg"], windows=[(40, 310, 1000, 930, 32)], guest_win=0,
                    cap=dict(mode="box", top=1262, size=58, chars=27, maxlines=2),
                    cta=dict(x=200, y=1510, w=680, fill=HL["btn"], ink=HL["btn_ink"]))
    raise SystemExit("layout must be D, E, A, B, G or H")


# ---------- static foreground (everything except video and captions) ----------

def name_box(d, x, y, name, desc, fill, name_ink, desc_ink):
    fn, fd = font("ExtraBold", 40), font("Bold", 28)
    name = name.upper()
    bw = max(text_w(d, name, fn), text_w(d, desc, fd) if desc else 0) + 56
    bh = 120 if desc else 74
    d.rounded_rectangle((x, y, x + bw, y + bh), radius=26, fill=fill)
    d.text((x + 28, y + 14), name, font=fn, fill=name_ink)
    if desc:
        d.text((x + 28, y + 66), desc, font=fd, fill=desc_ink)


def ep_pill(d, right, y, ep, fill=None):
    f = font("ExtraBold", 32)
    label = f"DIG EP. {ep}" if DIG else f"EP. {ep}"
    pw = text_w(d, label, f) + 56
    d.rounded_rectangle((right - pw, y, right, y + 62), radius=31, fill=fill or TEAL)
    d.text((right - pw + 28, y + 9), label, font=f, fill=PAPER)


def cta(d, spec):
    x, y, w = spec["x"], spec["y"], spec["w"]
    d.rounded_rectangle((x, y, x + w, y + 100), radius=50, fill=spec["fill"])
    f = font("ExtraBold", 42)
    label = "Full episode out now"
    d.text((x + (w - text_w(d, label, f)) / 2, y + 22), label, font=f, fill=spec["ink"])


def wordmark(d, cx, y, size, ink):
    f = font("wordmark", size)
    label = "MY TIME CAPSULE"
    d.text((cx - text_w(d, label, f) / 2, y), label, font=f, fill=ink)


def artwork_tile(size, border, border_col, angle):
    art = Image.open(ARTWORK).convert("RGB").resize((size, size), Image.LANCZOS)
    tile = Image.new("RGBA", (size + 2 * border, size + 2 * border), border_col)
    tile.paste(art, (border, border))
    rot = tile.rotate(angle, resample=Image.BICUBIC, expand=True)
    shadow = Image.new("RGBA", (rot.width + 80, rot.height + 80), (0, 0, 0, 0))
    alpha = rot.split()[3].point(lambda a: int(a * 0.35))
    shadow.paste((0, 0, 0, 255), (40, 54), alpha)
    shadow = shadow.filter(ImageFilter.GaussianBlur(14))
    shadow.alpha_composite(rot, (40, 40))
    return shadow  # draw at (x - 40, y - 40)


def build_foreground(layout, spec, guest, desc, ep):
    fg = Image.new("RGBA", (W, H), spec["bg"])
    # punch transparent windows for the video
    hole = Image.new("L", (W, H), 255)
    hd = ImageDraw.Draw(hole)
    for (x, y, w, h, r) in spec["windows"]:
        if r:
            hd.rounded_rectangle((x, y, x + w - 1, y + h - 1), radius=r, fill=0)
        else:
            hd.rectangle((x, y, x + w - 1, y + h - 1), fill=0)
    fg.putalpha(hole)
    d = ImageDraw.Draw(fg)

    gx, gy, gw, gh, _ = spec["windows"][spec["guest_win"]]
    if layout in ("D", "E"):
        tile = artwork_tile(190, 6, "#ffffff", 3)
        fg.alpha_composite(tile, (70 - 40, 26 - 40))
        d.text((322, 98), "MY TIME CAPSULE", font=font("wordmark", 64), fill=INK)
        name_box(d, gx + 36, gy + 36, guest, desc, ORANGE, GREEN, GREEN)
        ep_pill(d, gx + gw - 36, gy + 36, ep)
    elif layout in ("A", "G"):
        tile = artwork_tile(210, 6, PAPER, 3)
        fg.alpha_composite(tile, (70 - 40, 46 - 40))
        f = font("wordmark", 64)
        if DIG:
            d.text((340, 84), "MY TIME CAPSULE", font=f, fill=PAPER)
            ft = font("ExtraBold", 36)
            tw = text_w(d, "THE DIG!", ft) + 56
            d.rounded_rectangle((340, 186, 340 + tw, 252), radius=33, fill=TEAL)
            d.text((340 + 28, 192), "THE DIG!", font=ft, fill=PAPER)
        else:
            d.text((340, 128), "MY TIME CAPSULE", font=f, fill=PAPER)
        if layout == "G":
            for (_, wy, _, wh, _) in spec["windows"]:
                d.rectangle((0, wy, W, wy + 5), fill=LINE)
                d.rectangle((0, wy + wh - 6, W, wy + wh - 1), fill=LINE)
        else:
            d.rectangle((0, gy, W, gy + 5), fill=LINE)
            d.rectangle((0, gy + gh - 6, W, gy + gh - 1), fill=LINE)
        name_box(d, gx + 36, gy + 36, guest, desc, ACCENT, GREEN, GREEN)
        ep_pill(d, gx + gw - 36, gy + 36, ep)
    elif layout == "H":
        tile = artwork_tile(210, 6, HL["tile_border"], 3)
        fg.alpha_composite(tile, (70 - 40, 46 - 40))
        d.text((340, 84), "MY TIME CAPSULE", font=font("wordmark", 64), fill=HL["ink"])
        ft = font("ExtraBold", 36)
        tw = text_w(d, "THE DIG!", ft) + 56
        d.rounded_rectangle((340, 186, 340 + tw, 252), radius=33, fill=HL["tag"])
        d.text((340 + 28, 192), "THE DIG!", font=ft, fill=PAPER)
        d.rounded_rectangle((gx - 4, gy - 4, gx + gw + 3, gy + gh + 3), radius=36, outline=HL["frame"], width=8)
        name_box(d, gx + 24, gy + 24, guest, desc, HL["name"], HL["name_ink"], HL["name_ink"])
        ep_pill(d, gx + gw - 24, gy + 24, ep, fill=HL["pill"])
    elif layout == "B":
        wordmark(d, W / 2, 118, 84, GREEN)
        d.rounded_rectangle((60, 270, 1019, 1279), radius=40, outline=GREEN, width=8)
        name_box(d, gx + 20, gy + 20, guest, desc, GREEN, PAPER, ORANGE)
        ep_pill(d, gx + gw - 20, gy + 20, ep)
        badge = artwork_tile(240, 7, GREEN, 4)
        fg.alpha_composite(badge, (40 - 40, 1150 - 40))
    cta(d, spec["cta"])
    return fg


# ---------- captions ----------

def group_words(words, max_chars=34, max_lines=2, max_gap=0.8):  # max_chars set per layout
    """Split the word list into on-screen chunks of up to two lines."""
    chunks, cur, line_len, lines = [], [], 0, 1
    for i, w in enumerate(words):
        t = w["word"].strip()
        gap = (w["start"] - cur[-1]["end"]) if cur else 0
        add = len(t) + (1 if line_len else 0)
        if cur and (gap > max_gap or (line_len + add > max_chars and lines >= max_lines)):
            chunks.append(cur)
            cur, line_len, lines = [], 0, 1
            add = len(t)
        elif line_len + add > max_chars:
            lines += 1
            line_len = 0
            add = len(t)
        cur.append(w)
        line_len += add
        if t.endswith((".", "?", "!")) and line_len > 12 and len(cur) > 3:
            chunks.append(cur)
            cur, line_len, lines = [], 0, 1
    if cur:
        chunks.append(cur)
    return chunks


def wrap(d, words, f, max_w):
    lines, cur = [], []
    for i, w in enumerate(words):
        trial = " ".join(x for _, x in cur + [(i, w)])
        if cur and text_w(d, trial, f) > max_w:
            lines.append(cur)
            cur = []
        cur.append((i, w))
    if cur:
        lines.append(cur)
    return lines


def caption_image(chunk_words, hi, spec):
    cap = spec["cap"]
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    size = cap["size"]
    texts = [w["word"].strip() for w in chunk_words]
    max_w = 900 if cap["mode"] == "box" else 920
    while True:
        f = font("ExtraBold", size)
        lines = wrap(d, texts, f, max_w)
        if len(lines) <= cap.get("maxlines", 99) or size <= 36:
            break
        size -= 2
    lh = int(size * 1.25)
    block_h = lh * len(lines)
    if cap["mode"] == "box":
        top = cap["top"] + 40
        d.rounded_rectangle((60, cap["top"], 1020, cap["top"] + block_h + 80),
                            radius=30, fill=(28, 22, 18, 200))
    elif cap["mode"] == "seam":  # centred on the divide between the two stacked videos
        top = cap["seam"] - block_h // 2
    else:
        top = cap["bottom"] - block_h
    space = text_w(d, " ", f)
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    for li, line in enumerate(lines):
        y = top + li * lh
        lw = text_w(d, " ".join(t for _, t in line), f)
        x = (W - lw) / 2
        for idx, t in line:
            col = ORANGE if idx == hi else "#ffffff"
            if cap["mode"] in ("over", "seam"):
                sd.text((x, y + 4), t, font=f, fill=(0, 0, 0, 200))
            d.text((x, y), t, font=f, fill=col)
            x += text_w(d, t, f) + space
    if cap["mode"] in ("over", "seam"):
        shadow = shadow.filter(ImageFilter.GaussianBlur(9))
        shadow.alpha_composite(img)
        return shadow
    return img


def build_captions(words, spec, tmp, duration):
    chunks = group_words(words, max_chars=spec["cap"].get("chars", 34))
    blank = os.path.join(tmp, "cap_blank.png")
    Image.new("RGBA", (W, H), (0, 0, 0, 0)).save(blank)
    entries, t = [], 0.0  # (file, start)
    n = 0
    for ci, ch in enumerate(chunks):
        nxt = chunks[ci + 1][0]["start"] if ci + 1 < len(chunks) else None
        chunk_end = min(nxt, ch[-1]["end"] + 0.6) if nxt else min(duration, ch[-1]["end"] + 0.6)
        for wi, w in enumerate(ch):
            start = w["start"]
            path = os.path.join(tmp, f"cap_{n:04d}.png")
            caption_image(ch, wi, spec).save(path)
            entries.append((path, start))
            n += 1
        entries.append((blank, chunk_end))
    entries.sort(key=lambda e: e[1])
    lines, cur_t = [], 0.0
    first = entries[0][1] if entries else duration
    if first > 0:
        lines += [f"file '{blank}'", f"duration {first:.3f}"]
    for i, (p, s) in enumerate(entries):
        e = entries[i + 1][1] if i + 1 < len(entries) else duration
        dur = max(0.04, e - s)
        lines += [f"file '{p}'", f"duration {dur:.3f}"]
    lines.append(f"file '{blank}'")
    lst = os.path.join(tmp, "caps.txt")
    with open(lst, "w") as fh:
        fh.write("\n".join(lines) + "\n")
    return lst


# ---------- transcription ----------

def transcribe(video, start, end, tmp, model_name):
    import numpy as np
    from faster_whisper import WhisperModel
    # decode the audio with ffmpeg ourselves (avoids PyAV version problems)
    cmd = ["ffmpeg", "-loglevel", "error", "-ss", str(start or 0), "-i", video]
    if end is not None:
        cmd += ["-t", str(end - (start or 0))]
    cmd += ["-vn", "-ac", "1", "-ar", "16000", "-f", "f32le", "-"]
    r = subprocess.run(cmd, capture_output=True)
    if r.returncode != 0:
        raise SystemExit(r.stderr.decode()[-2000:])
    audio = np.frombuffer(r.stdout, dtype=np.float32)
    model = WhisperModel(model_name, device="cpu", compute_type="int8")
    segs, _ = model.transcribe(audio, word_timestamps=True, language="en")
    words = []
    for s in segs:
        for w in s.words:
            words.append({"word": w.word.strip(), "start": round(w.start, 2), "end": round(w.end, 2)})
    return words


# ---------- main ----------

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--video", required=True, help="Zoom recording (any size)")
    ap.add_argument("--start", help="clip start in the recording, e.g. 12:03.5")
    ap.add_argument("--end", help="clip end in the recording")
    ap.add_argument("--layout", required=True, choices=["D", "E", "A", "B", "G", "H"])
    ap.add_argument("--guest", required=True, help="guest name as it should appear")
    ap.add_argument("--desc", default="", help='short description, e.g. "World-renowned cellist"')
    ap.add_argument("--ep", required=True, help="episode number from the MTC - Guests sheet")
    ap.add_argument("--out", required=True)
    ap.add_argument("--words", help="word timings JSON (made by the first run; edit to fix words)")
    ap.add_argument("--guest-crop", help="x:y:w:h of the guest in the recording (layouts D, A, B, and E top)")
    ap.add_argument("--mike-crop", help="x:y:w:h of Mike in the recording (layout E bottom)")
    ap.add_argument("--guest-side", default="left", choices=["left", "right"],
                    help="layout E without crops: which half of a side-by-side recording is the guest")
    ap.add_argument("--mike-ranges", help="seconds in the CLIP where Mike speaks, e.g. 25.6-40 or 5-9,25.6-40; "
                    "his audio is boosted there (his Zoom track is usually much quieter than the guest's)")
    ap.add_argument("--mike-gain", type=float, default=14.0, help="dB boost for --mike-ranges (default 14)")
    ap.add_argument("--dig", action="store_true", help="The Dig colours (navy/blue/yellow palette from The Dig artwork, THE DIG! tag; layouts A and G)")
    ap.add_argument("--dig-look", default="blue", choices=["blue", "grey", "pink"],
                    help="layout H (second Dig look): blue or grey background")
    ap.add_argument("--model", default="small.en", help="faster-whisper model for transcription")
    a = ap.parse_args()

    start, end = tsec(a.start), tsec(a.end)
    global DIG, GREEN, TEAL, ORANGE, PAPER, ARTWORK, ACCENT, LINE
    DIG = a.dig
    if DIG:  # colours and artwork taken from The Dig artwork (navy, blue, yellow shovel, light grey)
        GREEN, TEAL, ORANGE, PAPER = "#0D1118", "#0558CE", "#FBC45F", "#E6E7E9"
        ACCENT, LINE = "#CAA3B8", "#D94E53"  # light pink (name box, button), darker pink (lines)
        ARTWORK = os.path.join(ROOT, "assets", "artwork-dig.png")
    if a.layout == "H":
        NAVY, BLUE, PINK, RED, GREY = "#0D1118", "#0558CE", "#CAA3B8", "#D94E53", "#E6E7E9"
        if a.dig_look == "blue":
            HL.update(bg=BLUE, ink=GREY, tag=NAVY, tile_border=GREY, frame=PINK, name=PINK, name_ink=NAVY,
                      pill=NAVY, btn=PINK, btn_ink=NAVY)
        elif a.dig_look == "pink":
            HL.update(bg=PINK, ink=NAVY, tag=BLUE, tile_border=NAVY, frame=NAVY, name=NAVY, name_ink=GREY,
                      pill=BLUE, btn=NAVY, btn_ink=GREY)
        else:
            HL.update(bg=GREY, ink=NAVY, tag=BLUE, tile_border=NAVY, frame=RED, name=NAVY, name_ink=GREY,
                      pill=BLUE, btn=NAVY, btn_ink=GREY)
    spec = layout_spec(a.layout)

    probe = run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                 "stream=width,height", "-show_entries", "format=duration", "-of", "json", a.video])
    info = json.loads(probe.stdout)
    sw, sh = info["streams"][0]["width"], info["streams"][0]["height"]
    total = float(info["format"]["duration"])
    s0 = start or 0.0
    duration = (end or total) - s0

    with tempfile.TemporaryDirectory() as tmp:
        if a.words:
            words = json.load(open(a.words))
        else:
            print("Transcribing...")
            words = transcribe(a.video, start, end, tmp, a.model)
            wpath = os.path.splitext(a.out)[0] + ".words.json"
            with open(wpath, "w") as fh:
                json.dump(words, fh, indent=1, ensure_ascii=False)
            print(f"Saved word timings to {wpath} (edit it to fix any words, then rerun with --words)")

        fg = build_foreground(a.layout, spec, a.guest, a.desc, a.ep)
        fg_path = os.path.join(tmp, "fg.png")
        fg.save(fg_path)
        caps = build_captions(words, spec, tmp, duration)

        # crops for each video window
        crops = []
        if a.layout in ("E", "G"):
            half = (0, 0, sw // 2, sh), (sw // 2, 0, sw - sw // 2, sh)
            g_def, m_def = (half[0], half[1]) if a.guest_side == "left" else (half[1], half[0])
            crops.append(tuple(map(int, a.guest_crop.split(":"))) if a.guest_crop else g_def)
            crops.append(tuple(map(int, a.mike_crop.split(":"))) if a.mike_crop else m_def)
        else:
            crops.append(tuple(map(int, a.guest_crop.split(":"))) if a.guest_crop else (0, 0, sw, sh))

        inp = ["-ss", str(s0), "-t", f"{duration:.3f}", "-i", a.video]
        filt = [f"color=c=black:s={W}x{H}:r=30:d={duration:.3f}[base]"]
        last = "base"
        for i, ((x, y, w, h, _), (cx, cy, cw, ch)) in enumerate(zip(spec["windows"], crops)):
            filt.append(f"[0:v]fps=30:start_time=0,crop={cw}:{ch}:{cx}:{cy},scale={w}:{h}:force_original_aspect_ratio=increase,"
                        f"crop={w}:{h},setsar=1[v{i}]")
            filt.append(f"[{last}][v{i}]overlay={x}:{y}:shortest=1[b{i}]")
            last = f"b{i}"
        filt.append(f"[{last}][1:v]overlay=0:0[f]")
        filt.append("[2:v]format=rgba[c]")
        filt.append("[f][c]overlay=0:0:eof_action=pass,format=yuv420p[out]")
        af = []
        if a.mike_ranges:
            en = "+".join(f"between(t,{r.split('-')[0]},{r.split('-')[1]})" for r in a.mike_ranges.split(","))
            af.append(f"volume={a.mike_gain}dB:enable='{en}'")
            af.append("alimiter=limit=0.9:level=disabled")
        af.append("loudnorm=I=-16:TP=-1.5:LRA=7")
        af.append(f"afade=t=out:st={max(duration - 0.35, 0):.2f}:d=0.3")
        audio_filter = ",".join(af)
        cmd = (["ffmpeg", "-y", "-loglevel", "error"] + inp +
               ["-loop", "1", "-i", fg_path, "-f", "concat", "-safe", "0", "-i", caps,
                "-filter_complex", ";".join(filt), "-map", "[out]", "-map", "0:a?",
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-r", "30",
                "-af", audio_filter, "-c:a", "aac", "-b:a", "160k", "-t", f"{duration:.3f}", "-movflags", "+faststart", a.out])
        print("Rendering...")
        run(cmd)
    print(f"Done: {a.out}")


if __name__ == "__main__":
    main()
