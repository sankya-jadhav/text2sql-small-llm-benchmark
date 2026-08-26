I completed a baseline Zero-Shot Text-to-SQL experiment and compared it with a keyword-based schema pruning approach using Qwen2.5-Coder-7B-Instruct on 180 SPIDER benchmark questions.

Initial Results

The baseline achieved 75.56% execution accuracy (136/180), while the schema pruning experiment achieved 72.78% execution accuracy (131/180).

Schema pruning also provided significant efficiency improvements:

Average schema size reduced by 40.46%
Average prompt tokens reduced from 380.86 to 301.95
Average latency reduced from 2.82 seconds to 2.61 seconds

At the question level:

Both Correct: 122
Both Wrong: 35
Pruning Helped: 9
Pruning Hurt: 14
Error Analysis and Evaluation Issue

Manual analysis of the questions where schema pruning performed worse revealed that some failures were caused by SQL post-processing rather than model reasoning or schema pruning.

For example, several generated queries contained duplicate trailing semicolons:

SELECT COUNT(*) FROM airlines WHERE Country = 'USA';;

SQLite interprets this as multiple statements and returns the error:

You can only execute one statement at a time.

Therefore, these failures should not be interpreted as schema pruning failures. The SQL cleaning module is being improved to normalize generated queries by removing markdown formatting, extracting the SQL statement, and removing duplicate or trailing semicolons.

After updating the SQL cleaner, the existing generated SQL will be re-executed without rerunning model inference. This will provide a corrected evaluation and separate post-processing failures from actual model and schema-pruning failures.

Preliminary Findings from Error Analysis

The remaining pruning failures appear to fall into several categories:

Missing relationship tables or incorrect join paths
Unnecessary joins that change query results
Hallucinated tables or columns
Incorrect column selection
Semantic differences between generated SQL and the intended query
SQL post-processing and formatting errors

Overall, the experiment currently indicates that schema pruning provides meaningful efficiency benefits through substantial schema and prompt reduction, but the current keyword-based strategy can negatively affect complex queries that require multiple tables, relationship tables, or precise join paths.

The next step is to re-evaluate the existing results using the improved SQL cleaner and then perform a detailed error-category analysis on the remaining failures.


Your main finding can now be stated as:

The keyword-based schema pruning approach achieved substantial efficiency improvements while maintaining accuracy close to the full-schema baseline. On 180 SPIDER benchmark questions, schema pruning reduced the average schema size by 40.46%, prompt tokens by 20.72%, and inference latency by 7.40%. After correcting SQL evaluation artifacts caused by repeated trailing semicolons, execution accuracy decreased from 75.56% to 74.44%, representing a relatively small reduction of 1.12 percentage points.

And the trade-off is very clear:

The results indicate that schema pruning can substantially reduce the input context with limited degradation in execution accuracy. However, the remaining 11 cases where pruning hurt performance demonstrate that a simple keyword-based pruning strategy may fail to preserve important relational or semantic information required for complex SQL generation.



| Question ID | Database                     | Error Type                 | What Pruning Caused                | Example                           |
| ----------- | ---------------------------- | -------------------------- | ---------------------------------- | --------------------------------- |
| 37          | concert_singer               | Incorrect Join             | Missing/incorrect relationship     | concert directly joined to singer |
| 57          | pets_1                       | Semantic Error             | Lost DISTINCT                      | duplicate results                 |
| 158         | car_1                        | Semantic Misinterpretation | Extra table changed interpretation | Volvo logic changed               |
| 179         | flight_2                     | Invalid Table              | Incorrect table introduced         | `countries` doesn't exist         |
| 421         | museum_visit                 | Invalid Column             | Hallucinated column                | `Visit_ID`                        |
| 534         | student_transcripts_tracking | Aggregation Error          | COUNT DISTINCT changed semantics   | degree programs                   |
| 692         | voter_1                      | Unnecessary Join           | Changed result multiplicity        | votes join                        |
| 693         | voter_1                      | Unnecessary Join           | Changed DISTINCT output            | area_code_state                   |
| 701         | voter_1                      | Unnecessary Join           | Changed result set                 | votes join                        |
| 780         | world_1                      | Semantic Error             | Missing DISTINCT                   | duplicate country codes           |
| 1027        | singer                       | Invalid Column             | Column hallucination               | `sname` instead of `Name`         |
