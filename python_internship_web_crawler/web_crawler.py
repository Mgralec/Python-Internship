import requests
from bs4 import BeautifulSoup


def site_map(url):
    #Main function generatin map of a site
    global global_url
    global_url = url
    list_of_links = []
    list_of_links.append(str(url))
    #Inserting url taken from parameter in function

    for link in list_of_links:
        #Looping through list with links. For each link it runs function which takes all links from particular url
        links_per_page = create_set_of_links(link)
        for item in links_per_page:
            if item not in list_of_links:
                list_of_links.append(item)
            else:
                continue
    r = form_data(list_of_links)
    #Running function responsible for formating data
    print(r)






def form_data(list_of_urls):
    #Function responsible for forming data into nested dictionary. It takes list of urls as a parameter
    data_dict = {}
    for url in list_of_urls:
        data_dict[url] = {}
        titles = create_list_of_titles(url)
        links = create_set_of_links(url)
        #Calling function responsible for returning set of links and list of titles
        for title in titles:
            data_dict[url]['title'] = title

        data_dict[url]['links'] = links


    return data_dict


def create_set_of_links(url):
    #Function takes parameter url. It parses url and stores all the links into set
    list = []
    link_dict = set()
    soup = parse_html(url)
    #Calling function responsible for parsing url
    for item in soup.find_all('a'):
        link = item.get('href')
        if 'clearcode' not in link and item not in list:
            #removing items containing 'clearcode' from the list for testing purposes.
            if 'http' not in link:
                list.append(global_url + link)
            elif '0.0.0.0' in link:
                #0.0.0.0 is not representation of address that can be called.
                newlink = link.replace('0.0.0.0', 'localhost')
                #replacing 0.0.0.0 with localhost to generate valid urls
                list.append(newlink)
            else:
                list.append(link)
        else:
            break
    for item in list:
        link_dict.add(item)
    return link_dict


def create_list_of_titles(url):
    #Creating list of titles basing on paresd html
    list_of_titles = []
    soup = parse_html(url)

    for item in soup.find_all('title'):
        list_of_titles.append(item.string)

    return list_of_titles


def parse_html(url):
    #Function responsible for parsing html out of url
    source_code = requests.get(url)
    text = source_code.text
    soup = BeautifulSoup(text, "html.parser")
    return soup




