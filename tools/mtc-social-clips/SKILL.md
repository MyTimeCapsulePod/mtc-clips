---
name: mtc-social-clips
description: Make branded, captioned 9:16 My Time Capsule podcast clips from Zoom recordings and save them as Buffer drafts for Instagram, Facebook and X. Use whenever someone asks for an MTC clip, reel, social video or Buffer post for an episode.
---

# My Time Capsule social clips

My Time Capsule is a weekly podcast hosted by Michael Fenton Stevens (no hyphen in his name) and produced by his son John Fenton-Stevens. Guests choose five things for a time capsule: four to keep and one to bury forever. These rules cover turning a short moment from a Zoom interview into a branded vertical clip, then preparing the posts in Buffer.

## Before you start

- **Episode number:** look it up in the Google Sheet "MTC - Guests". Unpublished episodes aren't in the RSS feed, so don't use the feed for this. Never edit that sheet without checking with John first.
- **Approval:** save everything to Buffer as **drafts only**. Never schedule or post until the person you're working with has approved the drafts and given times.
- **Old drafts:** when you make a new version, delete the older Buffer drafts it replaces and keep only the latest.

## Finding the moment

Use the episode's transcript with word timings (for example from OpusClip) and the Zoom audio to search; this is much cheaper than watching video. Download the full Zoom video only once a moment is chosen. If asked for laughs, look for jokes and funny exchanges in the text, and be honest if there is no real laughter, offering the best candidates. Aim for 35 to 60 seconds with a hook at the start.

## Second Dig look (layout H)

Dig clips alternate between two looks so two posts in a row never look the same. Look 1 is navy (layout A, or G when stacked). Look 2 is layout H with `--dig --dig-look pink`: dusty pink (#CAA3B8) background, navy wordmark and frame, rounded video frame, navy name box and button with light grey text, blue "THE DIG!" tag and "DIG EP. NN" pill, captions in a two-line box under the video, yellow only for the highlighted word. (`--dig-look blue` and `grey` also exist but weren't chosen.) First Dig clip of an episode uses Look 1, the next uses Look 2.

## Captions never cover faces

In the single-video layouts (A and D) the video window is shorter and the captions sit in a box beneath it, two lines at most (the font shrinks if a chunk would wrap to three). Never put captions over a face. In stacked layouts (E, G) they are two lines of text (no box, soft shadow) centred on the divide between the two videos, so they only overlap the bottom edge of the guest and the top edge of Mike. Mike's framing varies by recording (sometimes lots of wall above his head, sometimes his head near the top), so always look at a few frames and, if a face is touched, nudge the window crop or shrink the text.

## The Dig

The Dig is the Friday companion show. Its clips use the same designs in the colours of The Dig artwork (`assets/artwork-dig.png`): add `--dig` (layouts A and G) for a navy background (#0D1118), blue (#0558CE) pills, light pink (#CAA3B8) name box and button, darker pink (#D94E53) thin lines, shovel-yellow (#FBC45F) only for the highlighted caption word, light grey (#E6E7E9) text, the Dig artwork tile, a blue "THE DIG!" tag under the wordmark and a "DIG EP. NN" pill. Rules specific to The Dig:
- Use the recording of the **guest and Mike**, not the Mike and John session.
- Dig episodes are numbered separately from main episodes (Ep. 27 exists in both), so say "The Dig Ep. NN" in captions and link with `https://mytimecapsulepodcast.com/episodes.html?q=the%20dig%20-%20ep.%20NN`, not `?q=NN`.
- The guest session folder usually has separate audio tracks per person. Transcribe each track on its own (this gives you who said what), level each with loudnorm, mix them with amix, and mux that mix over the clip instead of using the video's own audio.
- If the Zoom video is in active-speaker view (one frame cutting between speakers), it can't be stacked: use layout A with `--dig`.

## Choosing the section

Always take the clip from the main bulk of the conversation, never the first or last few minutes, which are often cut from the finished episode. Check the transcript for swearing and avoid it.

## The video

Every clip is 1080×1920 (9:16), H.264 MP4. The same video goes to all three platforms.

### Brand
- Forest green `#355C45`, teal `#22B1AB`, orange `#FEA634`, warm off-white "paper" `#F2EEE6`.
- Orange backgrounds always take green `#355C45` text, never light text.
- The wordmark is "MY TIME CAPSULE" in a heavy, rounded serif, dark (`#1f1f1f`) or green depending on the background.
- Captions use a heavy rounded sans (Poppins ExtraBold or similar).
- No wavy lines or decorative bands. Don't borrow the artwork's hills as a stripe.
- The podcast artwork (`assets/artwork.jpg`, 1500×1500) is included with this skill.

### Elements on every clip
- **Captions:** big, white with a soft dark shadow, over the video. Each word turns orange as it is spoken, karaoke style. Get word timings by transcribing the clip's audio, then check the spellings of names against the episode title.
- **Guest name box:** fitted to the text, rounded corners, top left of the guest's video. The name is in capitals, with a short description beneath it, for example "DAME EVELYN GLENNIE / World-renowned percussionist". Mike never gets a name box.
- **Episode pill:** a teal rounded pill with paper-coloured text, "EP. 616", in the top right of the guest's video.
- **Button:** a rounded button reading "Full episode out now", 680×100 px, centred, sitting just below the video at about y 1400–1560.
- **Safe zones:** keep the bottom ~400 px free of anything important, and keep the right-hand edge in the lower half clear. Instagram puts its caption text and like, comment and share buttons there.

### Layouts (first clip of an episode: cream background)
- **Cream header (layouts D and E):** at the top left, the artwork as a 190 px tile, tilted about −3°, with a 6 px white border and a soft shadow. "MY TIME CAPSULE" sits beside it in black, about 64 px.
- **Layout E** is for side-by-side recordings, which is the default from now on. The background is paper `#F2EEE6`, with the cream header at the top. The guest's video fills the full width from y 250 to about y 828, with Mike's video directly below it to about y 1410. The captions sit in a dark, semi-transparent rounded box near the top of Mike's panel.
- **Layout D** is for single-camera recordings that cut between speakers. The background is paper, with the wordmark at the top. One full-width video runs from y 260 to y 1340, with the captions near the bottom of it.
- On the first clip, the guest name box is orange with green text and the button is green with paper-coloured text.

### Second and later clips for the same episode
These need to look different from the first clip, so people don't scroll past thinking they've already seen it. The first clip uses the cream look, then later clips alternate **Look A → Look B → Look A…** so no two posts in a row look the same.

- **Look A (green):**
  - Deep green `#355C45` background.
  - At the top left, the artwork as a 210 px tile, tilted about −3°, with a 6 px paper border and a soft shadow. "MY TIME CAPSULE" sits beside it in paper colour, about 64 px. Nothing else goes at the top.
  - Full-width video from about y 310 to y 1350, with thin 6 px orange lines above and below.
  - Orange name box with green text.
  - Orange button with green text.
- **Look B (orange):**
  - Orange `#FEA634` background, with a green wordmark centred at the top (about 84 px).
  - The video is inset 60 px from each side, in a frame with rounded corners (about 40 px) and an 8 px green edge, from about y 270 to y 1280.
  - Green name box with paper-coloured name and orange description.
  - The artwork as a 240 px badge, tilted about −4°, with a 7 px green border, overlapping the frame's **bottom-left** corner. Never put it on the right, where Instagram's buttons sit.
  - Green button with paper-coloured text, placed to the right of the badge.

### Building it: use `scripts/make_clip.py`
The skill includes the script that draws all four looks. The fonts are in `fonts/` (open licence) and the artwork is in `assets/`, so always use the script rather than redrawing the layouts by hand. It needs ffmpeg and Pillow, plus `pip install faster-whisper` for the captions.

```
python3 scripts/make_clip.py --video zoom.mp4 --start 12:03 --end 12:55 \
  --layout E --guest "Dame Evelyn Glennie" --desc "World-renowned percussionist" \
  --ep 616 --out evelyn-timpani.mp4
```

- `--layout`: D, E, A, B or G, following the rules above. **G is Look A (green) with the guest on top and Mike below**, for second clips of side-by-side recordings (use `--guest-crop 0:180:640:360 --mike-crop 640:180:640:360` for a 1280×720 Zoom gallery view with black bars). Look B stays a single video.
- `--start` / `--end`: where the moment sits in the recording.
- The first run transcribes the clip and saves `<out>.words.json`. Read it and fix any misheard words, especially names. Then run the same command again with `--words <out>.words.json`.
- **Layout E:** by default the guest is the left half of a side-by-side recording and Mike is the right half. Use `--guest-side right` to swap them, or give exact areas with `--guest-crop x:y:w:h` and `--mike-crop x:y:w:h`.
- **Layouts D, A and B:** `--guest-crop x:y:w:h` picks which part of the recording to show. Leave it out to use the whole frame.
- **Levelling Mike (layouts E and G):** Mike's Zoom audio is usually far quieter than the guest's. Pass `--mike-ranges` with the seconds, counted from the start of the clip, where Mike speaks (for example `--mike-ranges 25.6-40`; get them from the transcript timings). The script boosts him by 14 dB there (`--mike-gain` to change it), limits peaks and levels the whole clip to about -16 LUFS. Check afterwards that both speakers measure about the same average level with ffmpeg's volumedetect.
- **Ending:** end the clip on the last wanted word. Trim off any stray trailing word of Mike's (a tell-tale "and and"), then transcribe the last two seconds of the finished file to confirm.
- **First frame:** the very first frame is what people see before a post plays, so it must show the full layout with the video in place, never a black window. The script pads the start for this. Always extract frame 0 with `ffmpeg -i clip.mp4 -vf select=eq(n\,0) -frames:v 1 f0.jpg`, look at it, and fix it before uploading if the video is missing.
- **Checking:** pull a still or two with ffmpeg and look at them before uploading. Check that faces aren't cut off and the captions read correctly.

## The posts (Buffer)

Use three channels: Instagram (Reel, shared to feed), the Facebook page "My Time Capsule" (Reel), and X @fentonstevens, which is Mike's account and has the biggest following. Times are Europe/London.

**Captions must match what is said in the clip.** Re-read the clip's final transcript before writing them, and never state anything the guest didn't say or imply.

**Every caption on every platform includes the episode number**, for example "Ep. 616".

- **Instagram:** replace names with @handles, with no brackets and without repeating the name: the guest's handle, @mikefentonstevens, and anyone else mentioned. Find handles on official websites. End with "Link in bio", because links in Instagram captions aren't clickable. Add a few hashtags, such as #MyTimeCapsule and the guest's name. Collaborators (the guest and Mike) can't be set through Buffer's connection, so tell the person to add them by hand in Buffer's editor.
- **Facebook:** use plain names, no @tags. Include the episode link (below). Add a few hashtags.
- **X:** replace names with @handles. **Never start the post with an @**, because X then treats it as a reply that only mutual followers see. Lead with a word or an emoji. Mention @MyTCpod. Include the episode link. Keep the whole post under 280 characters; a link counts as 23.
- **Episode link (Facebook and X):** `https://mytimecapsulepodcast.com/episodes.html?q=NNN`. You can write it before release, because it works once the episode is out.

**Timing:** episodes go live at 00:02 on Mondays, so "out now" is safe all of release day. Stagger the platforms on release day: Facebook 12:30, X 14:00, Instagram 18:00. Instagram followers are most active from 18:00 to 21:00 on Sundays, Mondays and Wednesdays.

**Re-made clips:** give each new version a new filename (v2, v3) so Buffer fetches the new file instead of a cached copy, and remove the superseded file from the repo.

**Video link for Buffer:** Buffer needs a public, direct link to the MP4. The clips are stored in the GitHub repo `MyTimeCapsulePod/mtc-clips` under `clips/`, and the link takes the form `https://raw.githubusercontent.com/MyTimeCapsulePod/mtc-clips/main/clips/<file>.mp4`. If you can't upload there, give the person the MP4 and ask them to attach it to the drafts in Buffer themselves.
