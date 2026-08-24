# SkillMatch Insights

Build the frontend of my existing project, SkillMatch AI.

THIS IS AN EXISTING WORKING PROJECT.

DO NOT REBUILD THE PROJECT FROM SCRATCH.

DO NOT REPLACE THE BACKEND.

DO NOT CHANGE THE ATS ALGORITHM.

DO NOT INVENT A NEW API.

DO NOT REMOVE EXISTING FUNCTIONALITY.

Your responsibility is to create a highly polished, production-quality FRONTEND around the existing FastAPI backend.

==================================================

1. PROJECT PURPOSE

==================================================

SkillMatch AI is a resume-to-job matching application.

A user:

1. Uploads a PDF resume

2. Pastes a job description

3. Clicks Analyze

4. The backend extracts resume text

5. The backend extracts skills

6. The backend parses Required vs Preferred skills

7. The backend calculates a deterministic weighted ATS score

8. Groq generates qualitative AI analysis

9. React displays the complete analysis

The backend already works.

The frontend must make this feel like a real product.

==================================================

2. EXISTING BACKEND — DO NOT REPLACE

==================================================

The existing backend is:

FastAPI

Python

pdfplumber

deterministic skill extraction

job-description parsing

weighted ATS scoring

Groq AI integration

The existing endpoint is:

POST http://127.0.0.1:8000/analyze

It accepts multipart/form-data:

file

job_description

The frontend must call this existing endpoint.

Do NOT introduce:

- Supabase

- Firebase

- another backend

- another database

- another AI provider

- mock API data

- fake scoring

- a new server architecture

The backend is the source of truth.

==================================================

3. EXISTING API RESPONSE

==================================================

The frontend must consume this existing response structure:

{

  "success": true,

  "filename": "resume.pdf",

  "text": "...",

  "resume_skills": [

    "Python",

    "FastAPI",

    "PostgreSQL"

  ],

  "required_skills": [

    "Python",

    "SQL",

    "FastAPI"

  ],

  "preferred_skills": [

    "AWS",

    "Docker"

  ],

  "scoring": {

    "ats_score": 61.54,

    "required": {

      "matched": [

        "Python",

        "FastAPI"

      ],

      "missing": [

        "SQL"

      ],

      "matched_count": 2,

      "total_count": 3

    },

    "preferred": {

      "matched": [

        "AWS"

      ],

      "missing": [

        "Docker"

      ],

      "matched_count": 1,

      "total_count": 2

    },

    "earnings": {

      "earned_points": 2.5,

      "possible_points": 4

    }

  },

  "ai_analysis": {

    "summary": "...",

    "strengths": [

      "...",

      "...",

      "..."

    ],

    "weaknesses": [

      "...",

      "..."

    ],

    "recommendations": [

      "...",

      "...",

      "..."

    ],

    "experience_relevance": "...",

    "skill_gap_analysis": "..."

  },

  "message": "Resume analyzed successfully"

}

The real backend response may contain additional fields.

Do not break if additional fields exist.

==================================================

4. CRITICAL API RULE

==================================================

Do not calculate the ATS score in React.

Do not duplicate backend business logic.

React should display:

scoring.ats_score

and the other scoring fields exactly as returned.

The frontend is a presentation layer.

==================================================

5. DESIGN DIRECTION

==================================================

I have provided a visual reference.

Use the reference as inspiration for:

- composition

- typography

- spacing

- contrast

- asymmetry

- editorial layout

- visual confidence

- black/white palette

- acid-lime accent

- thin borders

- oversized typography

- intentional whitespace

- visual artifacts

DO NOT COPY THE WEBSITE.

Translate the visual language into an original SkillMatch AI interface.

==================================================

6. ABSOLUTELY NO GENERIC AI SaaS DESIGN

==================================================

DO NOT use:

- purple/blue gradients

- blue/purple AI backgrounds

- glowing blobs

- neon gradients

- excessive glassmorphism

- generic AI sparkles

- robot illustrations

- generic AI icons

- giant gradient text

- excessive rounded cards

- random floating cards everywhere

- generic dashboard templates

- excessive shadows

- rainbow color systems

- "AI MAGIC" aesthetics

I specifically want to avoid the typical AI-generated website look.

The design should feel:

editorial

technical

premium

confident

minimal

modern

slightly brutalist

typography-driven

==================================================

7. COLOR SYSTEM

==================================================

Primary visual system:

BLACK

WHITE / OFF-WHITE

ACID LIME / CHARTREUSE

Use the lime accent strategically.

Use it for:

- primary CTA

- active states

- score highlights

- important indicators

- small decorative details

Do NOT make the entire interface lime.

Do NOT introduce purple or blue as primary branding colors.

Create CSS variables/design tokens for the color system.

==================================================

8. TYPOGRAPHY

==================================================

Typography is one of the most important parts of the design.

Use a high-quality modern grotesk such as:

Geist

Inter

Manrope

Prefer Geist or Inter if available.

Use strong hierarchy:

Display:

800/900

Section headings:

600/700

Labels:

500/600

Body:

400/450

Metadata:

400/500

Tune together:

font-size

font-weight

line-height

letter-spacing

max-width

Do not simply make everything bold.

The large headline should have strong visual authority.

Supporting copy should be significantly quieter.

==================================================

9. LANDING / HERO

==================================================

Create a strong editorial hero.

Suggested direction:

Small eyebrow:

RESUME × JOB MATCHING

Large headline:

KNOW WHERE

YOU STAND.

Supporting copy:

Upload a resume. Add a job description.

Get a weighted match score, skill gaps, and

AI-powered recommendations.

The exact wording may be refined if you have a better product-specific alternative.

Do not create a giant marketing page.

This is a tool.

The user should reach the actual resume/JD workflow quickly.

==================================================

10. HEADER

==================================================

Create a minimal professional header.

Brand:

SKILLMATCH AI

Use strong typography.

The AI portion can use the lime accent subtly.

Do not create a massive navigation bar.

If a connection/backend status exists, make it subtle and useful.

Do not clutter the header.

==================================================

11. MAIN INPUT WORKSPACE

==================================================

Create a strong two-column desktop composition:

LEFT:

YOUR RESUME

RIGHT:

THE OPPORTUNITY

Use editorial numbering if appropriate:

01 YOUR RESUME

02 THE OPPORTUNITY

with subtle rules.

--------------------------------------------------

RESUME

--------------------------------------------------

Provide:

- drag and drop

- file picker

- PDF validation

- selected file state

- filename

- remove/replace

- hover state

- drag-over state

- loading state

- error state

Do not make the upload box unnecessarily huge.

Avoid excessive rounded corners.

Use strong typography and thin borders.

--------------------------------------------------

JOB DESCRIPTION

--------------------------------------------------

Provide:

- large textarea

- clear label

- useful placeholder

- comfortable writing area

- validation

- character count if useful

Make the textarea feel like part of the editorial composition rather than a generic form control.

==================================================

12. PRIMARY CTA

==================================================

The Analyze button is the most important action.

Use the lime accent.

Possible treatment:

ANALYZE MATCH →

Strong black text.

Sharp/simple geometry.

Clear hover state.

Disabled state.

Loading state.

Do not use a giant glowing gradient button.

==================================================

13. LOADING EXPERIENCE

==================================================

Do not simply display:

Loading...

Create a polished analysis state.

Possible stages:

01  Extracting resume

02  Matching skills

03  Calculating ATS score

04  Generating AI insights

IMPORTANT:

Do not pretend these are real-time backend stages unless the backend actually provides progress information.

These are visual stages only.

Do not show fake percentages.

Prevent layout shift.

==================================================

14. RESULTS EXPERIENCE

==================================================

Once analysis completes, transition into a professional report.

The result should feel like:

"candidate assessment report"

not:

"AI chatbot response."

Primary hierarchy:

MATCH SCORE

61.54%

Then:

Required Skills

Preferred Skills

Then:

AI Assessment

Use strong typography and editorial composition.

==================================================

15. ATS SCORE

==================================================

The ATS score is the primary quantitative result.

Make it prominent.

Do NOT create a generic glowing circular AI gauge.

Consider a typographic/editorial treatment:

MATCH SCORE

61.54%

8 / 13 POINTS

with a restrained progress indicator.

Use the backend value exactly.

Do not recalculate it.

==================================================

16. REQUIRED SKILLS

==================================================

Show:

Required Skills

6 / 9 matched

MATCHED:

✓ Python

✓ FastAPI

✓ PostgreSQL

✓ REST API

MISSING:

× Linux

× Docker

× Microservices

Use compact tags or typographic rows.

Do not turn every skill into a huge rounded card.

Use color plus symbols/text so meaning is not communicated by color alone.

==================================================

17. PREFERRED SKILLS

==================================================

Show:

Preferred Skills

4 / 8 matched

MATCHED:

✓ AWS

✓ React

✓ Redis

MISSING:

× Docker

× Kubernetes

× CI/CD

× System Design

Keep the visual treatment related to Required Skills but slightly lower in hierarchy.

==================================================

18. AI ASSESSMENT

==================================================

This is a major product feature.

Do NOT make it look like ChatGPT.

Do NOT use:

- robot icon

- sparkle icon

- purple gradient

- glowing AI card

Make it look like an intelligent professional assessment.

Structure:

AI ASSESSMENT

────────────────────────

SUMMARY

...

STRENGTHS

01 ...

02 ...

03 ...

AREAS TO IMPROVE

01 ...

02 ...

RECOMMENDATIONS

01 ...

02 ...

03 ...

EXPERIENCE RELEVANCE

...

SKILL GAP ANALYSIS

...

Use editorial hierarchy.

Recommendations should be especially readable and actionable.

==================================================

19. PRODUCT-SPECIFIC VISUAL ARTIFACTS

==================================================

The reference website uses visual artifacts around its main composition.

Translate that idea into SkillMatch.

If decorative visuals are needed, use SkillMatch-specific artifacts such as:

- resume preview snippets

- ATS score fragments

- skill-match fragments

- skill-gap fragments

- AI assessment fragments

- small resume document previews

Example visual language:

RESUME

PYTHON ✓

FASTAPI ✓

AWS ×

or:

MATCH

61.54%

or:

SKILL GAP

DOCKER

KUBERNETES

These should look like designed product artifacts.

Use black/white with small lime highlights.

Do not use random stock photographs merely to fill empty space.

If actual imagery is used, use properly licensed assets.

Prefer CSS-built or generated product-specific visual elements.

Decorative elements must support the product concept.

==================================================

20. LAYOUT / GRID

==================================================

Use a strong grid.

Use asymmetry intentionally.

Use whitespace intentionally.

Do not center everything.

Do not make every section a rounded rectangle.

Use:

- thin rules

- borders

- alignment

- spacing

- typography

to create structure.

Some elements may intentionally break the grid on desktop.

On mobile they must return to normal document flow.

==================================================

21. RESPONSIVE DESIGN

==================================================

Must work properly at:

desktop

laptop

tablet

mobile

Do not merely scale desktop down.

At mobile:

- stack the input areas

- reduce display typography appropriately

- simplify decorative elements

- preserve hierarchy

- keep CTA accessible

- prevent horizontal overflow

- keep text readable

No clipped content.

No horizontal scrolling.

==================================================

22. ACCESSIBILITY

==================================================

Treat accessibility as production functionality.

Use:

- semantic HTML

- proper labels

- keyboard navigation

- visible focus states

- accessible buttons

- aria-labels where necessary

- sufficient contrast

- status announcements for loading/errors

Do not rely only on color.

==================================================

23. ERROR STATES

==================================================

Handle:

- backend unavailable

- invalid PDF

- no file

- no job description

- failed analysis

- malformed response

- AI unavailable

- unexpected API response

If:

ai_analysis === null

DO NOT hide the ATS results.

Show:

AI INSIGHTS UNAVAILABLE

The deterministic ATS results should remain visible.

Example:

"The ATS analysis completed successfully, but AI insights are temporarily unavailable."

==================================================

24. EMPTY STATE

==================================================

Before analysis, make the page feel intentional.

Do not show a blank dashboard.

The user should clearly understand:

UPLOAD RESUME

+

ADD JOB DESCRIPTION

=

GET MATCH ANALYSIS

Use typography/visual structure rather than generic illustrations.

==================================================

25. RESULT RESET

==================================================

Allow the user to:

- analyze another resume

- replace the resume

- replace the job description

- start a new analysis

Do not force a page reload.

==================================================

26. COMPONENT ARCHITECTURE

==================================================

Keep the React code maintainable.

Use reusable components where appropriate.

Potential structure:

components/

  Header

  Hero

  ResumeUploader

  JobDescriptionInput

  AnalyzeButton

  AnalysisLoading

  AnalysisResults

  ATSScore

  SkillBreakdown

  SkillList

  AIAnalysis

  RecommendationList

  EmptyState

  ErrorState

Use the existing project structure if it is already sensible.

Do not create unnecessary abstraction.

Do not put the entire application into one enormous component.

==================================================

27. API / CODE QUALITY

==================================================

Keep API logic separate from presentation where practical.

Create a clear API function for:

POST /analyze

Handle:

loading

success

error

abort/reset

Do not expose API secrets in React.

There are NO API keys required in the frontend.

The Groq key remains exclusively in the FastAPI backend.

==================================================

28. TECHNOLOGY

==================================================

You may use appropriate frontend technologies.

Current/allowed stack:

React

Tailwind CSS

Framer Motion / Motion

Lucide React

You may use:

shadcn/ui

Radix

CSS variables

custom CSS

if they genuinely improve the result.

Do not install dependencies unnecessarily.

Do not create dependency bloat.

If existing Tailwind configuration needs adjustment, do it cleanly.

==================================================

29. NO BACKEND CHANGES

==================================================

Do NOT modify:

backend/main.py

backend/services.py

backend/skills.py

backend/ai_service.py

unless you discover a genuine frontend/API-contract incompatibility.

If you believe a backend modification is absolutely necessary:

STOP before changing it.

Explain exactly:

1. What is incompatible

2. Why it is necessary

3. What you want to change

The backend is currently tested and working.

==================================================

30. GIT SAFETY

==================================================

Do not delete the existing project.

Do not destroy working files.

Preserve the existing Git repository.

Make frontend changes in a clean, reviewable manner.

Do not commit secrets.

Never expose:

GROQ_API_KEY

or any other API key in frontend code.

==================================================

31. QUALITY BAR

==================================================

This must not look like a college assignment.

It should look like a real product someone could launch.

Before finishing, perform a complete visual and functional review.

Check:

TYPOGRAPHY

- hierarchy

- line height

- letter spacing

- font consistency

LAYOUT

- alignment

- spacing

- grid

- whitespace

- responsive behavior

VISUAL

- no accidental gradients

- no generic AI aesthetics

- no excessive cards

- no excessive rounded corners

- no visual clutter

- consistent borders

- consistent accent usage

FUNCTION

- upload

- drag/drop

- JD input

- analyze

- loading

- results

- ATS score

- skills

- AI analysis

- errors

- reset/new analysis

RESPONSIVE

- desktop

- tablet

- mobile

ACCESSIBILITY

- keyboard

- focus

- labels

- contrast

- status messages

CODE

- no console errors

- no broken imports

- no unnecessary duplication

- no dead components

- no hardcoded analysis results

==================================================

32. IMPORTANT FINAL INSTRUCTION

==================================================

Do not optimize for "wow" through effects.

Optimize for:

TYPOGRAPHY

COMPOSITION

HIERARCHY

SPACING

CONTRAST

USABILITY

DETAIL

CONSISTENCY

The reference website feels premium because its design system is coherent.

SkillMatch should have its own equally coherent identity.

The final impression should be:

"Someone intentionally designed this product."

NOT:

"An AI generated a React dashboard."

Inspect the existing frontend first.

Then make the changes.

After implementation, verify that the existing FastAPI `/analyze` flow still works.

Finally report:

1. Files changed

2. Dependencies added

3. Major design changes

4. Functional tests performed

5. Responsive tests performed

6. Any remaining issues

Do not claim something was tested unless you actually tested it.

This project was built with [Lovable](https://lovable.dev).

## Build with Lovable

Continue developing this project in the [Lovable editor](https://lovable.dev/projects/d51c762f-d69f-4a9f-9a1d-9b6ff315bf14).

- **Ship faster**: describe what you want to build and Lovable handles the code.
- **Stay in sync**: every change made in Lovable is committed straight to this repository.
- **Full ownership**: this code is yours. Push to `main` on GitHub and your changes sync back into Lovable, ready for your next prompt.

## Development

Prefer working locally? You need Node.js and npm — [install with nvm](https://github.com/nvm-sh/nvm#installing-and-updating).

```sh
git clone <this-repository-url>
cd <repository-name>
npm i
npm run dev
```
