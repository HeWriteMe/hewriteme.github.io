import os
import sys
from datetime import datetime
from pathlib import Path
from string import Template

def deploy_index():
    datemodified = datetime.now().isoformat()
    current_year = datetime.now().year
    home_dir = Path.home()
    script_dir = Path(__file__).parent.resolve()
    relative = script_dir.relative_to(home_dir)
    proj_dir = str(home_dir) + '/' + str(relative.parts[0])
    file = open(proj_dir + '/txt/index.org', 'r')    
    section_index = file.readlines()    
    content = '<ul>\n'
    for i in range(len(section_index)):
        if section_index[i].startswith("* "):
            link_title = section_index[i].removeprefix("* ").strip()
            link_summary = section_index[i+1].removeprefix("** ").strip()
            link_path = section_index[i+2].removeprefix("** ").strip()
            if link_path.endswith("html"):
                link_url = '/' + section_index[i+2].removeprefix("** ").strip()                                
            else:
                link_url = '/' + section_index[i+2].removeprefix("** ").strip() + '/'
            content += f'        <li><a href="{link_url}"><h2>{link_title}</h2><p>{link_summary}</p></a></li>\n'
        elif section_index[i].startswith("#+DESCRIPTION: "):
            description = section_index[i].removeprefix("#+DESCRIPTION: ").strip()
    content += '      </ul>';

    with open(proj_dir + '/templates/index.html', 'r') as f:        
        template_content = f.read()

    template = Template(template_content)
    result = template.substitute(content=content, current_year=current_year, datemodified=datemodified, description=description)

    with open(proj_dir + '/docs/index.html', 'w') as f:
        f.write(result)

deploy_index()
        
