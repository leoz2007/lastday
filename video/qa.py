"""Contrôles d'une capsule livrée : python3 video/qa.py 02
- ffprobe : 1080x1920, 30 fps, pistes vidéo+audio, durée vidéo ≈ audio + 1,5 s
- extrait 5 images du MP4 final (planche contact build/capsuleNN/qa_sheet.png)
- vérifie un pixel Red Poppy (attendu ≈ 248,72,94) et affiche le sous-titre attendu"""
import glob, json, os, subprocess, sys
import numpy as np
import skia

ROOT = os.path.dirname(os.path.abspath(__file__))
num = sys.argv[1].zfill(2)
mp4 = glob.glob(os.path.join(ROOT, '..', 'out', f'capsule{num}_*.mp4'))[0]
tmp = os.path.join(ROOT, 'build', f'capsule{num}')
tim = json.load(open(os.path.join(tmp, 'timing.json')))
pr = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-show_streams', '-show_format',
                                         '-of', 'json', mp4]))
v = [s for s in pr['streams'] if s['codec_type'] == 'video'][0]
a = [s for s in pr['streams'] if s['codec_type'] == 'audio']
dur = float(pr['format']['duration'])
ok = True
def chk(cond, msg):
    global ok
    print(('OK   ' if cond else 'FAIL ') + msg)
    ok &= bool(cond)
chk(v['width'] == 1080 and v['height'] == 1920, f"taille {v['width']}x{v['height']}")
chk(v['r_frame_rate'] == '30/1', f"fps {v['r_frame_rate']}")
chk(v['codec_name'] == 'h264' and v['pix_fmt'] == 'yuv420p', f"{v['codec_name']} {v['pix_fmt']}")
chk(len(a) == 1 and a[0]['codec_name'] == 'aac', f"audio {a[0]['codec_name'] if a else None} {a[0].get('bit_rate') if a else ''}")
d_audio = tim['audio']
chk(abs(dur - (d_audio + 1.5)) < 0.2, f"durée vidéo {dur:.2f}s / voix {d_audio:.2f}s (écart {dur - d_audio:.2f}s)")
moov = open(mp4, 'rb').read(200000).find(b'moov')
mdat = open(mp4, 'rb').read(200000).find(b'mdat')
chk(0 <= moov < (mdat if mdat >= 0 else 10**9), 'faststart (moov avant mdat)')
# 5 instants : milieu de 5 scènes, dont ouverture, contenu et fin
sc = tim['scenes']
picks = [0, 2, 3, 5, 6]
times = []
for i in picks:
    t0, t1 = sc[i]
    times.append(round(t0 + (t1 - t0) * 0.72, 2))
imgs = []
for t in times:
    out = os.path.join(tmp, f'qa_{t:06.2f}.png')
    subprocess.check_call(['ffmpeg', '-y', '-loglevel', 'error', '-ss', str(t), '-i', mp4,
                           '-frames:v', '1', out])
    imgs.append(out)
    sub = next((s[2] for s in tim['subs'] if s[0] <= t < s[1]), '—')
    print(f'  t={t:6.2f}s  sous-titre attendu : {sub}')
# pixel rouge : segment de progression actif sur une scène de contenu (x=80,y=77)
arr = skia.Image.open(imgs[1]).toarray(colorType=skia.kRGBA_8888_ColorType)
px = arr[77, 80][:3]
chk(np.abs(px.astype(int) - [248, 72, 94]).max() <= 10, f'pixel rouge {tuple(int(x) for x in px)} (attendu 248,72,94)')
arr = skia.Image.open(imgs[-1]).toarray(colorType=skia.kRGBA_8888_ColorType)
px = arr[1000, 30][:3]
chk(np.abs(px.astype(int) - [248, 72, 94]).max() <= 10, f'fond scène finale {tuple(int(x) for x in px)}')
s = skia.Surface(432 * 5, 768)
c = s.getCanvas()
for i, f in enumerate(imgs):
    c.drawImageRect(skia.Image.open(f), skia.Rect.MakeXYWH(i * 432, 0, 432, 768))
s.makeImageSnapshot().save(os.path.join(tmp, 'qa_sheet.png'))
print('planche :', os.path.join(tmp, 'qa_sheet.png'))
print('RÉSULTAT :', 'OK' if ok else 'ÉCHEC')
