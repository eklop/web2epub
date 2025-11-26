# web2epub
Download and convert one or more webpages into an ePub file.

## Required packages
- [requests](https://pypi.org/project/requests/)
- [readabilipy](https://pypi.org/project/readability/) for extracting the actual title and content from the page data
- [ebooklib](https://pypi.org/project/EbookLib/) to create the ePub file

## Quickstart

```
python -m venv env
source env/bin/activate
pip install -r requirements.txt
python web2epub.py "<URL>"
```

## Examples

**Single page (backward compatible)**  
`python web2epub.py https://example.com/article`

**Multiple pages via comma-separated string**  
`python web2epub.py "https://a.com/one,https://b.com/two"`

**Using flags**  
`python web2epub.py -u "https://a.com/one,https://b.com/two" -t "My Collection" -a "Various Authors"`

**From file with comments and blank lines**  
`python web2epub.py -f urls.txt -t "My Reading List" -a "Assorted"`

**Verbose logging**  
`python web2epub.py -u https://example.com/article --verbose`

### Using the `--file` option
- One URL per line.
- Lines starting with # are treated as comments.
- Empty lines are ignored.
  
**Example `urls.txt`:**  
```
# My reading list
https://example.com/article1
https://example.com/article2
# Another article
https://example.com/article3
```

## Notes
- For multiple URLs without `--title`/`--author`, you'll be prompted to provide a title and author.
- The script extracts content using readability algorithms
- Output EPUB files are named based on the title (slugified)
- Title and author can be specified via `--title`/`-t` and `--author`/`-a` arguments.

## Disclaimer
Creator of this software is not in charge of any - and has no responsibility for any kind of:
- Unlawful or illegal use of the tool.
- Legal or Law infringement (acted in any country, state, municipality, place) by third parties and users.
- Act against ethical and / or human moral, ethic, and peoples and cultures of the world.
- Malicious act, capable of causing damage to third parties, promoted or distributed by third parties or the user through this tool.

## License
This is free and open source software. You can use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of it, under the terms of the [MIT License](LICENSE.md).
This software is provided "AS IS", WITHOUT WARRANTY OF ANY KIND, express or implied. See the [MIT License](LICENSE.md) for details.

## Contact
[eklop@proton.me](mailto:eklop@proton.me)
