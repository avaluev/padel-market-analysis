# Padel Coaching Tech Research — developer convenience targets
#
# All targets are non-destructive. Targets that touch the public site
# (build, deploy) re-run the deterministic builders; targets that touch
# the research pipeline (run-pipeline, new-run) require OPENROUTER_API_KEY.

.PHONY: help install lint typecheck test test-fast audit build sanitise \
	check-quality check-links seo-assets clean docs deploy-check
.DEFAULT_GOAL := help

PY ?= python3
NODE ?= node

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | sort | \
	  awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-22s\033[0m %s\n", $$1, $$2}'

install: ## Install Python dev deps + Node deps
	$(PY) -m pip install -e '.[dev]'
	npm install --no-audit --no-fund

lint: ## Run ruff lint + format check
	ruff check scripts tests
	ruff format --check scripts tests

typecheck: ## Run mypy --strict on scripts/ and tests/
	mypy scripts tests

test: ## Run the pytest suite with coverage
	pytest

test-fast: ## Run pytest without coverage (quick iteration)
	pytest --no-cov -x

build: ## Rebuild the public pages (idempotent)
	$(NODE) scripts/build_pages.mjs
	$(NODE) scripts/inject_topnav.mjs
	$(PY) scripts/build_seo_assets.py

sanitise: ## Apply content sanitiser to top-level pages
	$(PY) scripts/sanitise_pages.py

check-quality: ## Run the unified content / SEO quality gates
	$(PY) scripts/check_quality.py

check-links: ## Verify every URL in the site bundle returns HTTP 200
	bash scripts/verify_links.sh

seo-assets: ## Regenerate robots.txt / llms.txt / sitemap.xml / etc
	$(PY) scripts/build_seo_assets.py

audit: build check-quality ## Full local pre-merge audit
	@echo ""
	@echo "[audit] all checks passed"

deploy-check: audit ## Pre-deploy gate (runs locally what CI runs)
	@bash -c 'if git diff --quiet reports/final; then echo "no public changes — skipping deploy"; exit 0; fi'
	@echo "[deploy-check] reports/final/ has unstaged or staged changes"

docs: ## Build docs/ from the docs/ source (placeholder)
	@echo "docs target not yet implemented"

clean: ## Remove generated artefacts (NOT the public bundle)
	rm -rf htmlcov .coverage .mypy_cache .ruff_cache .pytest_cache
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
