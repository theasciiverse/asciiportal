#!/usr/bin/env python3
"""Records asciiverse/asciiportal.cast, ASCIIpOrtal's catalog preview, at
100x30 (hub/RECORDING.md): level 2, "Momentary Switches and Portals",
played from the start through the portals. Climb out of the box room,
nudge the dropped box onto the switch, then stand on the door switch,
shoot one portal behind and one through the open door, and walk through.
Then back to the menu and quit.

The moves are fixed: they were worked out by hand and the level plays
the same every time. A fresh HOME with a save at level 2 keeps your own
progress out. Held keys are sent as autorepeat (30 a second). The game
runs in tmux (a real terminal emulator) and asciinema 3 records inside.
Usage, from the repo root after asciiverse/build.sh and stage.sh:
    python3 asciiverse/record-preview.py"""
import os, subprocess, sys, tempfile, time

s = "asciiportal-preview"
home = tempfile.mkdtemp()
os.makedirs(f"{home}/.asciiportal")
with open(f"{home}/.asciiportal/default.yaml", "w") as f:
    f.write("version: 1\nnumportals: 0\nnumdeaths: 0\nnumticks: 0\n"
            "numsteps: 0\nnumlevels: 0\nmaxlevel: 2\nlastlevel: 2\n")

def screen():
    return subprocess.run(["tmux", "capture-pane", "-p", "-t", s],
                          capture_output=True, text=True).stdout
def key(k, wait=0.25):
    subprocess.run(["tmux", "send-keys", "-t", s, k]); time.sleep(wait)
def taps(k, n, wait=0.25):
    for _ in range(n): key(k, wait)
def hold(k, secs):
    """a key held down: one tap to turn, then terminal autorepeat"""
    key(k, 0.15)
    for _ in range(int(secs * 30)): key(k, 0.033)

subprocess.run(["tmux", "kill-session", "-t", s], stderr=subprocess.DEVNULL)
subprocess.run(["tmux", "new-session", "-d", "-s", s, "-x", "100", "-y", "30",
    f"HOME={home} TERM=xterm-256color COLORTERM=truecolor LANG=C.UTF-8 "
    "asciinema rec --overwrite -q -i 2 --window-size 100x30 "
    "--capture-env TERM,COLORTERM,LANG -c ./stage/asciiportal "
    "asciiverse/asciiportal.cast"])
time.sleep(2.5)
key("Enter", 1.0)                 # title
key("Enter", 2.0)                 # Begin: level 2
hold("a", 2.5)                    # over the boxes to the ladder
hold("w", 0.8)                    # up into the corridor
hold("d", 1.2)                    # to the door; the box is dropped
for _ in range(50):               # wait for it to land beside us
    row = next((l for l in screen().split("\n") if "Å" in l), "")
    if "♥" in row[:row.index("Å")] if "Å" in row else False: break
    time.sleep(0.2)
gap = row.index("Å") - row.rindex("♥", 0, row.index("Å"))
taps("a", gap + 1)                # turn, walk up and nudge it onto the switch
hold("d", 1.9); hold("w", 0.6)    # through the door, up the ladder
taps("d", 7, 0.2); hold("s", 0.5) # down into the portal room
taps("d", 9)                      # onto the door switch
key("a"); key("z", 0.8)           # portal behind
key("d"); key("x", 1.2)           # portal through the open door
hold("a", 1.2)                    # and through
time.sleep(2.5)
made_it = "Cool how you can see yourself" in screen()
key("Escape", 1.0)                # pause menu
key("5", 0.4); key("Enter", 1.2)  # exit to main menu
key("Enter", 1.0)                 # title
key("6", 0.4); key("Enter", 1.5)  # quit
subprocess.run(["tmux", "kill-session", "-t", s], stderr=subprocess.DEVNULL)
print("through the portal" if made_it else "did NOT make it through: run again")
sys.exit(0 if made_it else 1)
