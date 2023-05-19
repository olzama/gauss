import sys
from pathlib import Path

corpus = Path(sys.argv[1])
for name in corpus.glob('**/**/**/*.txt'):
    if str(name).startswith("annotator"):
        print(name)