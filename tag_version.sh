#!/bin/sh

version=$(grep __version__ payments/__init__.py|cut -d"'" -f 2)
if [ "x${version#*-}" = "x$version" ]; then
    git tag -a v$version -m "Release $version"
else
    git tag -a v$version -m "Pre-release $version"
fi
echo "Remember to push tags: git push --tags"
