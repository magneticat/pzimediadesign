#! /usr/bin/env python
# -*- coding: utf-8 -*-

import pprint, re, subprocess, shlex, urllib
import xml.etree.ElementTree as ET
from mwclient import Site
from datetime import datetime
######
# GLOBAL VARS
######


years = range(2015, (datetime.now()).year+1)

#########
# Site Level
#########
def mwsite(host, path): #returns wiki site object
    site = Site(('http',host), path)
    return site

            

def mw_cats(site, args): #returns pages member of args(categories)
    pages = []
    last_names = None
    #    cats = site.Categories[args.category]#category, 'Graduation_work']
    for category in years:#args.category:
        #print 'cat:', category    
        cat = site.Categories[category]#, 'Graduation_work']
        print 'site cats:', cat, type(cat.members())  
        for i in list(cat.members()):# add members(objects) of cat as list, to pages list
            pages.append(i)
        #print 'pages:', pages
        
        # check whether pages are also part of Category Graduation_work
        
        for p in pages:
            #print 'page:', p, last_names
            #pages_by_name[p.name] = p
            if last_names == None: # what the duck am I doing here w/ last_names??
                results = pages
#    print "\n*** p.name ***\n", [p.name  for p in pages], "\n******\n"            
#    print "\n**p.name in results****\n", [p.name  for p in results], "\n******\n"    
    return [p.name  for p in results]

    

##############################
# CATEGORIES, PAGES AND IMAGES
##############################
def mw_page(site, page):
    page = site.Pages[page]
    return page

def mw_page_text(site, page):
    text = page.text()
    return text

def mw_page_cats(site, page):
    cats_list = list(page.categories())
    cats = [cat.name for cat in cats_list if cat.name != u'Category:04 Publish Me'] 
    return cats


def mw_page_imgsurl(site, page, thumb):
    #all the imgs in a page
    #except thumb: if thumb: remove
    #returns list of tuples (img.name, img.fullurl)
    imgs = page.images()
    imgs = list(imgs)    
    imgs_dict = { img.name:(img.imageinfo)['url'] for img in imgs if  (img.imageinfo)['url'] != thumb } # exclude thumb 
    imgs_dict = { (key.capitalize()).replace(' ','_'):value for key, value in imgs_dict.items()}
    # capilatize image name, so it can be called later
    return imgs_dict


def mw_img_url(site, img): #find full of an img 
    if 'File:' not in img:
        img = 'File:'+img
    img_page=site.Pages[img]
    img_url = (img_page.imageinfo)['url']
    return img_url




# PROCESSING MODULES

def write_html_file(html_tree, filename):
    doctype = "<!DOCTYPE HTML>"
    html = doctype + ET.tostring(html_tree,  method='html', encoding='utf-8', ) 
    edited = open(filename, 'w') #write
    edited.write(html)
    edited.close()

def parse_work(site, title, content):
    workdict = {'Title':title, 'Creator':u'', 'Date':u'', 'Website':u'', 'Thumbnail':u'', 'Bio':u'', 'Description':u'', 'Extra':u''}    

    if re.match(u'\{\{\Graduation work', content):
        template, extra = (re.findall(u'\{\{Graduation work\n(.*?)\}\}(.*)', content, re.DOTALL))[0]
        if extra:
            workdict['Extra'] = extra 
        keyval = re.findall(u'\|(.*?)\=(.*?\n)', template, re.DOTALL) 
        for pair in keyval:
            key = pair[0]
            val = (pair[1]).replace('\n', '')
            if 'Creator' in key:
                val = val.replace(u', ', u'')
            elif 'Thumbnail' in key:
                val = mw_img_url(site, val)#api_thumb_url(val)
            elif 'Website' in key:
                val = urllib.unquote( val)                
            workdict[key]=val
    return workdict

def pandoc2html(mw_content):
    '''convert individual mw sections to html'''
    mw_content = mw_content.encode('utf-8')
    tmpfile = open('./tmp_content.mw', 'w')
    tmpfile.write(mw_content)
    tmpfile.close()
    args_pandoc = shlex.split( 'pandoc -f mediawiki -t html5 tmp_content.mw' )
    pandoc = subprocess.Popen(args_pandoc, stdout=subprocess.PIPE)
    html = pandoc.communicate()[0]
    html = html.decode("utf-8")
    return html

author_exp = re.compile('^Authors?\: ?(.*?)\\n')
cat_exp = re.compile('\[\[Category\:.*?\]\]')
gallery_exp=re.compile('<gallery>(.*?)</gallery>', re.S)
imgfile_exp=re.compile('(File:(.*?)\.(gif|jpg|jpeg|png))')

def find_authors(content):
    authors = re.findall(author_exp, content[0:100]) #search only in 1st lines
    if authors:
        #replace authors in content
        content = re.sub(author_exp, '', content)
        authors = authors[0]        
    else:
        content = content
        authors = None
    return (authors, content) 
    
def remove_cats(content):
    content = re.sub(cat_exp, '', content)
    return content
    print 'NO CATS', content

def replace_gallery(content):
    content = re.sub(imgfile_exp, '[[\g<1>]]', content) #add [[ ]] to File:.*?
    content = re.sub(gallery_exp, '\g<1>', content) #remove gallery wrapper
    return content

video_exp=re.compile('{\{\#widget\:Html5media.*url\=\<a.*\>(.*?)\<\/a\>.*?\}\}')
vimeo_exp=re.compile('\{\{\#widget\:Vimeo\|id\=(.*?)\}\}')
youtube_exp=re.compile('{\{\#widget\:YouTube\|id\=(.*?)\}\}')

def replace_video(content):
    print '*** VIDEO ***'
    content = re.sub(vimeo_exp,"<iframe src='https://player.vimeo.com/video/\g<1>' width='600px' height='450px'> </iframe>", content)
    content = re.sub(youtube_exp, "<iframe src='https://www.youtube.com/embed/\g<1>' width='600px' height='450px'> </iframe>", content)
    content = re.sub(video_exp, "<video controls='controls' src='\g<1>' ></video>", content)

    
    
    return content

img_exp=re.compile('^.*?\.(?:jpg|jpeg|JPG|JPEG|png|gif)')

def replace_img_a_tag(img_anchor):
    # TO DO: remove <a> - requires finding the img_anchor
    href = img_anchor.get('href')
    if re.match(img_exp, href):
        img_anchor.clear()
        figure = ET.SubElement(img_anchor, 'figure')
        img = ET.SubElement(figure, 'img', attrib={'src': href})
#        figcaption = ET.SubElement(figure, 'figcaption')
#        figcaption.text = href



        


# Index Creation
def index_addwork(parent, workid, href, thumbnail, title, creator, date):
    child_div = ET.SubElement(parent, 'div', attrib={'class':'item',
                                                     'id':workid,
                                                     'data-title':title,
                                                     'data-creator':creator,
                                                     'data-date':date})

    grandchild_a = ET.SubElement(child_div, 'a', attrib={'href':href, 'class':'work'})
    if thumbnail is '':
        grandgrandchild_h3 = ET.SubElement(grandchild_a, 'h3', attrib={'class':'work', 'id':'thumbnail_replacement'})
        grandgrandchild_h3.text=title
    else:
        grandgrandchild_img = ET.SubElement(grandchild_a, 'img', attrib={'class':'work', 'src':thumbnail})    
    # need to add css width to div.item
