"""Rebuild a Dig clip source from separate Zoom audio tracks (active-speaker video).

Used for Dig Ep. 28 (Rosie Holt) v3. Edit the constants at the top, then run:
  python3 -I build_active_speaker_source.py
Needs: video.mp4, rosie.m4a (guest track), mike.m4a (Mike track) and the word
timings rosie.json / mike.json from transcribe_track.py (each track transcribed
separately, [[start, end, word], ...] in recording seconds), all in /home/claude/src/.
Writes mix.wav and assembled.mp4 (video segments + levelled, gated audio mix).
Then run make_clip.py on assembled.mp4 with --start 0 --end <duration minus a little>.

Lessons baked in (Rosie v1 had the last word clipped, v2 lost words):
- A0-A1 / B0-B1 are the kept source segments (a jump cut removes a pause/"um"). Cut inside silence.
- End the clip at least ~0.5 s after the last wanted word: make_clip.py fades the audio out over the final 0.3 s.
- The gate mutes each track outside its own word windows. NEVER drop long words from the gate (whisper
  stretches words over pauses, e.g. "interesting" 1.3 s); only drop hallucinated "yes/yeah" runs late on.
- Where the guest's track has bleed or overlapping speech under Mike's lines, force_mute the guest track
  so Mike's short replies ("Yes. I know. Oh God.") come through and get captioned.
"""
import json, subprocess, sys
S="/home/claude/src/"
A0,A1,B0,B1 = 1793.50, 1795.40, 1797.45, 1835.45
LA = A1-A0
BASE=1790.0
M=json.load(open(S+"mike.json")); R=json.load(open(S+"rosie.json"))
def wins(words, maxdur=1.0, pad=0.25, gap=0.6):
    ws=[(w[0],w[1]) for w in words if 1790<w[0]<1840 and not (w[0]>=1830 and (w[1]-w[0])>maxdur)]
    out=[]
    for s,e in ws:
        s-=pad; e+=pad
        if out and s-out[-1][1]<gap: out[-1][1]=max(out[-1][1],e)
        else: out.append([s,e])
    return out
def closed_expr(open_w):
    # volume enabled (muted) when NOT inside any open window; times relative to BASE
    return "+".join(f"between(t,{s-BASE:.3f},{e-BASE:.3f})" for s,e in open_w)
def track(name, path, open_w):
    ex = closed_expr(open_w)
    f = (f"[0:a]atrim={A0-BASE}:{A1-BASE},asetpts=PTS-STARTPTS[x0];"
         f"[0:a]atrim={B0-BASE}:{B1-BASE},asetpts=PTS-STARTPTS[x1];")
    return ex
# gate first (in source-relative time), then trim and concat, then level
def build(path, open_w, out, force_mute=None):
    ex = closed_expr(open_w)
    fm = f"+between(t,{force_mute[0]-BASE:.3f},{force_mute[1]-BASE:.3f})" if force_mute else ""
    fc = (f"[0:a]volume=enable='not({ex}){fm}':volume=0,"
          f"loudnorm=I=-18:TP=-2:LRA=9[g];"
          f"[g]asplit[g0][g1];"
          f"[g0]atrim={A0-BASE}:{A1-BASE},asetpts=PTS-STARTPTS,afade=t=out:st={LA-0.03:.3f}:d=0.03[x0];"
          f"[g1]atrim={B0-BASE}:{B1-BASE},asetpts=PTS-STARTPTS,afade=t=in:st=0:d=0.03[x1];"
          f"[x0][x1]concat=n=2:v=0:a=1[o]")
    subprocess.run(["ffmpeg","-y","-v","error","-ss",str(BASE),"-t","50","-i",path,"-filter_complex",fc,"-map","[o]","-ar","48000","-ac","1",out],check=True)
build(S+"rosie.m4a", wins(R), S+"rosie_seg.wav", force_mute=(1817.95,1821.4))
build(S+"mike.m4a", wins(M, maxdur=1.5), S+"mike_seg.wav")
subprocess.run(["ffmpeg","-y","-v","error","-i",S+"rosie_seg.wav","-i",S+"mike_seg.wav","-filter_complex","amix=inputs=2:normalize=0:duration=longest[o]","-map","[o]",S+"mix.wav"],check=True)
# video: same two segments, no audio
fc=(f"[0:v]trim={A0}:{A1},setpts=PTS-STARTPTS[v0];[0:v]trim={B0}:{B1},setpts=PTS-STARTPTS[v1];[v0][v1]concat=n=2:v=1:a=0[v]")
subprocess.run(["ffmpeg","-y","-v","error","-i",S+"video.mp4","-i",S+"mix.wav","-filter_complex",fc,"-map","[v]","-map","1:a","-c:v","libx264","-preset","veryfast","-crf","16","-r","25","-c:a","aac","-b:a","192k","-shortest",S+"assembled.mp4"],check=True)
print("ok")
