# Creative Approval Service

## How to run locally

- Once you have cloned the repo to your desktop, build the docker image: `docker build -t creative_approval .`
- Run the docker image: `docker run -p 8000:8000 creative_approval`
- Navigate to `http://localhost:8000/docs` in a browser where you can use swagger to test the endpoints

## Rules I chose

The service currently applies **three rules** that align with the **ASA CAP Code** and the **Global Outdoor Copy Approval Guidelines**.

### 1. Contrast Check

* **What it does:** Ensures the image has sufficient contrast (measured by pixel intensity standard deviation).
* **Decision:** Reject if below threshold.
* **Why it matters:**

  * Outdoor ads must be **legible and clear** at a distance.
  * CAP Code: Marketing must not mislead by presenting information in an **unclear or unintelligible manner**.
  * Outdoor Guidelines: stress **legibility & readability** for all OOH placements.

---

### 2. Skin Content Check

* **What it does:** Flags creatives with a high proportion of skin-tone pixels.
* **Decision:** Requires manual review if above threshold.
* **Why it matters:**

  * CAP Code: Marketing must **avoid harm or offence**, including sexualisation or inappropriate depictions.
  * Outdoor Guidelines: ban **nudity, sexual imagery, or indecent depictions**.
  * Automated review cannot fully judge context → we trigger **REQUIRES\_REVIEW**.

---

### 3. Blood/Red Content Check

* **What it does:** Flags creatives with an unusually high proportion of red pixels (proxy for blood/gore).
* **Decision:** Requires manual review if above threshold.
* **Why it matters:**

  * CAP Code: Marketing must not **condone or encourage violence**.
  * Outdoor Guidelines: explicitly prohibit ads containing **violence or excessive blood**.
  * This safeguard helps catch shocking or graphic imagery.

---

## Design decisions & trade‑offs

* Chose **lightweight heuristics** (contrast, pixel ratios) → deterministic, no heavy ML.
* Used `Pillow` for image analysis.
* Returned **REQUIRES\_REVIEW** for sensitive cases (skin, blood) instead of outright rejection, aligning with CAP Code’s emphasis on **responsibility and context**.
* Structured rules as `ValidationRule` objects, making it easy to extend with more checks (e.g., minimum dimensions, file format validation).

---

## Policy Sources

* **ASA CAP Code (UK)** – sections on **Misleading Advertising (3)** and **Harm & Offence (4)**.
* **Global Outdoor Copy Approval Guidelines** – requirements for **clarity, legibility, and prohibitions on nudity/violence**.