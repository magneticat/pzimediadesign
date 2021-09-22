# MMD&C Graduation Website CMS: from Mediawiki to HTML
Code "inherited" from Javi and acastro at https://git.xpub.nl/acastro/pzimediadesign

## Depencies
* python **2.7**
* Pandoc
* Python libraries: html5lib,  mwclient, 

## Run
Update the website with graduation from work from a particular year, by running:
`python mmdc_wiki2web.py --category Graduation_work 2015`

Or index all the gaduation works:
`python mmdc_wiki2web.py --category Graduation_work` 


## To Do
- Do NOT use for autodeployment just yet. Several students have deleted their Wikipedia project pages or parts of them. Also, some older years fail to build.
- Reintroduce the argument for processing only one year
- Port to Python 3.x



