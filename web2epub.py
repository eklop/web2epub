import re
import argparse
import sys
import logging
from requests import get
from readabilipy import simple_json_from_html_string
from ebooklib import epub

def valid_url(url):
	regex = re.compile(
        r'^(?:http)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
	return re.match(regex, str(url)) is not None

def slugify(s):
	s = s.lower().strip()
	s = ''.join(char for char in s if ord(char) < 128) #remove non-ascii characters
	s = re.sub(r'[^\w\s-]', '', s)
	s = re.sub(r'[\s_-]+', '-', s)
	s = re.sub(r'^-+|-+$', '', s)
	return s

def parse_urls_from_string(url_string):
	"""Parse URLs from a comma-separated string and validate them."""
	links = str(url_string).split(',')
	
	for link in links:
		link = link.strip()  # Remove whitespace
		if not valid_url(link):
			raise Exception("This is not a valid url: " + link)
	
	return links

def parse_urls_from_file(file_path):
	"""Read URLs from a file, one URL per line."""
	try:
		with open(file_path, 'r') as f:
			links = []
			for line in f:
				line = line.strip()
				if line and not line.startswith('#'):  # Skip empty lines and comments
					if not valid_url(line):
						raise Exception("This is not a valid url: " + line)
					links.append(line)
			return links
	except FileNotFoundError:
		raise Exception(f"File not found: {file_path}")
	except Exception as e:
		raise Exception(f"Error reading file {file_path}: {str(e)}")

def main():
	# Set up argument parser
	parser = argparse.ArgumentParser(
		prog='web2epub',
		description='Convert web pages to EPUB format using readability algorithms',
		epilog='''
Examples:
  # Convert a single webpage (backward compatible)
  python web2epub.py https://example.com/article

  # Convert multiple webpages with comma separation
  python web2epub.py https://example.com/page1,https://example.com/page2

  # Use --url option for single or multiple URLs
  python web2epub.py --url https://example.com/article
  python web2epub.py -u "https://example.com/page1,https://example.com/page2"

  # Read URLs from a file
  python web2epub.py --file urls.txt
  python web2epub.py -f urls.txt

  # Specify title and author via command line
  python web2epub.py --url https://example.com/article --title "My Article" --author "John Doe"
  python web2epub.py -f urls.txt -t "My Collection" -a "Various Authors"

  # Enable verbose logging
  python web2epub.py --url https://example.com/article --verbose

File format for --file option:
  - One URL per line
  - Lines starting with # are treated as comments
  - Empty lines are ignored
  - Example urls.txt:
    # My reading list
    https://example.com/article1
    https://example.com/article2
    # Another article
    https://example.com/article3

Notes:
  - For multiple URLs without --title/--author, you'll be prompted to provide a title and author
  - The script extracts content using readability algorithms
  - Output EPUB files are named based on the title (slugified)
  - Title and author can be specified via --title/-t and --author/-a arguments
		''',
		formatter_class=argparse.RawDescriptionHelpFormatter
	)
	parser.add_argument('--url', '-u', 
		help='URL or comma-separated URLs to convert to EPUB format')
	parser.add_argument('--file', '-f', 
		help='File containing URLs to convert (one URL per line, supports comments with #)')
	parser.add_argument('--title', '-t', 
		help='Title for the EPUB file (if not provided, will be extracted from first page or prompted)')
	parser.add_argument('--author', '-a', 
		help='Author for the EPUB file (if not provided, will be extracted from first page or prompted)')
	parser.add_argument('urls', nargs='*', 
		help='URLs as positional arguments (for backward compatibility)')
	parser.add_argument('--verbose', action='store_true', help='Enable verbose logging output')
	parser.add_argument('--version', action='version', version='web2epub 1.0.0')
	
	args = parser.parse_args()
	
	# Set up logging
	logging.basicConfig(level=logging.INFO if args.verbose else logging.WARNING, 
	                   format='%(message)s')
	logger = logging.getLogger(__name__)
	
	# If no arguments provided, show help
	if not args.url and not args.file and not args.urls:
		parser.print_help()
		return
	
	# Determine how to get URLs
	links = []
	
	if args.url and args.file:
		raise Exception("--url and --file are mutually exclusive. Please use only one.")
	
	if args.url:
		# Use --url argument
		links = parse_urls_from_string(args.url)
	elif args.file:
		# Use --file argument
		links = parse_urls_from_file(args.file)
	elif args.urls:
		# Backward compatibility: use positional arguments
		if len(args.urls) == 1:
			# Single argument might be comma-separated URLs
			links = parse_urls_from_string(args.urls[0])
		else:
			# Multiple arguments, treat each as a URL
			for url in args.urls:
				if not valid_url(url):
					raise Exception("This is not a valid url: " + url)
			links = args.urls

	book = epub.EpubBook()
	book.set_language('en')
	chapters = ['nav']
	epub_title = args.title if args.title else ""
	epub_author = args.author if args.author else ""
	toc = []

	# If title/author not provided via command line and multiple URLs, prompt user
	if len(links) > 1 and not epub_title:
		print(f"You're trying to download {len(links)} links. Please provide title and author.")
		if not epub_title:
			epub_title = input("ePub title: ")
		if not epub_author:
			epub_author = input("ePub author: ")
	
	print(f"Starting download of {len(links)} URL(s)...")
	for idx, link in enumerate(links):
		try:
			logger.info('Fetching URL %d/%d: %s', idx+1, len(links), link)
			request = get(link, timeout=5)
			if bool(request.text) == False:
				logger.warning('Empty response from %s', link)
				if input('Do you want to skip this URL and continue? [y/n]') == 'y':
					continue
				else:
					print('Script stopped')
					sys.exit(0)
			else:
				logger.info('Extracting content from page..')
				page_content = simple_json_from_html_string(request.text, use_readability=True)

				chapter_content = page_content['plain_content']
				chapter_content = f"<h1>{page_content['title']}</h1>{chapter_content}"

				if not epub_title:
					epub_title = page_content['title']

				if not epub_author:
					epub_author = page_content['byline'] if page_content['byline'] else "Various authors"

				logger.info('Adding content to ePub..')

				chapter = epub.EpubHtml(
        			title=page_content['title'], 
           			file_name=str('chapter{}.xhtml'.format(idx+1)), 
              		lang='en')

				chapter.content = u'{}'.format(chapter_content)
				book.add_item(chapter)
				chapters.append(chapter)
		except Exception as e:
			logger.error('Error fetching %s: %s', link, str(e))
			logger.info('Skipping URL %d/%d and continuing...', idx+1, len(links))
			continue

	logger.info("Finishing epub..")
	
	slug = slugify(epub_title)
	
	book.set_identifier(slug)
	book.set_title(epub_title)
	book.add_item(epub.EpubNcx())
	book.add_item(epub.EpubNav())

	book.spine = chapters
	
	if epub_author:
		book.add_author(epub_author)
	else:
		book.add_author("Unknown Author")

	try:
		epub.write_epub('{}.epub'.format(slug), book, {})
		print(f"Finished! Compiled book saved to {slug}.epub")
	except Exception as e:
		raise e

if __name__ == "__main__":
	main()