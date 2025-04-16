Python scripts to generate graphs from the Experiments section.

1. Create venv
```
python3 -m venv .venv
```

2. Activate venv
```
source .venv/bin/activate
``` 

3. Install dependencies using pip
```
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```

4. Generate image
```
python3 generate.py
```