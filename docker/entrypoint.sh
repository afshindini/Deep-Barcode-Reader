#!/bin/bash -l
set -e
if [ "$#" -eq 0 ]; then
  exec deep_barcode_reader --help
else
  exec "$@"
fi
