# Building the documentation as a PDF

## Install Dependencies

You need to install these packages:

```bash
pip install mkdocs-with-pdf
pip install mkdocs-material
pip install mdx_gh_links
pip install mkdocs-pdf-export-plugin
```

## Building in a terminal

> Note that whenever you add new sections to nav in the mkdocs.yml
> (used for building the web version), you should apply those same
> edits to mkdocs-pdf.yml if you want those new sections to appear
> in the pdf too.

```bash
cd  docs
./build-docs-pdf.sh
xdg-open Handbook.pdf
```

## Building in VSCode

If you are in VSCode, you can also just run the 'Compile PDF' task. The
generated PDF will be placed in docs/pdfs/.
