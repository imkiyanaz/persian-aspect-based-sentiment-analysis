# Data Availability

The original workflow uses Taaghche book-review data and several intermediate annotation files.

For the public portfolio repository, the raw corpus and row-level review/prediction files are intentionally excluded. They contain bulk user-generated text and are not necessary to inspect the modeling approach or aggregate results.

The original processed corpus contained 70,410 reviews. The context-extraction stage produced 46,221 aspect-context rows across 29,708 comments, 193 books, and 11 aspect categories.

Files referenced by the research notebook but not included here include:

- `taaghche_absa_aspect_detection_final_clean.csv`
- `taaghche_aspect_contexts.xlsx`
- `gold_aspect_annotation_prelabelled.xlsx`

Aggregate results required to review model performance are available under `results/`.
