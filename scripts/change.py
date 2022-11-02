#!/usr/bin/env python

# Felipe Torres Fabregas
# Created on 10/22/2017: Felipe
# This file takes the "lcp_references.html" generated by Ken Pierce
# and re-arranges it to a page with a sidebar of all years.

import datetime
from re import sub, DOTALL
import os


def get_years(current_year, start_year=2003):
    """
    Return a list of years from the current year to the start year.
    """
    years = {'ALL': ''}

    for item in reversed(range(2003, current_year + 1)):
        years[item] = ""

    return years


def get_recent_pubs(current_year, years):
    """
    Return a list of the most recent publications
    """
    recent = []

    if(years[current_year]):
        for item in years[current_year].split('<dd>'):
            if "http" in item.split("</a>")[0].split('<a')[1]:
                recent.append("<li><a" + item.split("</a>")[0].split('<a')[1] + "</a></li>")
        if len(years[current_year].split('<dd>')) < 5:
            for item in years[current_year-1].split('<dd>'):
                if "http" in item.split("</a>")[0].split('<a')[1]:
                    recent.append("<li><a" + item.split("</a>")[0].split('<a')[1] + "</a></li>")
    else:
        for item in years[current_year-1].split('<dd>'):
            if "http" in item.split("</a>")[0].split('<a')[1]:
                recent.append("<li><a" + item.split("</a>")[0].split('<a')[1] + "</a></li>")
        if len(years[current_year-1].split('<dd>')) < 5:
            for item in years[current_year-2].split('<dd>'):
                if "http" in item.split("</a>")[0].split('<a')[1]:
                    recent.append("<li><a" + item.split("</a>")[0].split('<a')[1] + "</a></li>")

    return recent

def get_header_template(head, side_tab, content):
    """
    Get content for the HTML header.
    """
    header_html = """
    {% set active_page = "Publications" %}
    {% extends "base.html" %}
    {% block title %}Laboratory for Computational Physiology{% endblock %}
    {% block head2 %}
    <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='css/publications.css') }}">
    <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='css/references.css') }}">
    {% endblock %}
    {% block content %}"""

    header_html += """
    <a id="skip_content"></a>
    <div class="container">
        <div class="row">
            <div class="col-md-12 col-sm-12 col-xs-12">
                <div class="text-left">
                    <h3 class="site-section-title">Publications</h3>
                </div>
            </div>
        </div>
        <div class='row'>
            <div class="col-md-12">
                %s
            </div>
        </div>
        <div class='row'>
            <div class="col-md-1 tabs-left">
            <ul class="nav nav-tabs" id="Publications" role="tablist">%s</ul>
            </div>
            <div class="col-md-10">
            <div class="tab-content">%s""" % (head, side_tab, content)

    return header_html


def get_footer_template():
    """
    Get content for the HTML header.
    """
    footer_html = """</div></div>
        </div>
    </div>
    <br>
    {% endblock %}
    """
    return footer_html

def split_content(content):
    """
    Splits content into X.
    """
    content_list = sub(r"<!--(.|\s|\n)*?-->", "", content, flags=DOTALL).split("""<ol compact="1" class="bib2xhtml">""")
    return content_list

def get_section_tags():
    """
    Get the tags for each section.
    """
    section_tags = {}
    section_tags['journal'] = """\n<a name="journal"></a><h3>Journal articles</h3>\n</ol>\n\n\n"""
    section_tags['conference'] = """\n<a name="conferences"></a><h3>Conference proceedings and presentations</h3>\n</ol>\n\n"""
    section_tags['book'] = """\n<a name="books"></a><h3>Books and book chapters</h3>\n</ol>\n\n"""
    section_tags['thesis'] = """\n<a name="theses"></a><h3>Theses</h3>\n</ol>\n\n"""

    return section_tags

def file_change(File_Content):
    """
    This function is designed to take the file that Ken generates for the publications,
    and re-arrange it to show the publications by year.
    """

    current_year = datetime.datetime.now().year
    years = get_years(current_year, 2003)

    File_Content = split_content(File_Content)

    Size = len(File_Content)
    Header = File_Content[0] # We take the header, and we sicard it.

    section_tags = get_section_tags()

    # Here we find where the stirngs above are located. 
    Journal_idx = File_Content.index(section_tags['journal']) #1
    Conferences_idx = File_Content.index(section_tags['conference']) #16
    Books_idx = File_Content.index(section_tags['book']) #31
    Theses_idx = File_Content.index(section_tags['thesis']) #38
    All = {'journal': {}, 'conferences': {}, 'books': {}, 'theses': {}}

    # Here we iterate throughout all four elements of the file. 
    # We keep a copy of the current row, each row is a journal or conference or book, depends on what for loop you are in.
    # Since there are two places the year is located at, we have to try and search for it.
    # The output of the try except, will be (2016 16</ OR ">20 2015), since we use that variable to set the year, we need a try except to see if the item is a intiger or a string.
    # We remove all newlines because they don't work on html, set the ID of the journal, conference... and we remove the commented data, just to try and clean out the code.
    # If the year wasn't found, then there was a change in the perl creation script, and now we have to check what happened and where is the year.

    for row in range(Journal_idx + 1, Conferences_idx):
        if File_Content[row][20:24].isdigit():
            section_tags['journal'] = section_tags['journal'].replace("\r","").replace("\n","").replace("</dl>","")
            years[int(File_Content[row][20:24])] += section_tags['journal'].replace("journal", "journal"+File_Content[row][20:24]) + File_Content[row][File_Content[row].index('</dl>')+5:]
            All['journal'][int(File_Content[row][20:24])] = section_tags['journal'] + File_Content[row][File_Content[row].index('</ol>')+5:]
        else:
            print(File_Content[row])
            print(File_Content[row][20:24])
            print ("We could not find the year, the variables are not int. Check the HTML file.", row, "\n\n")

    for row in range(Conferences_idx + 1, Books_idx):
        if File_Content[row][20:24].isdigit():
            section_tags['conference'] = section_tags['conference'].replace("\r","").replace("\n","").replace("</dl>","")
            years[int(File_Content[row][20:24])] += section_tags['conference'].replace("conferences", "conferences"+File_Content[row][20:24]) + File_Content[row][File_Content[row].index('</dl>')+5:]
            All['conferences'][int(File_Content[row][20:24])] = section_tags['conference'] + File_Content[row][File_Content[row].index('</dl>')+5:]
        else:
            print ("We could not find the year, the variables are not int. Check the HTML file.", row, "\n\n")

    for row in range(Books_idx + 1, Theses_idx):
        if File_Content[row][20:24].isdigit():
            section_tags['book'] = section_tags['book'].replace("\r","").replace("\n","").replace("</dl>","")
            years[int(File_Content[row][20:24])] += section_tags['book'].replace("books", "books"+File_Content[row][20:24]) + File_Content[row][File_Content[row].index('</dl>')+5:]
            All['books'][int(File_Content[row][20:24])] = section_tags['book'] + File_Content[row][File_Content[row].index('</dl>')+5:]
        else:
            print ("We could not find the year, the variables are not int. Check the HTML file.", row, "\n\n")

    for row in range(Theses_idx + 1, Size):
        if File_Content[row][20:24].isdigit():
            section_tags['thesis'] = section_tags['thesis'].replace("\r","").replace("\n","").replace("</dl>","")
            years[int(File_Content[row][20:24])] += section_tags['thesis'].replace("theses","theses"+File_Content[row][20:24]) + File_Content[row][File_Content[row].index('</dl>')+5:]
            All['theses'][int(File_Content[row][20:24])] = section_tags['thesis'] + File_Content[row][File_Content[row].index('</dl>')+5:]
        else:
            print ("We could not find the year, the variables are not int. Check the HTML file.", row, "\n\n")

    recent = get_recent_pubs(current_year, years)

    temp = ""

    for key in ['journal', 'conferences', 'books', 'theses']:
        if key == 'journal':
            temp += "<h3 id='journalall'>Journal articles</h3>"
        elif key == 'conferences':
            temp += "<h3 id='conferencesall'>Conference proceedings and presentations</h3>"
        elif key == 'books':
            temp += "<h3 id='booksall'>Books and book chapters</h3>"
        elif key == 'theses':
            temp += "<h3 id='thesesall'>Theses</h3>"
        else:
            print ('key', key)
        for item in reversed(range(2003, current_year+1)):
            if item in All[key].keys():
                if key == 'journal':
                    temp += All[key][item].replace('<h3>Journal articles</h3>', '<h4>{0}</h4>'.format(item))
                elif key == 'conferences':
                    temp += All[key][item].replace('<h3>Conference proceedings and presentations</h3>', '<h4>{0}</h4>'.format(item))
                elif key == 'books':
                    temp += All[key][item].replace('<h3>Books and book chapters</h3>', '<h4>{0}</h4>'.format(item))
                elif key == 'theses':
                    temp += All[key][item].replace('<h3>Theses</h3>', '<h4>{0}</h4>'.format(item))
                else:
                    print ('key', key)

    Head_tag = """<center><a href="#journalall">Journal articles</a> | <a href="#conferencesall">Conference    presentations</a> | 
    <a href="#booksall">Books and book chapters</a> | <a href="#thesesall">Theses</a></center><br>"""
    content    = """<div id="ALL" class="container tab-pane fade">{0}{1}</div>\n""".format(Head_tag, temp)

    # Setting the content of the years
    for key, value in years.items():
        Head_tag = """<center><a href="#journal{}">Journal articles</a> | <a href="#conferences{}">Conference    presentations</a> | 
        <a href="#books{}">Books and book chapters</a> | <a href="#theses{}">Theses</a></center><br>""".format(key, key, key, key)
        if key == current_year:
            if years[current_year] != "":
                content += """<div id="P_{0}" class="container tab-pane active">{1}{2}</div>\n""".format(key, Head_tag, value)
            else:
                content += """<div id="P_{0}" class="container tab-pane fade">{1}{2}</div>\n""".format(key, Head_tag, value)
        elif key == 'ALL':
            pass
            # content += """<div id="%s" class="tab-pane fade">%s%sUnder development</div>\n""" % (key, Head_tag, value)
        else:
            if years[current_year] == "" and key == current_year -1:
                content += """<div id="P_{0}" class="container tab-pane active">{1}{2}</div>\n""".format(key, Head_tag, value)
            else:
                content += """<div id="P_{0}" class="container tab-pane fade">{1}{2}</div>\n""".format(key, Head_tag, value)
                # content += """<div id="%s" class="tab-pane fade">%s%sUnder development</div>\n""" % (key, Head_tag, value)

    # Setting the sidebar with the years
    side_tab = """<li class="nav-item"><a class="nav-link" data-toggle="tab" id="ALL_tab" href="#ALL">All</a></li>"""
    for item in reversed(range(2003, current_year+1)):
        if item == current_year:
            if years[current_year] != "":
                side_tab += """<li class="nav-item"><a class="nav-link active" data-toggle="tab" id="{}_tab" href="#P_{}">{}</a></li>\n""".format(item, item, item)
            else:
                side_tab += """<li class="nav-item"><a class="nav-link btn disabled" data-toggle="tab" id="{}_tab" href="#P_{}">{}</a></li>\n""".format(item, item, item)
        else:
            if years[current_year] == "" and item == current_year -1:
                side_tab += """<li class="nav-item"><a class="nav-link active" data-toggle="tab" id="{}_tab" href="#P_{}">{}</a></li>\n""".format(item, item, item)
            else:
                side_tab += """<li class="nav-item"><a class="nav-link" data-toggle="tab" id="{}_tab" href="#P_{}">{}</a></li>\n""".format(item, item, item)

    # Head = "<center>"+ File_Content[0].replace("""| <a href="#theses">Theses</a>""", """<!--| <a href="#theses">Theses</a>-->""") + "</center><br>"
    File_Content[0] = File_Content[0].replace("""\n\n<p>\n(A separate listing of PhysioNet tutorials is available at <a href="http://physionet.org/tutorials/" target="_blank" >http://physionet.org/tutorials/</a>.)\n</p>\n\n""","").replace("\r","").replace("\n","").replace("<br>","").replace("< br>","").replace("<br >","").replace("<br />","").replace("""<a href="#journal">Journal articles</a> | <a href="#conferences">Conference    presentations</a> | <a href="#books">Books and book chapters</a> | <a href="#theses">Theses</a>""","")

    head = str(File_Content[0])
    header_html = get_header_template(head, side_tab, content)
    footer_html = get_footer_template()

    return recent, header_html + footer_html

def main():

    # Here will be the shasum and the content of the newly edited publications
    CHANGE_FILE = os.path.join('..', 'sitedata', 'lcp_references.html')
    NEW_PUB = os.path.join('..', 'templates', 'publications.html')
    RECENT_PUB = os.path.join('..', 'templates', 'recent_publications.html')

    # Read the file used to update the publications
    Edited_File    = open(CHANGE_FILE, 'rb').read()
    # Return the converted file separated by most recent publications and content
    Recent, Content = file_change(Edited_File.decode('UTF-8'))

    # Write the new content to the publications template
    New_File = open(NEW_PUB, "w").write(Content)

    # Update the most recent publications
    Recent_File = open(RECENT_PUB, "w")
    for indx, item in enumerate(Recent):
        if indx < 4:
            Recent_File.write(item)
    Recent_File.close()

    print ("CHANGE DONE")

if __name__ == '__main__':
    main()
