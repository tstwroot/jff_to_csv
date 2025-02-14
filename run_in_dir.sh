#!/bin/bash

if [ $# -ne 2 ]
then
  echo "Invalid Arguments."
  exit -1
fi

INPUT_DIR=$1
OUTPUT_DIR=$2

if [ ! -d "$OUTPUT_DIR" ]
then
  echo "Creating the output directory in: $OUTPUT_DIR"
  mkdir "$OUTPUT_DIR"
fi

for CURRENT_FILE in "$INPUT_DIR"/*
do
  python3 jff_to_csv.py $INPUT_DIR/$(basename $CURRENT_FILE) $OUTPUT_DIR/$(basename "$CURRENT_FILE" | sed 's/\.[^.]*$//').csv
done
