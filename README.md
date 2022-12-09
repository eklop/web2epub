# www2epub
Download and convert web content into an ePub file.

## Packages used
- [requests]()
- [readabilipy]() for extracting the actual title and content from the page data
- [ebooklib]() to create the ePub file

## Quickstart

```
python -m venv env
source env/bin/activate
pip install -r requirements.txt
python www2epub.py <link>
```

## Examples

**Download a single URL**
`python www2epub.py https://100r.co/site/off_the_grid.html`
- This script will try to extract title and author from the content

**Download multiple URL's**
- Comma separate two or more URL's. Each URL will be added as a chapter to the ePub.
- You have to manually enter a title and author

`python www2epub.py https://100r.co/site/off_the_grid.html,https://100r.co/site/cooking.html`

## Disclaimer & License
This script could be used to download copyrighted content. 
I'm not responsible for any copyright infringement caused by using this script. 
See [MIT License](LICENSE.md) for more details.