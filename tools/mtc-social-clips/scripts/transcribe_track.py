import sys, subprocess, json, numpy as np
from faster_whisper import WhisperModel
src, out = sys.argv[1], sys.argv[2]
raw = subprocess.run(["ffmpeg","-v","error","-i",src,"-f","f32le","-ac","1","-ar","16000","-"],capture_output=True).stdout
a = np.frombuffer(raw, dtype=np.float32)
m = WhisperModel("base", device="cpu", compute_type="int8")
segs,_ = m.transcribe(a, word_timestamps=True, language="en", vad_filter=True)
words=[]
for s in segs:
    for w in s.words: words.append([round(w.start,2), round(w.end,2), w.word])
json.dump(words, open(out,"w"))
print(out, len(words))
