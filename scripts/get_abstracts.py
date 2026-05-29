#! /usr/bin/env python

import io
import time

import requests
import pandas as pd
from tqdm import tqdm
from pypdf import PdfReader

INPUT = "cvpr2026_papers.csv"
OUTPUT = "cvpr2026_with_abstracts.csv"

df = pd.read_csv(INPUT)

try:
    done = set(pd.read_csv(OUTPUT)["paper_url"])
except:
    done = set()

def extract_from_pdf(pdf_url):
    try:
        r = requests.get(pdf_url, timeout=15)
        pdf = PdfReader(io.BytesIO(r.content))

        # first page usually contains abstract
        text = pdf.pages[0].extract_text()

        if not text:
            return ""

        # heuristic: extract section after "Abstract"
        text = text.replace("\n", " ")
        idx = text.lower().find("abstract")

        if idx != -1:
            return text[idx + len("abstract"): idx + 1500].strip()

        return text[:1500]

    except:
        return ""

def get_abstract(row):
    if row["paper_url"] in done:
        return None

    # try PDF first (more reliable than HTML)
    pdf = row.get("pdf_url", "")
    if pdf:
        abs_text = extract_from_pdf(pdf)
        if abs_text:
            return abs_text

    return ""

def append(row):
    pd.DataFrame([row]).to_csv(
        OUTPUT,
        mode="a",
        header=False,
        index=False
    )

for _, r in tqdm(df.iterrows(), total=len(df)):

    if r["paper_url"] in done:
        continue

    abstract = get_abstract(r)

    append({
        "title": r["title"],
        "authors": r["authors"],
        "pdf_url": r["pdf_url"],
        "paper_url": r["paper_url"],
        "abstract": abstract
    })

    done.add(r["paper_url"])
    time.sleep(1)

print("done")
