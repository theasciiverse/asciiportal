#!/bin/sh
# Lays out the av archive in stage/: the start script at the top, and the
# game in lib/ with its map packs (ASCIIpOrtal looks for maps/ next to its
# binary). The music in media/ and maps/ is left out: no sound here.
set -eu
rm -rf stage && mkdir -p stage/lib
cp asciiverse/asciiportal stage/asciiportal
cp asciiportal stage/lib/asciiportal
cp -R maps stage/lib/maps
find stage/lib/maps -name '*.ogg' -delete
cp LICENSE README.md PATCHES.md stage/
