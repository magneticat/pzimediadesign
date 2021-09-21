#! /usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import html5lib, urllib, pprint, re
from mmdc_modules import pandoc2html, parse_work, write_html_file, mw_cats, mw_page_imgsurl, mw_img_url, mw_page_text, mwsite, mw_page_cats, mw_page, remove_cats, find_authors, replace_video, replace_img_a_tag, index_addwork, years, vimeo_exp
from argparse import ArgumentParser
from random import shuffle
###### REQUIRES #####
# * webserver: to server web/ folder
#
### WORKINGS ####
# * years are create by var years = range(2015, (datetime.now()).year+1) in mmdc_moudles.py

# * each year has its own html template in YYYY-template.html
# * the --category provides the year. I.e. 2017
# * year does not need to be indicated in arguments
#
# * work pages generation uses: work-YYYY-template.html
# * graduation year index pages generation uses: index-template-YYYY.html
#
#
################

######
# user_args
####
parser = ArgumentParser()
parser.add_argument("--host", default="pzwiki.wdka.nl")
parser.add_argument("--path", default="/mw-mediadesign/", help="nb: should end with /")
parser.add_argument("--category", "-c", nargs="*",  help="category to query, use -c foo bar to intersect multiple categories")
parser.add_argument("--preview", help='Preview page. Will override category querying. Use: --page "Name Of Wiki Page"')

user_args = parser.parse_args()
print 'user_args', user_args

######
# DEFS:  create_pages create_index
######

test_exp=re.compile('\{\{\#widget\:Vimeo\|id\=(.*?)\}\}')


def create_pages(memberpages, mode):
    indexdict = {} #parent dict: contains articledict instances
    for member in memberpages:
        page = mw_page(site, member)
        page_text = mw_page_text(site, page)
        # import pdb; pdb.set_trace()
        articledict = parse_work(site, member, page_text) # create dictionary
        # Title, Creator, Date, Website, Thumbnail, Bio, Description, Extra
        if len(articledict['Creator'])>0 and len(articledict['Title'])>0  and len(articledict['Thumbnail'])>0:

            for key in articledict.keys():
                print key

                if key in ['Extra', 'Description', 'Bio']:
                    print '3 keys'
                    articledict[key] =  pandoc2html(articledict[key])
                elif key is 'Creator':
                   print 'creator'
                   articledict[key] =  articledict[key].replace(',','' )

                if key is 'Extra':
                    print 'extra', type( articledict['Extra'])
                    articledict[key] = remove_cats(articledict['Extra'])
                    articledict[key] = replace_video(articledict['Extra'])  
#                    found = re.findall(vimeo_exp, articledict['Extra'])
#                    print 'FOUND:', found
                     

            pprint.pprint( articledict)
          
            articledict['Imgs'] = mw_page_imgsurl(site, page, articledict['Thumbnail'] )
            
        year = articledict['Date']
        page_template = open("./work-{}-template.html".format(year), "r") # a template for each year            
        page_tree = html5lib.parse(page_template, namespaceHTMLElements=False)
        page_title = page_tree.find('.//title')
        page_title.text=articledict['Title']#.decode('utf-8')
        page_creator = page_tree.find('.//h2[@id="creator"]')
        page_creator.text=(articledict['Creator'])
        page_title_date = page_tree.find('.//p[@id="title"]')
        page_title_date.text=u"{} {}".format(articledict['Title'], articledict['Date'])
        page_description = page_tree.find('.//div[@id="description"]')
        page_description_el = ET.fromstring('<div>'+articledict['Description'].encode('utf-8')+'</div>')
        page_description.extend(page_description_el)
        page_bio = page_tree.find('.//div[@id="bio"]')
        page_bio_el = ET.fromstring('<div>'+articledict['Bio'].encode('utf-8')+'</div>')
        page_bio.extend(page_bio_el)
        page_sortArea_title = page_tree.find('.//div[@id="sortArea"]/p')
        page_sortArea_title.text =articledict['Title'] 
        page_extra = page_tree.find('.//div[@id="extra"]')
        page_extra_el = ET.fromstring('<div>'+articledict['Extra'].encode('utf-8')+'</div>')
        page_extra.extend(page_extra_el)
        page_website = page_tree.find('.//p[@class="hightlightSidebar"]/a')
        page_website.set('href', articledict['Website'])
        page_website.text=articledict['Website']        
        page_thumb = page_tree.find('.//img[@id="thumbnail"]')
        page_thumb.set('src', articledict['Thumbnail'])
        #print
        #print ET.tostring(page_tree)
        #print
        figures = page_tree.findall('.//figure')
        images = page_tree.findall('.//img')

        if len(figures) > 0:
            for figure in figures:
                img = figure.find('.//img')            
                figcaption = figure.find('.//figcaption')
                img_src = img.get('src')
                #print img_src
                figcaption_text = figcaption.text
                if figcaption_text == img_src:# remove figcation if ==  src
                    figure.remove(figcaption)                 

                src = (('File:'+img_src).capitalize()).decode('utf-8')
                if src in articledict['Imgs'].keys(): #full-url
                    url = (articledict['Imgs'][src])
                    #print url
                    img.set('src', url)
        else:
            for img in images:
                img_src = img.get('src')
                #print img_src
                src = (('File:'+img_src).capitalize()).decode('utf-8')
                #pprint.pprint(articledict)
                if src in articledict['Imgs'].keys(): #full-url
                    url = (articledict['Imgs'][src])
                    #print url
                    img.set('src', url)
                    #print ET.tostring(img)
                    img.set('title', (img.get('title').replace('fig:','')) )
        # save work page
        creator = articledict['Creator'].encode('ascii', 'ignore')
        creator = creator.replace(' ','_')
        work_filename = 'web/works/{}-{}.html'.format(year, creator)
        write_html_file(page_tree, work_filename)
        articledict['Path'] = work_filename[4:]
        indexdict[articledict['Title']] = articledict                    
    return indexdict
        

def create_index(indexdict, year):
    index_template = open("./index-template-{}.html".format(year), "r") 
    index_tree = html5lib.parse(index_template, namespaceHTMLElements=False)
    index_container = index_tree.find(".//div[@class='isotope']") #maybe id is imp    
    works = indexdict.keys()

    #print '\n\n******* indexdict keys: works ***********\n\n'
    #print(works)

    for work in works:
        index_addwork( parent=index_container,
                       workid=work,
                       href=indexdict[work]['Path'],
                       title=indexdict[work]['Title'],#.decode('utf-8'),
                       creator=indexdict[work]['Creator'],
                       date=indexdict[work]['Date'],                                         
                       thumbnail=(indexdict[work]['Thumbnail'])
        )
        
    #print '----', indexdict[key]['Title'],indexdict[key]['Path']
    indexfile_year = './web/{}.html'.format(year)
    write_html_file(index_tree, indexfile_year)

    years.sort()
    if year == years[-1]:  # last year works --> index.html
        indexfile = './web/index.html'    
        write_html_file(index_tree, indexfile)






#####
# ACTION
#####    
site = mwsite(user_args.host, user_args.path)
if user_args.preview:
    memberpages=[unicode(user_args.preview)]
else:    
    memberpages=mw_cats(site, user_args)
#    print '\n\nmemberpages:\n\n', memberpages, '\n\n********\n\n' # memberpages include years, from current to 2015

    indexdict = create_pages(memberpages, 'index')
    indexdict_byyear={year:{} for year in years } # index of all page organized according to year
    # indexdict_byyear structure:
    # {year1:{ work1: {work1 prop:vals}, work2: {...} }, year2:..., year3: }
    # {2015: {u'A Unique Line': {'Bio': ...}}}

    for key in indexdict.keys(): # populate indexdict_byyear with works
        indexdict_byyear[ int(indexdict[key]['Date'])][key] = indexdict[key]

    #print '\n\n******* indexdict_byyear ***********\n\n'
    #pprint.pprint( indexdict_byyear )    

    for year in indexdict_byyear.keys(): # create index page for each year ie 2016.html
        print '\n***** ', year, ' *****\n'
        create_index(indexdict_byyear[year], year)

