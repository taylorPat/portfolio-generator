# Portfolio Setup Plan (Python + Jinja2 + GitHub Pages)

## Goal

Build a simple, extensible portfolio website:

- Data-driven (YAML)
- Generated via Python (Jinja2)
- Hosted as static site (GitHub Pages)

---

## 1. Project Setup

### Install dependencies

```bash
uv add jinja2 pyyaml
```

### Project structure

```
/portfolio
  /data
    profile.yml
  /templates
    base.html
    index.html
  /static
    style.css
  build.py
  /output
```

---

## 2. Data Layer (YAML)

Create `data/profile.yml`:

- Personal info
- Contact links
- Skills
- Projects

All content should live here (no hardcoding in HTML).

---

## 3. Python Generator

Create `build.py`:

- Load YAML
- Load Jinja templates
- Render HTML
- Output to `/output/index.html`

### Run

```bash
python build.py
```

---

## 4. Templates (Jinja2)

- `base.html` → layout (HTML skeleton)
- `index.html` → content

Render:

- Name / title
- About section
- Skills list
- Projects list

---

## 5. First Working Version

- Generate HTML
- Open `output/index.html` in browser
- Verify everything renders correctly

---

## 6. GitHub Pages Deployment

### Option A

- Move output to `/docs`
- Enable GitHub Pages

### Option B

- Use GitHub Actions to build + deploy

---

## 7. Styling (Basic → Advanced)

### Start simple

- Clean layout
- Readable typography

### Then improve

- Project cards
- Hover effects
- Responsive design
- Optional: dark mode

---

## 8. Extensibility

- Add new YAML fields easily
- Split templates into components
- Support multiple pages later

---

## Result

- Fully static portfolio
- Easy to maintain (edit YAML only)
- Fast + free hosting
- Scalable for future features
