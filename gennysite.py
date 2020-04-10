import markdown
import os

def get_html(filename, md=None):
    text = None
    with open(filename) as infile:
        text = infile.read()
    if md is None:
        return markdown.markdown(text)
    else:
        return md.convert(text)

def get_article(filename, md=None):
    html = get_html(filename, md)
    html = f"<article class=\"content box\">\n{html}\n</article>"
    print(f"Got html from article {filename}")
    return html

def insert_content(pagehtml, content):
    pagehtml.insert(pagehtml.index("<main>")+1, content)

def get_master_template():
    masterhtml = None
    with open("templates/master.html") as masterfile:
        masterhtml = masterfile.readlines()
    masterhtml = [line.strip() for line in masterhtml]
    print("Got master template")
    return masterhtml

def write_html(html, filename):
    with open(filename, "w") as f:
        for line in html:
            f.write(f"{line}\n")
    print(f"Wrote {filename}")

def get_files_with_extension(directory, extension):
    files = os.listdir(directory)
    return [f for f in files if f.split(".")[-1] == extension]

   
md = markdown.Markdown()

### homepage / blog ###
postfiles = get_files_with_extension("posts_raw", "md")

pagehtml = get_master_template()

for postfile in reversed(postfiles):
    article_html = get_article(f"posts_raw/{postfile}", md)
    insert_content(pagehtml, article_html)

write_html(pagehtml, "index.html")

### other pages ###
for pagesfile in get_files_with_extension("pages", "html"):
    pagehtml = get_master_template()
    html = None
    with open(f"pages/{pagesfile}") as infile:
        html = infile.read()
    insert_content(pagehtml, html)
    write_html(pagehtml, pagesfile)
