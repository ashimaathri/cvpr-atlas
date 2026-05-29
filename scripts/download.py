#! /usr/bin/env python

import time

import requests
import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm

BASE_URL = "https://openaccess.thecvf.com"
CVPR_URL = f"{BASE_URL}/CVPR2026?day=all"

papers = []

html = requests.get(CVPR_URL).text
soup = BeautifulSoup(html, "lxml")

paper_links = []

for link in soup.find_all("a"):

    href = link.get("href", "")

    if "/content/CVPR2026/html/" in href:

        full_url = BASE_URL + "/" + href.lstrip("/")

        if full_url not in paper_links:
            paper_links.append(full_url)

print("Found paper pages:", len(paper_links))

for paper_url in tqdm(paper_links):

    try:

        page = requests.get(paper_url).text
        paper_soup = BeautifulSoup(page, "lxml")

        title = paper_soup.find("div", id="papertitle")
        title = title.text.strip() if title else ""

        authors = paper_soup.find("div", id="authors")
        authors = authors.text.strip() if authors else ""

        abstract_header = paper_soup.find("h3", string="Abstract")

        abstract = ""

        if abstract_header:
            abstract_div = abstract_header.find_next("div")
            if abstract_div:
                abstract = abstract_div.text.strip()

        pdf_link = ""

        for a in paper_soup.find_all("a"):

            href = a.get("href", "")

            if href.endswith(".pdf"):
                pdf_link = BASE_URL + "/" + href.lstrip("/")
                break

        papers.append({
            "title": title,
            "authors": authors,
            "abstract": abstract,
            "paper_url": paper_url,
            "pdf_url": pdf_link,
        })

        time.sleep(0.2)

    except Exception as e:
        print("Error:", paper_url, e)

df = pd.DataFrame(papers)

df.to_csv("cvpr2026_papers.csv", index=False)

print("Saved", len(df), "papers")
