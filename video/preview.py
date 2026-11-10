"""Planche d'aperçu sans voix (alignement factice) : python3 video/preview.py 03 [fraction]"""
import importlib, json, os, sys
os.environ['FAKE_TTS'] = os.environ.get('FAKE_TTS', '1')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import engine, skia  # noqa
num = sys.argv[1].zfill(2)
fr = float(sys.argv[2]) if len(sys.argv) > 2 else 0.97
cap = importlib.import_module(f'capsules.capsule{num}')
engine.render(cap, only_frames=[0.1])
tmp = os.path.join(engine.ROOT, 'build', f'capsule{num}')
sc = json.load(open(os.path.join(tmp, 'timing.json')))['scenes']
ts = [round(a + (b - a) * fr, 2) for a, b in sc]
engine.render(cap, only_frames=ts)
s = skia.Surface(432 * 7, 768); c = s.getCanvas()
for i, t in enumerate(ts):
    c.drawImageRect(skia.Image.open(os.path.join(tmp, f'preview_{t:06.2f}.png')), skia.Rect.MakeXYWH(i * 432, 0, 432, 768))
s.makeImageSnapshot().save(os.path.join(tmp, 'preview_sheet.png'))
print(os.path.join(tmp, 'preview_sheet.png'))
