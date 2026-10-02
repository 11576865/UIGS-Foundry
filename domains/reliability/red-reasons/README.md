# Red Reason Registry

Red Reasons normalize why a CI/build/test/release run is red.

The registry exists so "CI failed" is not treated as a single undifferentiated event. A red run should be classifiable as policy violation, build failure, test failure, runtime smoke failure, environment/toolchain failure, packaging/release failure, resource-budget failure, infrastructure/flaky failure, or an unresolved category.

The taxonomy is intentionally independent from any one workflow name.
