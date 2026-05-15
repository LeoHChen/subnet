PYTHON ?= python3
MARKDOWN ?= docs/cpvss-subnet-design.md
HTML ?= index.html
PORT ?= 8080

.PHONY: html build serve clean help

html build: $(HTML)

$(HTML): $(MARKDOWN) tools/render_markdown.py
	$(PYTHON) tools/render_markdown.py $(MARKDOWN) $(HTML)

serve: html
	$(PYTHON) -m http.server $(PORT)

clean:
	rm -f $(HTML)

help:
	@printf '%s\n' \
		'Targets:' \
		'  make html        Regenerate index.html from docs/cpvss-subnet-design.md' \
		'  make serve       Regenerate and serve locally on PORT=8080' \
		'  make clean       Remove generated index.html' \
		'' \
		'Variables:' \
		'  MARKDOWN=path    Source Markdown file' \
		'  HTML=path        Output HTML file' \
		'  PORT=8080        Local server port'
