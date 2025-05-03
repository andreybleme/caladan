#!/bin/bash
PID=$1
INTERVAL=15      # seconds between samples
DURATION=600     # total duration in seconds
OUTFILE=top.log

echo "Logging CPU/MEM for PID $PID every $INTERVAL to $OUTFILE"
echo "Time,  %CPU,  %MEM" > $OUTFILE

# Run top in batch mode, but filter only our PID
top -b -d $INTERVAL -p $PID \
  | awk -v d="$INTERVAL" '
      /^%Cpu/ { next } 
      /^ *PID/ { next } 
      $1 == "'"$PID"'" {
        # $9=%CPU, $10=%MEM in default top output
        printf "%s, %5s, %5s\n", strftime("%Y-%m-%dT%H:%M:%S"), $9, $10
      }
    ' >> $OUTFILE &
TOP_PID=$!

sleep $DURATION
kill $TOP_PID
echo "Done."

# ======= res
# 34275 is always 100% CPU (IOKernel)
# 34339 the synthetic server