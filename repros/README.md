# repros

When I'm trying to reproduce or track down a bug, it's often useful to build a minimal example.
This helps check it really is a bug (and not my mistake), and it's a good starting point for a bug report.

This folder has some of those minimal examples, both for posterity and to give me a starting point the next time I need a minimal Scala/Ruby/whatever project.

Not every example becomes a bug report!

Often while trying to debug a simpler example, I discover a mistake in my own understanding.
Then I don't need to file a bug report, but I keep the project around anyway.

## Bugs filed from these examples:

*   [rack-test/rack-test#241](https://github.com/rack-test/rack-test/issues/241) – Possible bug with rack/test's handling of String response bodies
