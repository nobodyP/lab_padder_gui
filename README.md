# lab_padder
A python tool to pad a specific amount of time at the beginning and end of an NNSVS style LAB file.

## How to use:
```
pip install -U click
python lab_padder.py -d {path_to_labs}
```

All args:
```
--time / amount of time IN LABEL UNITS to pad on each side (default: 5000000 aka 500 milliseconds)
--phoneme / phoneme to pad with (default: SP)
--lab_dir or -d / directory of labels to pad (REQUIRED)
--out or -o / directory to export to (default: out)
```
