# CVPR Atlas

Structured metadata for CVPR papers across years.

This repository provides:

* CSV datasets containing CVPR paper metadata
* Python scripts to extract paper information for different years
* A foundation for community-driven analysis of research trends in computer vision

Each dataset may include:

* Paper titles
* Authors
* Abstracts
* Paper links
* Additional metadata when available

## Usage
Activate the virtual environment:

```bash
source .venv/bin/activate
```

Install dependencies with `uv`:

```bash
uv sync
```

Download paper metadata:

```bash
./scripts/download.py
```

Fetch abstracts:

```bash
./scripts/get_abstracts.py
```

## Goals

The goal of this project is to make CVPR research more accessible and easier to explore programmatically.

Potential community contributions include:

* Trend analysis
* Topic clustering
* Embedding visualizations
* Citation/network analysis
* Interactive dashboards
* Year-over-year comparisons

## Contributing

Contributions are welcome. Feel free to open issues, improve the scraper, add datasets for other years, or build analysis tools on top of the data.

## License

MIT License
