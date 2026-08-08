# Elyndor — developer quality checks (headless, no Godot required).
#
# Run the exact same validation the CI pipeline enforces:
#
#   make ci          # full pytest + verify + region review + quality gate
#   make check       # quality gate only (verify + review + contracts + saves + docs)
#   make test        # full pytest suite
#   make verify      # tactical combat foundation verification
#   make review      # living-world Region Completion Review
#   make gate        # CI quality gate (no pytest)

PYTHON ?= python

.PHONY: ci check test verify review gate

ci:
	$(PYTHON) scripts/ci_quality_gate.py --pytest

check: gate

test:
	$(PYTHON) -m pytest -q

verify:
	$(PYTHON) -m tactical.verify

review:
	$(PYTHON) -m tactical.living_world.region_review

gate:
	$(PYTHON) scripts/ci_quality_gate.py
