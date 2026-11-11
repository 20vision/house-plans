#!/usr/bin/env python3
"""Builds the open house-plan dataset repo from the site's own library (floorplan_archi/public/house-plans/*/page.json)
and the public files on storage.googleapis.com/20img/house-plans/<slug>/. Idempotent: skips files that exist.
Each plan folder: plan-level*.dxf, building.json, area-schedule.csv, thumb.jpg, README.md. Root: README.md, index.csv."""
import csv, json, os, glob, shutil, time, urllib.request
LIB = os.path.expanduser('~/projects/floorplan_archi/public/house-plans'); BASE = 'https://storage.googleapis.com/20img/house-plans/'
SITE = 'https://floorplan.ai-architectures.com/house-plans/'; TAG = '?utm_source=github-plans&utm_medium=probe&utm_campaign=github'
ROOT = os.path.dirname(os.path.abspath(__file__)); M2 = 10.7639
def fetch(url, path):
    if os.path.exists(path) and os.path.getsize(path) > 0: return True
    try:
        data = urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'}), timeout=40).read()
        open(path, 'wb').write(data); time.sleep(0.1); return True
    except Exception as e:
        return False
import re
def units(path):
    try: m = re.search(r'\$INSUNITS\s*\n\s*70\s*\n\s*(\d+)', open(path, errors='ignore').read(200000))
    except Exception: m = None
    return {'1': 'inches', '2': 'feet', '4': 'millimetres', '5': 'centimetres', '6': 'metres'}.get(m.group(1) if m else '', 'not stated in the file')
rows, miss = [], 0
for f in sorted(glob.glob(LIB + '/*/page.json'), reverse=bool(os.environ.get('REVERSE'))):
    d = json.load(open(f)); s = d['slug']; out = f'{ROOT}/plans/{s}'; os.makedirs(out, exist_ok=True)
    assets = d.get('assets') or []
    want = [a for a in assets if (a.endswith('.dxf') and not a.endswith('-m.dxf')) or a in ('building.json', 'area-schedule.csv')]
    for a in want:
        if not fetch(BASE + s + '/' + a, f'{out}/{a}'): miss += 1
    th = os.path.dirname(f) + '/thumb.jpg'
    if os.path.exists(th) and not os.path.exists(out + '/thumb.jpg'): shutil.copy(th, out + '/thumb.jpg')
    p = d.get('plan') or {}; rooms = [r for r in (p.get('rooms') or [])]
    indoor = [r for r in rooms if not r.get('outdoor')]
    area = sum((r.get('cell') or {}).get('w', 0) * (r.get('cell') or {}).get('h', 0) for r in indoor)
    copy = d.get('copy') or {}; issues = d.get('issues') or []
    L = [f"# {copy.get('title') or s}", '', (d.get('summary') or '').strip(), '',
         f"![Floor plan preview](thumb.jpg)" if os.path.exists(out + '/thumb.jpg') else '', '',
         '| | |', '|---|---|', f"| Levels | {p.get('levels')} |", f"| Footprint | {round(p.get('width') or 0, 2)} m × {round(p.get('depth') or 0, 2)} m ({(p.get('width') or 0) * 3.28084:.0f} ft × {(p.get('depth') or 0) * 3.28084:.0f} ft) |",
         f"| Rooms | {len(indoor)} indoor, {len(rooms) - len(indoor)} outdoor |", f"| Indoor area including garage, from the room grid | about {area:.0f} m² ({area * M2:,.0f} sq ft) |", '',
         '## Files here', ''] + [f"- `{a}`" + (f' (floor plan, DXF, drawing units: {units(out + "/" + a)})' if a.endswith('.dxf') else ' (rooms, walls, openings as data)' if a == 'building.json' else ' (room schedule)') for a in sorted(want)] + ['',
         '## More for this plan', '', f"- Plan page with the PDF plan set, IFC and 3D model, and a tool to change the plan: {SITE}{s}{TAG}",
         f"- PDF plan set: {BASE}{s}/plan-set.pdf", f"- IFC model: {BASE}{s}/model.ifc", '',
         '## Known issues in this drawing', ''] + ([f"- {i.get('message')}" for i in issues] if issues else ['- None found by the automatic checks.']) + ['',
         'Concept design generated with AI. Not for construction or permit; verify with a licensed professional.', '']
    open(out + '/README.md', 'w').write('\n'.join(L))
    rows.append(dict(slug=s, title=copy.get('title') or '', search_phrase=d.get('keyword') or '', levels=p.get('levels'), width_m=round(p.get('width') or 0, 2), depth_m=round(p.get('depth') or 0, 2), rooms_indoor=len(indoor),
                     indoor_area_m2_incl_garage=round(area), indoor_area_sqft_incl_garage=round(area * M2), tags=' '.join(d.get('tags') or []), dxf_units=units(out + '/plan-level1.dxf'), known_issues=len(issues), issue_codes=' '.join(sorted({i.get('code') for i in issues})), page=SITE + s + TAG))
with open(ROOT + '/index.csv', 'w', newline='') as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
import collections
n = len(rows); clean = sum(1 for r in rows if not r['known_issues']); un = collections.Counter(r['dxf_units'] for r in rows); one = sum(1 for r in rows if r['levels'] == 1)
ar = sorted(r['indoor_area_sqft_incl_garage'] for r in rows)
stat = f"""
## The collection in numbers

- {n} plans; {one} on one level, {n - one} on two or more.
- Indoor area including garages from about {ar[0]:,} to {ar[-1]:,} sq ft; the middle plan has {ar[n // 2]:,} sq ft.
- Drawing units of the DXF files: {', '.join(f'{v} in {k}' for k, v in un.most_common())}.
- {clean} plans have no issue found by the automatic checks; {n - clean} have at least one, listed in their README.
"""
open(ROOT + '/README.md', 'w').write(open(ROOT + '/_templates/head.md').read() + stat + open(ROOT + '/_templates/tail.md').read())
print('plans', len(rows), 'missing files', miss, 'no known issues', sum(1 for r in rows if not r['known_issues']))
