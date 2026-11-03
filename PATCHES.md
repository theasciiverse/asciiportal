# Asciiverse patches

ASCIIpOrtal by Joe Larson (Cymon's Games), from
[cymonsgames/ASCIIpOrtal](https://github.com/cymonsgames/ASCIIpOrtal) at
`master` (v1.3-beta8 plus later fixes), packaged for the Asciiverse in
its terminal version: plain ncurses, no SDL window, no sound.

The changes are small and meant to be offered upstream. Everything else
is upstream's, including all the levels and map packs.

## Fixes

- **Crash at startup with current compilers.**
  `MapPack::set_currentlevel` and `play_level` could reach the end
  without returning a value. Recent GCC compiles that into a jump into
  nowhere, and the game crashed before the title screen. Both now
  return 0 there. (`src/ap_maps.cpp`, `src/ap_play.cpp`)

- **Keyboard in the terminal version.** Upstream's own notes say the
  input of the no-SDL build "really sucks". It read one key per game
  beat and threw away the rest, so a quick tap between two beats was
  lost. A held key also stalled for the terminal's autorepeat delay
  before it walked, because a terminal never says when a key goes up.
  (`src/ap_input.cpp`, `src/ap_input.h`, `src/ap_draw.cpp`)
  - In terminals that speak the
    [kitty keyboard protocol](https://sw.kovidgoyal.net/kitty/keyboard-protocol/)
    (kitty, foot, WezTerm, Ghostty, Alacritty, iTerm2 and others), the
    game asks for key press and release events. A held key then repeats
    every beat until it is released, exactly as in the SDL version.
  - Elsewhere, keys are queued instead of dropped, and a run of
    autorepeat counts as one step per beat.
  - Esc (pause menu) responds after 25 ms instead of one second.
  - The level-complete screen now reads keys through the same code.

- **Terminal version builds without SDL installed.** `src/main.cpp`
  included `SDL/SDL.h` even with `__NOSDL__`, though it uses nothing from
  it then; the include is now skipped in the terminal version, as every
  other source file already does. (`src/main.cpp`)

## Packaging

- Built from `asciiverse/build.sh` rather than upstream's Makefiles. It
  compiles the same sources as C++17 (Apple's compiler would otherwise
  use C++98, too old for yaml-cpp) with `-D__NOSDL__ -D__NOSOUND__` and links
  yaml-cpp 0.8.0, built from source, statically.
- The av archive holds a start script, the binary in `lib/` and the map
  packs in `lib/maps/`. The music files are left out, since this build
  has no sound.
- Saves and custom map packs stay where upstream puts them:
  `~/.asciiportal`.

## Licences

Upstream's LICENSE is the GPL, version 3; the source files carry Joe
Larson's MIT-style notice. Map packs carry their own terms, e.g. Zugz's
packs (`evil`, `Mechanist`) are CC BY-SA 2.0 (see their COPYING files).
