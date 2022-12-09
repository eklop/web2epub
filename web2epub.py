import re
from requests import get
from sys import argv as cla
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

def main():
	if not cla[1]:
		raise Exception("Invalid argument..")
	if len(cla) != 2:
		raise Exception("This script expects just one parameter.. Did you comma separate the URL's")

	links = str(cla[1]).split(',')

	for l in links:
		if not valid_url(l):
			raise Exception(str("This is not a valid url: "+l))

	book = epub.EpubBook()
	book.set_language('en')
	chapters = ['nav']
	epub_title = ""
	epub_author = ""
	toc = []

	if len(links) > 1:
		print("You're trying to download {0} links. Please provide title and author.".format(len(links)))
		epub_title = input("ePub title: ")
		epub_author = input("ePub author: ")
	for idx, link in enumerate(links):
		try:
			request = get(link)
			if bool(request.text) == False:
				if input('Do you want to skip this URL and continue? [y/n]') == 'y':
					continue
				else:
					print('Script stopped')
					sys.exit(0)
			else:
				print('Extracting content from page..')
				page_content = simple_json_from_html_string(request.text, use_readability=False)

				chapter_content = page_content['plain_content']

				if not epub_title:
					epub_title = page_content['title']

				if not epub_author:
					epub_author = page_content['byline'] if page_content['byline'] else "Various authors"

				print('Adding content to ePub..')
				chapter = epub.EpubHtml(title=page_content['title'], file_name=str('chapter{}.xhtml'.format(idx+1)), lang='en')
				chapter.content = u'{}'.format(chapter_content)
				book.add_item(chapter)
				chapters.append(chapter)
			pass
		except Exception as e:
			raise e

	print("Finishing epub..")
	
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
		print("Done! Saved to {}.epub".format(slug))
	except Exception as e:
		raise e

if __name__ == "__main__":
	main()