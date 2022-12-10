# web2epub
Download and convert one or more webpages into an ePub file.

## Packages used
- [requests](https://pypi.org/project/requests/)
- [readabilipy](https://pypi.org/project/readability/) for extracting the actual title and content from the page data
- [ebooklib](https://pypi.org/project/EbookLib/) to create the ePub file

## Quickstart

```
python -m venv env
source env/bin/activate
pip install -r requirements.txt
python web2epub.py <link>
```

## Examples

`python web2epub.py https://100r.co/site/off_the_grid.html`  

Comma separate two or more URL's. Each URL will be added as a chapter to the ePub.  

`python web2epub.py https://100r.co/site/off_the_grid.html,https://100r.co/site/cooking.html`  

This script will try to extract title and author from the content. If you provide more than one url, you will be prompted to enter title and author.  

## Disclaimer
Creator of this software is not in charge of any and has no responsibility for any kind of:
- Unlawful or illegal use of the tool.
- Legal or Law infringement (acted in any country, state, municipality, place) by third parties and users.
- Act against ethical and / or human moral, ethic, and peoples and cultures of the world.
- Malicious act, capable of causing damage to third parties, promoted or distributed by third parties or the user through this tool.

## License
This is free and open source software. You can use, copy, modify,
merge, publish, distribute, sublicense, and/or sell copies of it,
under the terms of the [MIT License](LICENSE.md).

This software is provided "AS IS", WITHOUT WARRANTY OF ANY KIND,
express or implied. See the [MIT License](LICENSE.md) for details.

##Contact

[eklop@proton.me](mailto:eklop@proton.me)
