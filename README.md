## Description
This is a repo holding some of the initial test ideas that lead to a website I later made called <a href="https://knittoknit.com" target="_blank" rel="noopener noreferrer">Knit to Knit</a>.

Basic Knitting Grid/ is an editor made using python and tkinter. And can be run by changing directory into `Basic Knitting Grid/` and running `uv run KnittingAppRun.py`

knitting_app/ can be bundled into a Macos application using `uv run pyinstaller knitting_app/SweaterMaker.spec` or just run via `uv run python -m knitting_app.runner`

## Setup
Install uv if you don't have it already.

Run `uv sync` to install Python dependencies