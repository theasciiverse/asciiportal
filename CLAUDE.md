# ASCIIpOrtal (Asciiverse packaging)

ASCIIpOrtal by Joe Larson (Cymon's Games), a 2D Portal fan game,
packaged for the Asciiverse catalog as its terminal build (no SDL, no
sound). Not our code: keep changes small, list every one in PATCHES.md,
and prefer patches upstream could take.

- Branch `asciiverse` on upstream `master` (v1.3-beta8 + 12 commits);
  `upstream` is github.com/cymonsgames/ASCIIpOrtal (quiet since 2019).
- Build: `sh asciiverse/build.sh` (clones and builds yaml-cpp 0.8.0
  into build/; `YAML_CPP_SYSTEM=1` uses libyaml-cpp-dev instead), then
  `sh asciiverse/stage.sh`; run `stage/asciiportal`.
- The game chdirs to its binary's folder and reads `maps/` there (or
  /usr/share/asciiportal if that exists); saves go to ~/.asciiportal.
- Terminal input lives in `src/ap_input.cpp` (`#ifdef __NOSDL__`): kitty
  keyboard protocol when the terminal answers `CSI ? u`, otherwise a key
  queue. tmux doesn't speak the protocol, so tmux tests the fallback; the
  kitty path was tested with a pty that answers like kitty.
- Preview: `python3 asciiverse/record-preview.py` (tmux, asciinema 3):
  fixed moves through level 2; it says whether the take made it through.
- Name: "ASCIIpOrtal", upstream's; it is a fan game with its own levels.
