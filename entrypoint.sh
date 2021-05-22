#!/bin/bash
# coding: utf-8
# brief: Run tests and aggregate logs


# test all
if [ $# -eq 0 ]; then
    ls contracts | cut -d. -f1 | xargs -I@ smartpy test contracts/@.py $OUTPUT_DIR/@ --html
else
    smartpy "$@"
fi

echo "Tests have run and saved @ $OUTPUT_DIR!"
ls $OUTPUT_DIR

