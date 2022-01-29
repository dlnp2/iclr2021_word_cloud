# To use this script, run `brew install chromedriver` first.
from pathlib import Path

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from wordcloud import WordCloud

NAME = "neurips2021"
URL = "https://neurips.cc/Conferences/2021/Schedule?type="
TAGS = ["Oral", "Poster", "Spotlight"]
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
    content = driver.find_element(By.ID, "main")
    texts = []
    for note in content.find_elements(By.CLASS_NAME, "maincardBody"):
        texts.append(note.text)
    texts_all.extend(texts)
    _result = pd.DataFrame({"title": texts, "type": tag})
    results = pd.concat([results, _result])
    driver.quit()


outdir = Path("./results")
outdir.mkdir(exist_ok=True)

wordcloud = (
    WordCloud(background_color="white", max_font_size=None, max_words=300, scale=2.5)
    .generate("\n".join(texts))
    .to_file(str(outdir / f"{NAME}.png"))
)
results.to_csv(outdir / f"{NAME}.csv", index=False)
print("Done.")
