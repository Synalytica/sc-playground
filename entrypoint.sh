#!/bin/bash
# coding: utf-8
# brief: Run tests and aggregate logs


OUTPUT_DIR=/app/results

if [ $# -eq 0 ]; then
    # test all
    ls contracts | cut -d. -f1 | xargs -I@ smartpy test contracts/@.py $OUTPUT_DIR/@ --html
else
    # run specific
    smartpy $@
fi

echo "Tests have run and saved @ $OUTPUT_DIR!"

# generate homepage
find $OUTPUT_DIR -name log.html | cut -d\/ -f4,5 | xargs -I@ printf '<a
href="%s/log">%s</a><br>' @ @ > $OUTPUT_DIR/index.html

# serve file explorer
serve -p $PORT -d $OUTPUT_DIR

