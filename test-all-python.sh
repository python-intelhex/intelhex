#!/bin/sh

TARGETS="3.8 3.9 3.10 3.11 3.12 3.13"
DIR=$(dirname "$(readlink -f "$0")")

_pyenv=$(command -v pyenv)
[ -z "$_pyenv" ] && { echo "pyenv is missing on your system."; exit 1; }

_tox=$(command -v tox)
[ -z "$_tox" ] && { echo "tox is missing on your system."; exit 1; }

cd "$DIR"

echo "Installing (if needed) Python versions: $TARGETS"
for version in $TARGETS ; do
	$_pyenv install --skip-existing $version
done

echo "Enabling Python versions from pyenv..."
$_pyenv local $TARGETS

echo "Running tox..."
$_tox

