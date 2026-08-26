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