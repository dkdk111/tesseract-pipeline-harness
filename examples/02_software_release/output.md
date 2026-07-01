## Ship the v2.1 release

### Build the application
- Compiled and bundled from a clean checkout; artifact hash recorded.
- Build is green and reproducible.

## Run the test suites

### Run unit tests
- Unit suite passed; fast feedback on core logic.
- Coverage held above the agreed threshold.
- (revised in light of: ### Build the application)

### Run integration tests
- Integration suite passed against staging dependencies.
- Contract boundaries verified.
- (revised in light of: ### Build the application)

### Run end-to-end tests
- End-to-end journeys passed on a production-like environment.
- No regressions in the critical user paths.
- (revised in light of: ### Build the application)

### Package the release artifacts
- Release artifacts packaged and signed.
- Version, changelog, and checksums attached.
- (revised in light of: ### Build the application)

[HELD FOR HUMAN APPROVAL] Deploy v2.1 to production
- Not self-designed or executed by the harness.
- A human must approve this action before it runs.
