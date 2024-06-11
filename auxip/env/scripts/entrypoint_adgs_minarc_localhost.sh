#!/bin/bash
set +e

[ "$DEBUG" == 'true' ] && set -x


echo "entrypoint adgs minarc / waiting 10s for db"
sleep 10

echo "minArcDB -c"
minArcDB -c

echo "minArcServer -s"
minArcServer -s

## Infinite loop tailing foo

echo "container entrypoint started adgs minarc"

touch /tmp/foo2.txt
tail -f /tmp/foo2.txt
