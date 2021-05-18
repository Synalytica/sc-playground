#!/bin/bash

if (($# == 0)); then
    for file in $(find contracts/ -type f); do
        /root/smartpy-cli/SmartPy.sh test $file .testResult
    done
else
    /root/smartpy-cli/SmartPy.sh test $1 .testResult
fi

rm -rf .testResult