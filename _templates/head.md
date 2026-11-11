# Open house plans: 503 concept floor plans as DXF, JSON and CSV

503 house plans, from 300 sq ft backyard units to large two-story homes: ranch, farmhouse, barndominium, cabin, craftsman, ADU, duplex and more. Each plan folder in [`plans/`](plans) holds

| File | What it is |
|---|---|
| `plan-level1.dxf` (one per level) | The floor plan as a drawing. Opens in AutoCAD, BricsCAD, LibreCAD, QCAD and other CAD programs. |
| `building.json` | The same plan as data: the room program with an adjacency list, then rooms, walls, doors, windows and fixtures with coordinates in metres. |
| `area-schedule.csv` | Room schedule with sizes and areas. |
| `thumb.jpg` | Preview picture. |
| `README.md` | Summary, footprint, known issues, and links to the PDF plan set, the IFC model and the plan's page. |

[`index.csv`](index.csv) lists every plan with levels, footprint, area, tags, drawing units and the number of known issues, so you can filter before you download.

## What these plans are, and what they are not

- They come from the plan engine behind [AI Architectures](https://floorplan.ai-architectures.com/house-plans?utm_source=github-plans&utm_medium=probe&utm_campaign=github) (20Vision GmbH, Vienna). Each layout was generated with AI from a written brief and drawn by our own drafting code.
- They are concept designs. They are not construction or permit documents. Have a licensed architect or engineer check anything you intend to build.
- Our automatic checks found issues in many of them, such as a narrow room, an area that differs from the brief or a missing door. Each plan's README lists its issues, and `index.csv` counts them.
