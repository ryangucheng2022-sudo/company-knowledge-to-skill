# CI kit

Ready-to-enable GitHub Actions setup, kept outside `.github/workflows/`
so it can be reviewed and versioned like any other file.

**Enable it:** copy `ci.yml` to `.github/workflows/ci.yml` and push.

The job validates the worked example in both export modes and both input
formats, runs the package consistency (drift) check, and asserts that a
deliberately dirty register (duplicate claim, empty claim) is rejected.
