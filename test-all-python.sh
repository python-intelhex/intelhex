#!/bin/sh

TARGETS="3.5.10 3.6.12 3.7.9 3.8.1 3.9.0 pypy2.7-7.3.1 pypy3.5-7.0.0 pypy3.6-7.3.1"
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

