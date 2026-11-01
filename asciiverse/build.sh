#!/bin/sh
# Builds the terminal version of ASCIIpOrtal (no SDL, no sound) as
# ./asciiportal. Linux: run inside alpine:3.22 for a fully static binary;
# macOS: run on the runner with CC_ARCH set to x86_64 or arm64, linking the
# system's ncurses. Other Linux (local testing) links ncursesw shared.
#   docker run --rm -v "$PWD":/src -w /src alpine:3.22 sh asciiverse/build.sh
# yaml-cpp is built from source into build/ and linked statically, so the
# binary needs nothing but (on macOS and local builds) ncurses. With
# YAML_CPP_SYSTEM=1 the installed yaml-cpp is used instead.
# Upstream's Makefiles want a system yaml-cpp and a PORT dance; the source
# list below is their OBJECTS_NOSOUND.
set -eu
YAML_CPP=0.8.0
AP_VERSION=1.3-beta8

if [ -f /etc/alpine-release ]; then
  apk add --no-cache build-base cmake git ncurses-dev ncurses-static >/dev/null
  curses="-static -lncursesw"
  cursesinc=""
elif [ "$(uname)" = Darwin ]; then
  curses="-lncurses"
  cursesinc=""
else
  curses="-lncursesw"
  cursesinc="-I/usr/include/ncursesw"
fi
cxx="c++${CC_ARCH:+ -arch $CC_ARCH}"

if [ "${YAML_CPP_SYSTEM:-}" = 1 ]; then
  yamlinc=""
  yamllib="-lyaml-cpp"
else
  mkdir -p build
  if [ ! -d build/yaml-cpp ]; then
    git clone -q --depth 1 -b "$YAML_CPP" https://github.com/jbeder/yaml-cpp build/yaml-cpp
  fi
  cmake -S build/yaml-cpp -B build/yaml-cpp-build -DCMAKE_BUILD_TYPE=Release \
    -DYAML_CPP_BUILD_TESTS=OFF -DYAML_CPP_BUILD_TOOLS=OFF \
    -DYAML_CPP_BUILD_CONTRIB=OFF -DYAML_BUILD_SHARED_LIBS=OFF \
    -DCMAKE_POLICY_VERSION_MINIMUM=3.5 \
    ${CC_ARCH:+-DCMAKE_OSX_ARCHITECTURES=$CC_ARCH} >/dev/null
  cmake --build build/yaml-cpp-build -j 4 >/dev/null
  yamlinc="-Ibuild/yaml-cpp/include"
  yamllib="build/yaml-cpp-build/libyaml-cpp.a"
fi

rm -f asciiportal
# shellcheck disable=SC2086
$cxx -O2 -DAP_VERSION="\"$AP_VERSION\"" -D__NOSDL__ -D__NOSOUND__ \
  -D_XOPEN_SOURCE_EXTENDED $yamlinc $cursesinc \
  src/ap_pager.cpp src/ap_object.cpp src/ap_maps.cpp src/ap_filemgr.cpp \
  src/ap_input.cpp src/ap_draw.cpp src/ap_play.cpp src/main.cpp src/menu.cpp \
  $yamllib $curses -o asciiportal
strip asciiportal
