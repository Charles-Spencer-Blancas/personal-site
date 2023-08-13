import os
import sys
import shutil
import pypandoc

def generate_blog_card(frontmatter, filename):
    return f'<a href="./{filename}.html"><div id="{filename}" class="nav-card"><h1 class="blog-title">{frontmatter["title"]}</h1><p>{frontmatter["date"]}</p></div></a>\n'

if os.path.isdir('build'):
    shutil.rmtree('build')
shutil.copytree('src', 'build')

blog_index = open('build/notes-to-self/index.html', 'a')

for fullname in os.listdir('content/notes-to-self'):
    (name, extension) = fullname.split('.', 1)

    if extension != 'md':
        continue

    fullpath = f'content/notes-to-self/{fullname}'
    
    file = open(fullpath, 'r')

    line = file.readline()
    if line != '---\n':
        print('Error: Frontmatter does not start with ---\\n', file=sys.stderr)
        exit(1)

    information = {}
    while True:
        line = file.readline()
        if line == '---\n':
            break

        (key, value) = line.split(': ', 1)
        information[key] = value.split('\n')[0]
    
    blog_index.write(generate_blog_card(information, name))

    pypandoc.convert_file(fullpath, 
                          'html', 
                          outputfile = f'build/notes-to-self/{name}.html',
                          extra_args = ['--standalone', '--template=templates/notes-to-self.html'])
    
blog_index.write('</div></div></body></html>\n<!-- DO NOT EDIT THIS FILE, THIS WAS GENERATED BY main.py -->')