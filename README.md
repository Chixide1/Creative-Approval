# Creative Approval Service

## Running the project

### How to run in Docker

- Once you have cloned the repo to your desktop, build the Docker image:

  ```bash
  docker build -t creative-approval .
  ```
- Run the Docker container:

  ```bash
  docker run -p 8000:8000 creative-approval
  ```
- Navigate to [http://localhost:8000/docs](http://localhost:8000/docs) in your browser to test the endpoints via Swagger UI.

### How to run locally with UV
- Install dependencies and start the FastAPI server: `uv run fastapi dev src/main.py`
- The API will be available at [http://localhost:8000/docs](http://localhost:8000/docs).

### How to run locally with pip

- Create and activate a virtual environment:

  ```bash
  python3 -m venv venv
  source venv/bin/activate   # On Windows: venv\Scripts\activate.bat
  ```
- Install dependencies:

  ```bash
  pip install .
  ```
- Start the FastAPI server:

  ```bash
  fastapi dev src/main.py
  ```
- Visit [http://localhost:8000/docs](http://localhost:8000/docs).

### How to test
- Run the tests using UV:

  ```bash
  uv run pytest -s
  ```
- Or with pip (inside the virtual environment):

  ```bash
  pytest -s
  ```

## Rules & Justifications

### Contrast / Legibility Check

- **What it does:** Flags creatives with insufficient visual contrast, measured by standard deviation.
- **Why it matters:** Global Outdoor Guidelines: Require clarity and legibility for all outdoor placements.
- **Outcome:** Ensures text and key visuals remain clear to the public.

### Skin Content Check

- **What it does:** Flags creatives with a high proportion of skin-tone pixels.
- **Why it matters:** CAP Code, Section 4 (Harm and Offense): marketing must avoid sexualization or indecent depictions.Global Outdoor Guidelines: prohibit nudity or overtly sexual imagery.
- **Outcome:** Safeguards against inappropriate or offensive outdoor advertising.

### Blood / Red Content Check

- **What it does:** Flags creatives with an unusually high proportion of red pixels, used as a proxy for blood or gore.
- **Why it matters:** CAP Code, Section 4.4 (Harm and Offense): marketing must not condone or encourage violence. Global Outdoor Guidelines: explicitly prohibit depictions of violence or excessive blood.
- **Outcome:** Prevents shocking or graphic imagery from being displayed outdoors.

### Metadata Check

- **What it does:** Scans metadata string for keywords linked to prohibited categories.
- **Why it matters:** Global Outdoor Guidelines: ban categories including nudity, sexual imagery, violence, drugs, excessive blood, gambling, tobacco, weapons, extremist content, profanity, and culturally offensive symbols.
- **Outcome:** Ensures creatives are  content-compliant with outdoor advertising standards.

## Design Decisions & Trade-offs

### Skin & Blood Content Check

I used Pillow to apply color masks that approximate how much of an image falls within predefined ranges for skin tones and red hues. This helps detect creatives that may depict excessive nudity or graphic blood, which are not acceptable for outdoor placements.

Because color alone is not always reliable (for example, red objects that are not blood), flagged images are returned as REQUIRES\_REVIEW rather than rejected outright. In production, I would replace this heuristic with a trained model capable of distinguishing skin and blood more accurately.

### Metadata Keyword Check

Instead of using a static list of banned keywords, a production system would use a text classifier to identify references to prohibited categories.

### Contrast & Legibility Check

Clear contrast is essential for OOH advertising to remain legible from distance. I implemented a simple contrast ratio check as a proxy. This can be tuned depending on the medium (for example, roadside billboards vs. smaller digital screens).

### Rule Structure

All checks are implemented as `ValidationRule` objects. This makes the system:

- Extensible - new rules can be added easily
- Consistent – each rule returns a clear status: APPROVED, REJECTED, or REQUIRES\_REVIEW, with reasons attached

---

### Trade-offs

- Heuristics vs. Models: For speed and simplicity, I used heuristics (color ranges, basic keyword search). In production, I would adopt lightweight ML models for higher accuracy.
- False Positives: Color-based checks may flag safe images. To avoid unfair rejections, I defaulted to REQUIRES\_REVIEW rather than outright rejection.