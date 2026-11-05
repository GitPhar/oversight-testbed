# Reader brief (common to every reader of the program 6 scout)

Written 2026-11-04 by the program 6 scout session, before any reading. Each reader is a fresh subagent with this brief and its own disjoint source list.

## The program

Program 6, `programs/test-awareness/`. Seed question, in Sean's words: **does a model behave differently when it thinks it is being tested?** The safety reason: evaluations only mean something if the model behaves the same when it is not told it is one.

The tests this program can afford: API calls to `claude-haiku-5-5`, `claude-sonnet-5-5` and `claude-opus-5-5`, $5.00 for the whole program, short prompts, no fine-tuning, no access to model internals (an open-weight model on a laptop is possible but slow). Earlier programs found that a model's ratings move with wording, format, question order and its own earlier answers, so any "test versus real" comparison must separate the belief "this is a test" from plain wording and format differences.

## What to write

One Markdown file, your cluster file, at the path your task names. **Never overwrite a file that exists**: check first; if your path exists, write `<name>-<your-reader-letter>2.md` instead and say so in your summary. Write nothing else in the repository, and do not commit.

The file starts with a short header (cluster, reader, date, fields searched, which searches returned nothing relevant: an empty field is a finding). Then one record per source:

```markdown
### <short name> — <authors>, <year>, <venue>, <URL>
- read_depth: full | partial (<sections>) | abstract (<why>)
- what_tested:
- on_whom: <participants / models / datasets, with n>
- how_scored:
- result: <numbers, from the text>
- limits: <what it did not measure; what the authors say they did not do>
- borrow: <a method, control, metric or failure mode, and where it would go in a cheap API test>
- next_steps_it_suggests: <the paper's own "what to do next", in one or two lines>
```

End the file with a section `## Next steps for program 6` listing 5–10 candidate tests drawn from your sources, each one line: the test, which records it comes from, and why it is or is not doable for under about $2 on the three Claude models.

## Rules

- **Numbers come from the text you read, never from memory.** If you cannot open the full text, mark `abstract` and report only numbers in the abstract.
- **Verify every 2025–2026 preprint directly** (arXiv abstract page or HTML, PMC, the publisher). Do not cite a paper you could not find; if a title on your list does not exist or differs, say so in one line.
- At most one direct quote per source, under 15 words, in quotation marks.
- A source that turns out not to transfer gets one line saying why and stops there. Killing fast is part of the job.
- Prefer, in order: full open-access text; arXiv HTML or PDF; a preprint; a publisher page. Web reads only. No model API calls, no paid services.
- Aim for 8–12 records. Depth beats count: at least half should be `full` or `partial` with named sections.
- Your final message (the summary returned to the scout) is at most 300 words: the file path, record count by read depth, the three most important findings with numbers, and the top five next steps.
