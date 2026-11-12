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

## The collection in numbers

- 503 plans; 346 on one level, 157 on two or more.
- Indoor area including garages from about 310 to 4,821 sq ft; the middle plan has 1,875 sq ft.
- Drawing units of the DXF files: 375 in inches, 128 in millimetres.
- 96 plans have no issue found by the automatic checks; 407 have at least one, listed in their README.

## Use

The files are free to download and to use for ideas, study and research, the same terms as on the site. If you share a plan or publish work that uses these files, please link to the plan's page or to this repository. For anything else, write to us through the [support page](https://floorplan.ai-architectures.com/support).

## Also published on

- Kaggle: https://www.kaggle.com/datasets/aiarchitectures/house-plans-dxf-json-csv

## Change a plan

Every plan's page has a tool that changes rooms, style or layout and exports the drawing again. The link is in each plan's README.

## How this repository is made

`build.py` reads the library of the site, copies the public files and writes every README and `index.csv`. The two text blocks of this page are in `_templates/`.

## Related

- [Gallery of all plans](https://20vision.github.io/house-plans/): name, area, bedrooms, one link per plan
- [AI Architectures page for this project](https://floorplan.ai-architectures.com/house-plans?utm_source=github&utm_medium=probe&utm_campaign=house-plans)
- [ai-architectures-desktop](https://github.com/20vision/ai-architectures-desktop): AI Architectures desktop app
- [skills](https://github.com/20vision/skills): agent skills: house plans, floor plan CAD, WCAG audit
