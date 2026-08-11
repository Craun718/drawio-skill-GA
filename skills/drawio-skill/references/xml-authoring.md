# Authoring .drawio XML

Read this **before hand-writing any `.drawio` XML** (workflow step 3). Skip it when a bundled generator writes the XML for you (`autolayout.py` + importers, `seqlayout.py`).


### File skeleton

```xml
<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="drawio" version="26.0.0">
  <diagram name="Page-1">
    <mxGraphModel>
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        <!-- user shapes start at id="2" -->
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

**Rules:**
- `id="0"` and `id="1"` are required root cells — never omit them
- User shapes start at `id="2"` and increment sequentially
- All shapes have `parent="1"` (unless inside a container — then use container's id)
- All text uses `html=1` in style for proper rendering
- **Never use `--` inside XML comments** — it's illegal per XML spec and causes parse errors
- Escape special characters in attribute values: `&amp;`, `&lt;`, `&gt;`, `&quot;`
- **Multi-line text in labels:** use `&#xa;` for line breaks inside `value` attributes (not literal `\n`). Example: `value="Line 1&#xa;Line 2"`

### Shape types (vertex)

| Style keyword | Use for |
|--------------|---------|
| `rounded=0` | plain rectangle (default) |
| `rounded=1` | rounded rectangle — services, modules |
| `ellipse;` | circles/ovals — start/end, databases |
| `rhombus;` | diamond — decision points |
| `shape=mxgraph.aws4.resourceIcon;` | AWS icons |
| `shape=cylinder3;` | cylinder — databases |
| `swimlane;` | group/container with title bar |

For **vendor/branded icons** (AWS/Azure/GCP/Cisco/Kubernetes) and any non-trivial shape, don't guess the `shape=mxgraph.*` name — a wrong name renders as a blank box. Run `python3 <this-skill-dir>/scripts/shapesearch.py "<keywords>"` to get the exact official style + size, or see `references/shapes.md` for the hand-writable cheatsheet. For **AI/LLM brand logos** (OpenAI, Claude, Gemini, …), which draw.io has none of, use `python3 <this-skill-dir>/scripts/aiicons.py "<brand>"`.

### Required properties

```xml
<!-- Rectangle / rounded box -->
<mxCell id="2" value="Label" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="160" height="60" as="geometry" />
</mxCell>

<!-- Cylinder (database) -->
<mxCell id="3" value="DB" style="shape=cylinder3;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;fontColor=#333333;" vertex="1" parent="1">
  <mxGeometry x="350" y="100" width="120" height="80" as="geometry" />
</mxCell>

<!-- Diamond (decision) -->
<mxCell id="4" value="Check?" style="rhombus;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;" vertex="1" parent="1">
  <mxGeometry x="100" y="220" width="160" height="80" as="geometry" />
</mxCell>
```

### Containers and groups

For architecture diagrams with nested elements, use draw.io's parent-child containment — do **not** just place shapes on top of larger shapes.

| Type | Style | When to use |
|------|-------|-------------|
| **Group** (invisible) | `group;pointerEvents=0;` | No visual border needed, container has no connections |
| **Swimlane** (titled) | `swimlane;startSize=30;` | Container needs a visible title bar, or container itself has connections |
| **Custom container** | Add `container=1;pointerEvents=0;` to any shape | Any shape acting as a container without its own connections |

**Key rules:**
- Add `pointerEvents=0;` to container styles that should not capture connections between children
- Children set `parent="containerId"` and use coordinates **relative to the container**

```xml
<!-- Swimlane container -->
<mxCell id="svc1" value="User Service" style="swimlane;startSize=30;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="1">
  <mxGeometry x="100" y="100" width="300" height="200" as="geometry"/>
</mxCell>
<!-- Child inside container — coordinates relative to parent -->
<mxCell id="api1" value="REST API" style="rounded=1;whiteSpace=wrap;html=1;" vertex="1" parent="svc1">
  <mxGeometry x="20" y="40" width="120" height="60" as="geometry"/>
</mxCell>
<mxCell id="db1" value="Database" style="shape=cylinder3;whiteSpace=wrap;html=1;" vertex="1" parent="svc1">
  <mxGeometry x="160" y="40" width="120" height="60" as="geometry"/>
</mxCell>
```

### Connector (edge)

**CRITICAL:** Every edge `mxCell` must contain a `<mxGeometry relative="1" as="geometry" />` child element. Self-closing edge cells (`<mxCell ... edge="1" ... />`) are **invalid** and will not render. Always use the expanded form.

```xml
<!-- Directed arrow — always include rounded, orthogonalLoop, jettySize for clean routing -->
<mxCell id="10" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;" edge="1" parent="1" source="2" target="3">
  <mxGeometry relative="1" as="geometry" />
</mxCell>

<!-- Arrow with label + explicit entry/exit points to control direction -->
<mxCell id="11" value="HTTP/REST" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;" edge="1" parent="1" source="2" target="4">
  <mxGeometry relative="1" as="geometry" />
</mxCell>

<!-- Arrow with waypoints — use when edge must route around other shapes -->
<mxCell id="12" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;" edge="1" parent="1" source="3" target="5">
  <mxGeometry relative="1" as="geometry">
    <Array as="points">
      <mxPoint x="500" y="50" />
    </Array>
  </mxGeometry>
</mxCell>
```

**Edge style rules:**
- **Animated connectors:** add `flowAnimation=1;` to any edge style to show a moving dot animation along the arrow. Works in SVG export and draw.io desktop — ideal for data-flow and pipeline diagrams. Example: `style="edgeStyle=orthogonalEdgeStyle;flowAnimation=1;rounded=1;..."`
- **Always** include `rounded=1;orthogonalLoop=1;jettySize=auto` — these enable smart routing that avoids overlaps
- Pin `exitX/exitY/entryX/entryY` on every edge when a node has 2+ connections — distributes lines across the shape perimeter. `scripts/edgeports.py <file>` does this for a whole diagram: it picks the side facing each peer and spreads that side's edges over even slots ordered by the far endpoint, so they don't stack or cross at the boundary. It skips ends you pinned by hand and is idempotent
- Add `<Array as="points">` waypoints when an edge must detour around an intermediate shape
- **Leave room for arrowheads:** the final straight segment between the last bend and the target shape must be ≥20px long. If too short, the arrowhead overlaps the bend and looks broken. Fix by increasing node spacing or adding explicit waypoints
- **libavoid obstacle-avoiding routing (editor-side, draw.io ≥ 30):** draw.io has a newer connector router that recomputes edge paths to run *around* shapes (fanning out parallel edges) without moving any node. It runs interactively in the draw.io desktop editor (or via jgraph's MCP app-server `routing:"libavoid"`) — it is **not** a headless CLI flag. Passing `--layout libavoid` opens a modal `Unknown layout:` error dialog and hangs the run; the CLI `--layout` values are ELK *node* layout presets, a different thing (see `mermaid-authoring.md`). For CLI-authored files keep the orthogonal rules above; if a dense diagram still has crossings after export, open the `.drawio` in draw.io desktop once and let libavoid re-route. Don't stack it on an ELK `--layout` pass — pick one router, not both.

### Distributing connections on a shape

When multiple edges connect to the same shape, assign different entry/exit points to prevent stacking:

| Position | exitX/entryX | exitY/entryY | Use when |
|----------|-------------|-------------|----------|
| Top center | 0.5 | 0 | connecting to node above |
| Top-left | 0.25 | 0 | 2nd connection from top |
| Top-right | 0.75 | 0 | 3rd connection from top |
| Right center | 1 | 0.5 | connecting to node on right |
| Bottom center | 0.5 | 1 | connecting to node below |
| Left center | 0 | 0.5 | connecting to node on left |

**Rule:** if a shape has N connections on one side, space them evenly (e.g., 3 connections on bottom → exitX = 0.25, 0.5, 0.75)

### Color palette (fillColor / strokeColor)

*Used only when no user style preset is active (see `references/style-presets.md` → "Applying a preset").*

**Color restraint:** use this table as a soft pastel pool. For any single diagram, choose at most three theme colors plus black/white/gray and reuse them across roles/tiers; tints/shades of the same theme count as one theme, so do not add a new hue per node type unless the user explicitly requests a different palette. The built-in exception is a **tiered semantic palette** for layered architecture: tints/shades of up to three theme colors may be distributed across labeled layers, with no legend required.

| Color name | fillColor | strokeColor | Use for |
|-----------|-----------|-------------|---------|
| Blue | `#dae8fc` | `#6c8ebf` | services, clients |
| Green | `#d5e8d4` | `#82b366` | success, databases |
| Yellow | `#fff2cc` | `#d6b656` | queues, decisions |
| Orange | `#ffe6cc` | `#d79b00` | gateways, APIs |
| Red/Pink | `#f8cecc` | `#b85450` | errors, alerts |
| Grey | `#f5f5f5` | `#666666` | external/neutral |
| Purple | `#e1d5e7` | `#9673a6` | security, auth |

### Capability Stack Architecture style

For layered architecture, prefer the compact **Capability Stack Architecture** style: larger bold text, white service blocks, thick unadorned layer edges, aggregate components, and a narrow vertical rail for external/coordination systems. This is a **tiered semantic palette**, so the layer headers carry the color meaning and no legend is needed.

- **Canvas:** keep the page compact; do not stretch every layer across the full page. Use a main stack around 900-1100px wide, a right rail around 95px wide when present, `x=30`, and page width/height sized to the content plus 40-70px margins.
- **Page title:** `text;html=1;align=center;verticalAlign=middle;fontSize=28;fontStyle=1;fontFamily=黑体;` at `x=30 y=10`, spanning the stack plus the rail when one is present.
- **Layer containers:** `swimlane;startSize=32;html=1;whiteSpace=wrap;fillColor=#dae8fc;strokeColor=#6c8ebf;fontFamily=黑体;fontSize=20;fontStyle=1;` (replace colors per tier).
- **Content blocks:** `rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#6c8ebf;fontFamily=仿宋_GB2312;fontSize=19;fontStyle=1;` (replace stroke per layer). Keep gaps and card dimensions on multiples of 10.
- **Aggregate component full-width:** when a layer has a summary, place one full-width rounded card at `x=20`, width = layer width - 40, height 45-55; put subordinate components below it.
- **Inter-layer edges:** `edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;exitX=0.5;exitY=0;exitDx=0;exitDy=0;entryX=0.5;entryY=1;entryDx=0;entryDy=0;strokeWidth=3;fontSize=18;fontStyle=1;labelBackgroundColor=#ffffff;` Keep these unadorned unless direction is semantically required.
- **Inside-layer edges:** use the same orthogonal base without `strokeWidth=3`; when several subordinate components connect to one aggregate component, spread their `exitX/entryX` values evenly so the lines do not stack.
- **External/coordination rail:** when there are 4+ external systems, use a narrow vertical swimlane (e.g. `width=95`, `startSize=120`) whose children are vertical cards (`width=60`, `height=250`, `textDirection=vertical-lr;direction=west;fontStyle=1;`). Connect it from the main layers with `entryX=0;entryY=0.5`.
- **Rail edge:** use classic bidirectional arrows when the rail has shared two-way coordination: `startArrow=classic;endArrow=classic;startFill=1;endFill=1`.
- **Typography pairing:** use `黑体` for titles/layer headers and `仿宋_GB2312` for body blocks in Chinese diagrams; keep the active preset font for non-Chinese labels.
- **Legend:** do not auto-add a legend for a **tiered semantic palette**; add one only when the user asks or when role colors are not already explained by visible labels.

All coordinates and sizes remain multiples of 10.

### Legend (optional)

Add a legend only when role colors are not self-explanatory or the user asks for one. Generate it mechanically from the roles actually present — never invent legend entries that aren't in the diagram:

```xml
<!-- Legend container: place in a corner clear of the diagram (e.g. below-left) -->
<mxCell id="legend" value="Legend" style="rounded=0;whiteSpace=wrap;html=1;fillColor=none;strokeColor=#666666;verticalAlign=top;fontStyle=1;" vertex="1" parent="1">
  <mxGeometry x="40" y="720" width="180" height="110" as="geometry"/>
</mxCell>
<!-- One swatch + label pair per used role, 24px row pitch, children of the legend -->
<mxCell id="leg1" value="" style="rounded=0;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" vertex="1" parent="legend">
  <mxGeometry x="10" y="30" width="30" height="16" as="geometry"/>
</mxCell>
<mxCell id="leg1t" value="Service" style="text;html=1;align=left;verticalAlign=middle;" vertex="1" parent="legend">
  <mxGeometry x="50" y="28" width="120" height="20" as="geometry"/>
</mxCell>
```

Rules: swatch colors come from the active palette (preset or the table above) with the **role name** as the label (Service, Database, Queue, …); height = `30 + 24 × rows`; the legend is a container (`parent="legend"`, relative coordinates). Skip it for single-color diagrams and for **tiered semantic palette** diagrams whose layer headers already explain each tint.

### Layout tips

**Spacing — scale with complexity:**

| Diagram complexity | Nodes | Horizontal gap | Vertical gap |
|-------------------|-------|----------------|--------------|
| Simple | ≤5 | 200px | 150px |
| Medium | 6–10 | 280px | 200px |
| Complex | >10 | 350px | 250px |

**Routing corridors:** between shape rows/columns, leave an extra ~80px empty corridor where edges can route without crossing shapes. Never place a shape in a gap that edges need to traverse.

**Grid alignment:** snap all `x`, `y`, `width`, `height` values to **multiples of 10** — this ensures shapes align cleanly on draw.io's default grid and makes manual editing easier.

**General rules:**
- Plan a grid before assigning x/y coordinates — sketch node positions on paper/mentally first
- Group related nodes in the same horizontal or vertical band
- Use `swimlane` cells for logical grouping with visible borders
- Place heavily-connected "hub" nodes centrally so edges radiate outward instead of crossing
- To force straight vertical connections, pin entry/exit points explicitly on edges:
  `exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0`
- Always center-align a child node under its parent (same center x) to avoid diagonal routing
- **Event bus pattern**: place Kafka/bus nodes in the **center of the service row**, not below — services on either side can reach it with short horizontal arrows (`exitX=1` left side, `exitX=0` right side), eliminating all line crossings
- Horizontal connections (`exitX=1` or `exitX=0`) never cross vertical nodes in the same row; use them for peer-to-peer and publish connections

**Avoiding edge-shape overlap:**
- Before finalizing coordinates, trace each edge path mentally — if it must cross an unrelated shape, either move the shape or add waypoints
- For tree/hierarchical layouts: assign nodes to layers (rows), connect only between adjacent layers to minimize crossings
- For star/hub layouts: place the hub center, satellites around it — edges stay short and radial
- When an edge must span multiple rows/columns, route it along the outer corridor, not through the middle of the diagram
