PYTHON ?= python3
MARKDOWN ?= docs/poseidon-subnet-design-tokenomics-proposal.md
HTML ?= index.html
RELEASE_METADATA ?= release.json
RELEASE_DIR ?= releases
RELEASE ?=
RELEASE_DOC ?= $(RELEASE_DIR)/$(RELEASE).md
COMMIT ?= $(shell git rev-parse --short HEAD 2>/dev/null || echo unknown)
RELEASE_DATE ?= $(shell date +%Y-%m-%d)
PORT ?= 8080

.PHONY: html build major-release serve clean help

html build: $(HTML)

$(HTML): $(MARKDOWN) tools/render_markdown.py
	$(PYTHON) tools/render_markdown.py $(MARKDOWN) $(HTML)

major-release:
	@test -n "$(RELEASE)" || (printf '%s\n' 'Usage: make major-release RELEASE=v1.0.0' && exit 1)
	@mkdir -p $(RELEASE_DIR)
	cp $(MARKDOWN) $(RELEASE_DOC)
	$(PYTHON) tools/render_markdown.py $(MARKDOWN) $(HTML) --release "$(RELEASE)" --commit "$(COMMIT)" --release-date "$(RELEASE_DATE)" --release-page "$(RELEASE_DIR)/$(RELEASE).html" --release-doc "$(RELEASE_DOC)" --metadata-out $(RELEASE_METADATA)
	$(PYTHON) tools/render_markdown.py $(MARKDOWN) "$(RELEASE_DIR)/$(RELEASE).html" --release "$(RELEASE)" --commit "$(COMMIT)" --release-date "$(RELEASE_DATE)" --release-page "$(RELEASE).html" --release-doc "$(RELEASE).md"

serve: html
	$(PYTHON) -m http.server $(PORT)

clean:
	rm -f $(HTML)

help:
	@printf '%s\n' \
		'Targets:' \
		'  make html        Regenerate index.html from docs/poseidon-subnet-design-tokenomics-proposal.md' \
		'  make major-release RELEASE=v1.0.0' \
		'                   Create a new major-release HTML snapshot' \
		'  make serve       Regenerate and serve locally on PORT=8080' \
		'  make clean       Remove generated index.html' \
		'' \
		'Variables:' \
		'  MARKDOWN=path    Source Markdown file' \
		'  HTML=path        Output HTML file' \
		'  RELEASE=vX.Y.Z   Major release version for release snapshots' \
		'  RELEASE_DOC=path Markdown archive path for major releases' \
		'  PORT=8080        Local server port'
