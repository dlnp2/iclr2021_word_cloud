# To use this script, run `brew install chromedriver` first.
from pathlib import Path

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from wordcloud import WordCloud

NAME = "iclr2021"
URL = "https://openreview.net/group?id=ICLR.cc/2021/Conference"
TAGS = ["#oral-presentations", "#spotlight-presentations", "#poster-presentations"]
DRIVER = "/opt/homebrew/bin/chromedriver"

options = webdriver.ChromeOptions()
options.add_argument("--headless")

texts_all = []
results = pd.DataFrame()
for tag in TAGS:
    driver = webdriver.Chrome(service=Service(DRIVER), options=options)
    driver.implicitly_wait(30)  # wait for complete page loading
    url = URL + tag
    print(url)
    driver.get(url)
    content = driver.find_element(By.ID, tag.replace("#", ""))
    texts = []
    for note in content.find_elements(By.CLASS_NAME, "note"):
        texts.append(note.find_element(By.TAG_NAME, "h4").text)
    texts_all.extend(texts)
    _result = pd.DataFrame({"title": texts, "type": tag.replace("#", "")})
    results = pd.concat([results, _result])
    driver.quit()


outdir = Path("./results")
outdir.mkdir(exist_ok=True)

wordcloud = (
    WordCloud(background_color="white", max_font_size=40, scale=2.5)
    .generate("\n".join(texts))
    .to_file(str(outdir / f"{NAME}.png"))
)
results.to_csv(outdir / f"{NAME}.csv", index=False)
print("Done.")
