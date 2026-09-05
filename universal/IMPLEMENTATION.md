# SkillMatch Universal Backend — Final

## Design contract

The backend has three independent deterministic outputs:

- **Job Match:** compares job requirements against resume evidence.
- **ATS Readiness:** evaluates document/parser characteristics only; it is not an ATS-pass probability.
- **Resume Health:** evaluates resume quality independent of the supplied job description and adapts to career stage.

The LLM is an **interpretation layer only**. It cannot set scores, create requirements, or upgrade deterministic evidence.

## AI provider

Set `OPENAI_API_KEY` to use OpenAI. If it is absent, the backend falls back to an OpenAI-compatible Groq endpoint using `GROQ_API_KEY`.

For production, pin `OPENAI_MODEL` or `GROQ_MODEL` to a model available to the configured account.

## Verification

Run:

```bash
python -m pytest -q
python -m compileall -q .
```

The test suite covers multiple occupations, aliases, required/preferred classification, negation, evidence strength, student/experienced resume health, LLM contradiction rejection, randomized score bounds, and adversarial text.


## Final verification performed

In addition to the automated suite, the final logic was stress-tested with 5,000 randomized resume/JD matching cases, 2,000 adversarial AI-output contract cases, and alias matrices covering technical, business, marketing, engineering, healthcare, legal, and education terminology. No score-bound or matcher exceptions were observed.
