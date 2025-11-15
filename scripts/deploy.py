import os
import re
import sys
from datetime import datetime
from string import Template

if len(sys.argv) < 2:
    print("Usage: python deploy.py <filename>")
    sys.exit(1)

filename = sys.argv[1]

full_path = os.path.dirname(os.path.abspath((filename)))
base_path = full_path.partition("/txt/")[0]
folder = full_path.partition("/txt/")[2]
if base_path.endswith("/txt"):
    base_path = base_path.removesuffix("/txt")

section_path = folder.split('/')
head_title = ''
page_title = ''
path_so_far = '/'

if section_path:
    for subfolder in section_path:
        subfolder_formatted = subfolder.replace("-", " ").title()
        if subfolder != section_path[0]:
            head_title += ' &gt; '
            head_title += subfolder_formatted
            page_title += ' &gt; <a href="' + path_so_far + subfolder + '/">' +    subfolder_formatted + '</a>'
        path_so_far += subfolder + '/'

date, summary, title = None, None, None

with open(filename, 'r') as file:
    for line in file:
        if line.startswith('date: '):
            datecreated = line[len('date: '):].strip()
        elif line.startswith('desc: '):
            description = line[len('desc: '):].strip()
        elif line.startswith('ti: '):
            title = line[len('ti: '):].strip()

datemodified = datetime.now().isoformat()

content_lines = []
recording = False

with open(filename, 'r') as file:
    for line in file:
        if line.startswith('---'):
            recording = True
            continue
        if recording:
            if line.startswith('==='):
                break
            content_lines.append(line.rstrip('\n'))

content = '\n'.join(content_lines)

content = '\n<p>' + re.sub(r'\n{2,}', '</p>\n\n<p>', content.strip()) + '</p>\n'

if(folder.startswith("dreams/")):
    dt = datetime.strptime(datecreated, '%Y-%m-%d')
    content += '<p class="dream-date">' + dt.strftime('%d %B %Y') + '</p>'

with open(base_path + '/templates/webpage.html', 'r') as f:
    template_content = f.read()

template = Template(template_content)

result = template.substitute(content=content, datecreated=datecreated, datemodified=datemodified, description=description, head_title=head_title, page_title=page_title, title=title)

filename = os.path.basename(filename)

if filename.endswith(".txt"):
    outputfile = filename[:-4]
else:
    outputfile = filename

with open(base_path + '/docs/' + folder + '/' + outputfile + '.html', 'w') as f:
    f.write(result)
