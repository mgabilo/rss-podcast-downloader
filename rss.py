from rss_parser import Parser
import requests
import pdb
import shutil
import pdb
import os
import unicodedata
import string

valid_filename_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
char_limit = 255

def clean_filename(filename, whitelist=valid_filename_chars, replace=' :'):
    # replace spaces
    for r in replace:
        filename = filename.replace(r,'_')

    # keep only valid ascii chars
    cleaned_filename = unicodedata.normalize('NFKD', filename).encode('ASCII', 'ignore').decode()

    # keep only whitelisted chars
    cleaned_filename = ''.join(c for c in cleaned_filename if c in whitelist)
    if len(cleaned_filename)>char_limit:
        print("Warning, filename truncated because it was over {}. Filenames may no longer be unique".format(char_limit))
    return cleaned_filename[:char_limit]



def download_feed(url):
    feed_content = requests.get(url)
    parser = Parser(xml=feed_content.content)
    feed = parser.parse()


    # Print out feed meta data
    print(feed.title)
    dirname = clean_filename(feed.title.strip())
    os.makedirs(dirname, exist_ok=True)

    # Iteratively print feed items
    for item in feed.feed:
        print(clean_filename(item.title), item.enclosure_url)
        ext = os.path.splitext(item.enclosure_url.rpartition('/')[-1].partition('?')[0])[-1]
        filename = os.path.join(dirname, clean_filename(item.title) + ext)
        if os.path.exists(filename):
            print ('EXISTS, SKIPPING: --->', filename)
            continue

        print ('--->', filename)
        if not item.enclosure_url:
            print ("******* URL NOT FOUND")
            continue
        response = requests.get(item.enclosure_url, stream=True)

        with open(filename, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)

if __name__ == "__main__":
    for feed_url in open('rss_list.txt').read().splitlines():
        download_feed(feed_url)
