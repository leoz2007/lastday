"""Rendu d'une capsule : python3 video/render.py 02 [--preview 1.0 12.5 ...] [--md]"""
import importlib
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import engine  # noqa: E402

def main():
    num = sys.argv[1].zfill(2)
    cap = importlib.import_module(f'capsules.capsule{num}')
    engine.write_script_md(cap)
    if '--md' in sys.argv:
        full = ' '.join(s['text'].strip() for s in cap.SCENES)
        print(len(full.split()), 'mots')
        for i, s in enumerate(cap.SCENES):
            print(i + 1, len(s['text'].split()))
        return
    if '--preview' in sys.argv:
        ts = [float(x) for x in sys.argv[sys.argv.index('--preview') + 1:]]
        engine.render(cap, only_frames=ts)
    else:
        engine.render(cap)

if __name__ == '__main__':
    main()
