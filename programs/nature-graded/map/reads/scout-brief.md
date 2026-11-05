# Scout brief for reader agents (program 3, nature-graded)

You are one of five reader agents for a literature scout. Today is 2026-11-04. The program asks open questions in quantum foundations and IBM Heron r2 device physics that can be tested cheaply on `ibm_fez` (156-qubit Heron r2) under the IBM Open Plan: **374 QPU seconds remain** before the project's hard stop. The quantum chip is used as *ground truth* (nature as referee), never as a computational resource.

Empirical cost rule from our own jobs on ibm_fez: 39 circuits × 4,000 shots = 156,000 shots billed 44 s (≈ 0.28 ms per shot, dominated by a ~250 µs repetition delay), and 1 circuit × 1,000 shots billed 2 s (per-job overhead ≈ 1–2 s). Open Plan: no pulse access, no qutrit control, jobs queue for hours (one waited 2 h 50 min), SamplerV2 / EstimatorV2 only, dynamic circuits (mid-circuit measurement + feed-forward) are available on Heron.

## Rules (strict)

1. **Full reads.** Open the full text (arXiv HTML at `https://arxiv.org/html/<id>` or the abs/PDF, or an open-access publisher page). Use WebFetch and WebSearch only. No model API calls of your own, no paid services, no hardware.
2. **Numbers only from the text you opened.** If you could open only the abstract, mark `read_depth: abstract` and report no numbers that are not in the abstract. Never fill a number from memory. If a paper I name does not exist or has different authors/IDs than stated, say so plainly — that is a finding.
3. At most one direct quote per source, under 15 words, in quotation marks.
4. A source that does not transfer to our situation gets one line saying why, and stops.
5. Record, for every paper that ran on hardware: platform/device, number of qubits, number of circuits/settings, shots, the violation size in standard deviations or with CI, and what loopholes or assumptions the authors themselves say remain open. These numbers are what we cost our own tests from.
6. Write your output to the single file named in your task (in `/Users/seanpharris/nature-graded/related-work/`). Do not edit any other file. Do not run git.

## Record format (one per source)

```markdown
### <short name> — <authors>, <year>, <venue>, <URL>
- read_depth: full | partial (<sections>) | abstract (<why>)
- what_tested:
- on_whom: <platform / device / qubits, n circuits, shots>
- how_scored:
- result: <numbers, from the text>
- limits: <what it did not measure; what the authors say they did not do>
- borrow: <a method, control, metric or failure mode we can use>
- next_steps_it_suggests: <the paper's own "what to do next", one or two lines>
```

## End of your file

After the records, add a section `## Cluster summary` with:
- **Open questions that fit our budget** (each: the question; who came closest; why it is still open; a concrete circuit-level test on a Heron r2 chip — qubits, circuits, shots — and your QPU-second estimate using the cost rule above).
- **Questions that do not fit** (one line each, with the reason: needs pulse access, needs spacelike separation, needs >X s, already settled, etc.).
- **Fields searched that returned nothing relevant.**

Aim for 8–14 sources, read properly, rather than many skimmed. Report back in under 300 words: the file path, the number of sources and how many were full reads, and the 3 most promising open questions with costs.
