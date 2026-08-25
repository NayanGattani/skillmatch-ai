# Plan: improve favicon size and header logo fit

## Changes

1. **Favicon size**
   - Keep the current SkillMatch AI SM mark design and colors unchanged.
   - Regenerate `public/favicon.png` so the visible SM mark fills the favicon canvas more like standard website favicons.
   - Keep only minimal padding so the mark is large and readable in browser tabs, without touching the edges.

2. **Header logo lockup**
   - Keep the existing header typography, colors, spacing, and layout direction.
   - Adjust the header brand area so the SM mark feels aligned with `SKILLMATCH AI`.
   - Try a subtle vertical divider layout:

```text
[SM] | SKILLMATCH AI
```

   - Keep the divider small and understated, using existing border/foreground styling.
   - If the divider makes the header feel busier or cramped in preview, remove the divider and instead tune the logo size/alignment only.

3. **Preview verification**
   - Open the preview after the changes.
   - Check the header at desktop width and confirm the logo lockup looks balanced.
   - Check the favicon visually against the browser/tab reference so it appears comparable in size to other favicons.

## Technical details

- Update only `public/favicon.png` and `src/components/Header.tsx`.
- Use the existing favicon image as the source; do not redesign, recolor, or create a different mark.
- Enlarge the actual SM artwork inside the 64x64 favicon canvas rather than changing the website’s favicon link.
- Header changes stay limited to the brand anchor: logo dimensions, alignment, and possibly one subtle `|` divider.
