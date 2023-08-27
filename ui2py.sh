#!/bin/bash

# Loop through all .ui files in the current directory
for ui_file in *.ui; do
  # Extract the filename without the extension
  filename=$(basename -- "$ui_file")
  filename_noext="${filename%.*}"
  
  # Convert .ui to .py using pyuic5
  pyuic5 -x "$ui_file" -o "${filename_noext}.py"
  
  echo "Converted $ui_file to ${filename_noext}.py"
done

echo "Conversion complete."
