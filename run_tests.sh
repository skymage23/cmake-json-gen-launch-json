#!/bin/sh

function die(){ 
    echo "$1" 1>&2
    exit 1
}

if ! which python3 2>&1 >/dev/null; then
    die "Python3 is either not instaled or it is not on your system PATH."
fi

if ! which cmake 2>&1 >/dev/null; then
    die "CMake is either not installed or it is not on your system PATH."
fi

echo "Running Python tests:"

if ! python3 tests/python_tests/main.py; then
    die "Python tests failed."
fi

echo "Running CMake tests"

if ! cmake -P tests/run_tests.cmake; then
    die "CMake tests failed."
fi

exit 0