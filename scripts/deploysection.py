import os
import sys
from datetime import datetime
from labels import format_label
from pathlib import Path
from string import Template

def deploy_section(section):
    datemodified = datetime.now().isoformat()
    current_year = datetime.now().year
    home_dir = Path.home()
    script_dir = Path(__file__).parent.resolve()
    relative = script_dir.relative_to(home_dir)
    proj_dir = str(home_dir) + '/' + str(relative.parts[0])
    file = open(proj_dir + '/txt/' + section + '/index.org', 'r')
    section_index = file.readlines()
    section_path = section.split('/')
    head_title = format_label(section_path[0])    
    page_title = ''
    path_so_far = '/'
    
    for folder in section_path:
        folder_formatted = format_label(folder)
        if folder != section_path[0]:
            head_title += ' &gt; ' + folder_formatted
        if folder == section_path[-1]:
            page_title += ' &gt; ' + folder_formatted
        else:
            page_title += ' &gt; ' + '<a href="' + path_so_far + folder + '/">' + folder_formatted + '</a>'
        path_so_far += folder + '/'
        
    content = '<ul>\n'
    for i in range(len(section_index)):
        if section_index[i].startswith("* "):
            link_title = section_index[i].removeprefix("* ").strip()
            link_summary = section_index[i+1].removeprefix("** ").strip()
            link_path = section_index[i+2].removeprefix("** ").strip()
            if link_path.endswith("/"):
                link_url = f'/{section}/' + link_path
            else:
                link_url = f'/{section}/' + link_path + '.html'                
            content += f'        <li><a href="{link_url}"><h2>{link_title}</h2><p>{link_summary}</p></a></li>\n'
        elif section_index[i].startswith("#+DESCRIPTION: "):
            description = section_index[i].removeprefix("#+DESCRIPTION: ").strip()
    content += '      </ul>';

    with open(proj_dir + '/templates/section.html', 'r') as f:
        template_content = f.read()

    template = Template(template_content)
    result = template.substitute(content=content, datemodified=datemodified, description=description, head_title=head_title, page_title=page_title, current_year=current_year)

    if not os.path.exists(proj_dir + '/docs/' + section):
        os.makedirs(proj_dir + '/docs/' + section)        
    with open(proj_dir + '/docs/' + section + '/index.html', 'w') as f:
        f.write(result)

my_section = sys.argv[1]        
deploy_section(my_section)
        
