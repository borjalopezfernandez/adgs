#!/bin/bash
set +e

[ "$DEBUG" == 'true' ] && set -x

rm -f /data/adgs/arc/tmp/.lock_minArcServer_*

echo "entrypoint adgs minarc / waiting 10s for db"
sleep 10


echo "minArcDB -c"
minArcDB -c

sleep 2

echo "minArcServer -s -H -D"
minArcServer -s -H -D

## Infinite loop tailing foo

echo "container entrypoint started adgs minarc"

touch /tmp/foo2.txt
tail -f /tmp/foo2.txt
