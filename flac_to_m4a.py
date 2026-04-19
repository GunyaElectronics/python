#!/usr/bin/env python3

import sys
import re
import subprocess
from pathlib import Path


def parse_time(t):
    m, s, f = map(int, t.split(":"))
    return m * 60 + s + f / 75.0


def parse_flac_folder(folder):

    flac_files = sorted(folder.glob("*.flac"))

    if not flac_files:
        print("No FLAC files found")
        sys.exit(1)

    tracks = []
    artist = None
    album = None

    for i, f in enumerate(flac_files, start=1):

        cmd = [
            "ffprobe",
            "-v", "error",
            "-show_entries", "format_tags=artist,album,title",
            "-of", "default=noprint_wrappers=1:nokey=0",
            str(f)
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        tags = {}
        for line in result.stdout.splitlines():
            if "=" in line:
                k, v = line.split("=", 1)
                tags[k.strip().lower()] = v.strip()

        track_artist = tags.get("artist")
        track_album = tags.get("album")
        track_title = tags.get("title", f.stem)

        if artist is None and track_artist:
            artist = track_artist

        if album is None and track_album:
            album = track_album

        tracks.append({
            "track": i,
            "title": track_title,
            "file": f.name
        })

    # fallback якщо тегів нема
    if artist is None:
        artist = "Unknown Artist"

    if album is None:
        album = folder.name

    return artist, album, tracks


def parse_cue(cue_path):

    artist = None
    album = None
    tracks = []
    current = {}
    current_file = None
    files = []

    with open(cue_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()

            if line.startswith("PERFORMER") and artist is None:
                artist = re.findall(r'"(.*)"', line)[0]

            elif line.startswith("TITLE") and album is None:
                album = re.findall(r'"(.*)"', line)[0]

            elif line.startswith("FILE"):
                current_file = re.findall(r'"(.*)"', line)[0]
                files.append(current_file)

            elif line.startswith("TRACK"):
                if current:
                    tracks.append(current)
                current = {
                    "track": int(line.split()[1]),
                    "file": current_file
                }

            elif line.startswith("TITLE") and "track" in current:
                current["title"] = re.findall(r'"(.*)"', line)[0]

            elif line.startswith("INDEX 01"):
                current["time"] = parse_time(line.split()[2])

    if current:
        tracks.append(current)

    return artist, album, tracks


def is_multifile(tracks):
    files = {t["file"] for t in tracks}
    return len(files) > 1


def run_single_image(folder, artist, album, tracks):

    audio_file = tracks[0]["file"]
    audio_path = folder / audio_file

    for i, track in enumerate(tracks):

        start = track["time"]
        end = None

        if i < len(tracks) - 1:
            end = tracks[i + 1]["time"]

        out_name = f'{track["track"]:02d} - {track["title"]}.m4a'

        cmd = [
            "ffmpeg",
            "-y",
            "-i", str(audio_path),
            "-ss", str(start),
        ]

        if end:
            cmd += ["-to", str(end)]

        cmd += [
            "-map_metadata", "-1",
            "-c:a", "alac",
            "-metadata", f"artist={artist}",
            "-metadata", f"album={album}",
            "-metadata", f"title={track['title']}",
            "-metadata", f"track={track['track']}",
            out_name
        ]

        print("\nRUN:", " ".join(cmd))

        r = subprocess.run(cmd)

        if r.returncode != 0:
            print("FFmpeg error")
            sys.exit(1)


def run_multifile(folder, artist, album, tracks):

    for track in tracks:

        cue_file = track["file"]

        # cue може писати wav але реально flac
        real_file = Path(cue_file).with_suffix(".flac")

        audio_path = folder / real_file

        out_name = f'{track["track"]:02d} - {track["title"]}.m4a'

        cmd = [
            "ffmpeg",
            "-y",
            "-i", str(audio_path),
            "-map", "0:a:0",
            "-map_metadata", "-1",
            "-c:a", "alac",
            "-metadata", f"artist={artist}",
            "-metadata", f"album={album}",
            "-metadata", f"title={track['title']}",
            "-metadata", f"track={track['track']}",
            out_name
        ]

        print("\nRUN:", " ".join(cmd))

        r = subprocess.run(cmd)

        if r.returncode != 0:
            print("FFmpeg error")
            sys.exit(1)


def main():

    if len(sys.argv) != 2:
        print("Usage: cue_split_ffmpeg.py <folder>")
        sys.exit(1)

    folder = Path(sys.argv[1])

    cue_files = list(folder.glob("*.cue"))

    if not cue_files:
        print("No CUE file — using FLAC metadata")
        artist, album, tracks = parse_flac_folder(folder)
    else:
        cue_path = cue_files[0]
        print("Using:", cue_path)
        artist, album, tracks = parse_cue(cue_path)

    print("Artist:", artist)
    print("Album:", album)
    print("Tracks:", len(tracks))

    if is_multifile(tracks):
        print("Mode: multi-file")
        run_multifile(folder, artist, album, tracks)
    else:
        print("Mode: single-image")
        run_single_image(folder, artist, album, tracks)


if __name__ == "__main__":
    main()