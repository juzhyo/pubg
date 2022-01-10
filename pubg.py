################################################
# Script to generate updated publications page #
# Author: Justin Zhou Yong                     #
################################################

import codecs
import pandas as pd
from scholarly import scholarly


search_query = scholarly.search_author_id("p4TVZTEAAAAJ", sortby="year")
author = scholarly.fill(search_query, sortby="year")

# first_publication = author['publications'][0]
# i=1

# for pub in author['publications']:
#     scholarly.fill(pub)
#     # print(i)
#     # i+=1

# for i in range(50):
for i in range(len(author['publications'])):
    scholarly.fill(author['publications'][i])
    print(i)
    # i+=1

publication_titles = [pub['bib']['title'] for pub in author['publications']]
publication_years = [pub['bib'].get('pub_year') for pub in author['publications']]
publication_authors = [pub['bib'].get('author') for pub in author['publications']]
publication_journals = [pub['bib'].get('journal') for pub in author['publications']]
publication_urls = [pub.get('pub_url') for pub in author['publications']]

header = codecs.open("header.html", 'r')
footer = codecs.open("footer.html", 'r')
publications = codecs.open("publications.html", 'w')

while True:
    line = header.readline()
    publications.write(line)

    if not line:
        break

# titles = ['Substitutional doping in 2D transition metal dichalcogenides', 'Coupling 2D Materials to an Elastomer Waveguide', 'Measuring valley polarization in transition metal dichalcogenides with second-harmonic spectroscopy', 'Synergistic additive-mediated CVD growth and chemical modification of 2D materials', 'Electroluminescent devices based on 2D semiconducting transition metal dichalcogenides', 'Excitonic electro-optical phenomena in van der Waals crystals', 'The substrate influence on the optoelectronic properties of 2D materials']
# journals = ['Nano Research', '2019 Conference on Lasers and Electro-Optics Europe & European Quantum Electronics Conference (CLEO/Europe-EQEC)', 'ACS Photonics', 'Chemical Society Reviews', 'Advanced Materials', 'JSAP-OSA Joint Symposia', '2018 Conference on Lasers and Electro-Optics Pacific Rim (CLEO-PR)']

publication_authors = ['-' if i is None else i for i in publication_authors]
publication_years = ['-' if i is None else i for i in publication_years]
# publication_journals = ['-' if i is None else i for i in publication_authors]
publication_journals = ['-' if i is None else i for i in publication_journals]
publication_urls = ['-' if i is None else i for i in publication_urls]

publication_include = ['yes' for i in range(len(publication_titles))]
publication_dois = [url.split('/')[-2] + "/" + url.split('/')[-1] for url in publication_urls]
publication_authors = [authors.replace(" and ", ", ") for authors in publication_authors]

df = pd.read_csv('pub_list.csv',sep='>',names = ['titles', 'authors', 'journals', 'urls', 'dois', 'years', 'include'], skiprows=1)

# pub_dict = {'titles': publication_titles, 'authors': publication_authors, 'journals': publication_journals, 'urls': publication_urls, 'dois': publication_dois, 'years': publication_years, 'include': publication_include}
# df = pd.DataFrame(pub_dict)
# df.to_csv('./pub_list.csv', sep='>', index=None)

# df_list = pd.read_csv('pub_list.csv', sep='>', names=['title','journal'], skiprows=1)

titles= df['titles'].tolist()
authors= df['authors'].tolist()
years = df['years'].tolist()
journals = df['journals'].tolist()
urls = df['urls'].tolist()
inc = df['include'].tolist()
dois = df['dois'].tolist()



for i in range(len(publication_titles)):
    if publication_titles[i] not in titles:
        titles.insert(0, publication_titles[i])
        authors.insert(0, publication_authors[i])
        years.insert(0, str(publication_years[i]))
        journals.insert(0, publication_journals[i])
        urls.insert(0, publication_urls[i])
        dois.insert(0, publication_dois[i])
        inc.insert(0, 'yes')

pub_dict = {'titles': titles, 'authors': authors, 'journals': journals, 'urls': urls, 'dois': dois, 'years': years, 'include': inc}
df = pd.DataFrame(pub_dict)
df.to_csv('./pub_list.csv', sep='>', index=None)

curr_year = []

for i in range(len(titles)):
    if inc[i] == 'yes':
        if (years[i] not in curr_year) and (int(years[i]) > 2010):
            if curr_year:
                publications.write("</ol>")

            publications.write('<h1 class="blog-post-title">' + str(df['years'][i]) + '</h1>')
            publications.write("<ol>")
            curr_year.append(years[i])

        elif int(years[i]) == 2010 and (curr_year[-1] != years[i]):
            publications.write("</ol>")
            publications.write('<h1 class="blog-post-title">' + '- 2010' + '</h1>')
            publications.write("<ol>")
            curr_year.append(years[i])

    # if publication_titles[i] in titles:
    #     publication_journal[i] = journals[titles.index(publication_titles[i])]

        print(i)
        entry = "<li><b>" + titles[i] + "</b><br>" + authors[i].replace(" and ", ", ") + "<br>" + journals[i] + ', doi: <a href="' + urls[i] + '" target="_blank" rel="noopener">' + dois[i] + "</a><br><br></li>"
    # print(entry)
        publications.write(entry)

    else:
        continue

# # <li><b>Mode-center Placement of Monolayer WS<sub>2</sub> in a Photonic Polymer Waveguide</b><br>
# #              Angelina Frank, Justin Zhou, James A. Grieve, Ivan Verzhbitskiy, José Viana-Gomes, Leyi Loh, Michael Schmid, Kenji Watanabe, Takashi Taniguchi, Goki Eda, Alexander Ling<br>
# #              Advanced Optical Materials, doi: <a href="https://onlinelibrary-wiley-com.libproxy1.nus.edu.sg/doi/10.1002/adom.202101684" target="_blank" rel="noopener">10.1002/adom.202101684</a><br><br></li>

while True:
    line = footer.readline()
    publications.write(line)

    if not line:
        break

# # print(header.read())
publications.close()
