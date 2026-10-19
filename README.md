# cURL-scrape

Pull the JSON data behind a web page using your browser's DevTools and `curl`, then convert it to CSV.

## Requirements

- **curl**: preinstalled on macOS. Check with `curl --version`.
- **Python 3.9+**
- **pandas**

```bash
pip install -r requirements.txt
```

## 1. Scrape the JSON from a web page

1. Open the page you want to scrape in Chrome
2. **Inspect** the page
3. Open the **Network** tab.
4. Click the **Fetch/XHR** filter.
5. Refresh the page so the requests show up in the list.
6. Find the **largest** request with the **`{;}`** icon. The icon marks a JSON response.
   - To confirm it's the right one, click it and check the **Preview** tab for the data you want.
7. Right-click the request and choose **Copy → Copy as cURL**.
8. In Terminal, `cd` into this project's `json/` folder.
9. Paste the cURL command and add `-o "filename.json"` to the end:

   ```bash
   curl 'https://example.com/api/...' \
     -H 'accept: application/json' \
     ... \
     -o "financial-statements.json"
   ```

> **Note:** The copied cURL contains your session cookies and auth tokens. Don't share or commit it. If the download comes back empty or with an error, your session may have expired, so refresh the page and copy the request again.

## 2. Convert the JSON to CSV

Set the filename at the bottom of [json-to-csv.py](json-to-csv.py):

```python
converter = JSONToCSVConverter("filename.json")
```

Then run:

```bash
python json-to-csv.py
```

The CSV is written to `csv/filename.csv`.

## 3. (Optional) Preview a large CSV

[get-structure.py](get-structure.py) copies the first 100 rows of a CSV into a smaller file so you can check its structure quickly. Edit the input and output paths in the script, then run:

```bash
python get-structure.py
```

## Project layout

```
json/              raw JSON downloaded with curl
csv/               converted CSV output
json-to-csv.py     JSON → CSV converter (flattens nested fields and transactions)
get-structure.py   writes a 100-row sample of a CSV
```
