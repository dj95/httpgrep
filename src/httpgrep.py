#!/usr/bin/env python3
#
# httpgrep
#
# (c) 2018 Daniel Jankowski


import argparse
import requests

from colorama import Fore, Back, Style
from htmlparser import HtmlParser


def do_request(url):
    # do a get request and get the html as text
    page = requests.get(url).text

    # return the string
    return page


def color_keyword(line, keyword, keyword_position):
    # part before the keyword
    part_one = line[max(keyword_position - 20,0):keyword_position] 

    # part after the keyword
    part_three = line[keyword_position + len(keyword) + 1:keyword_position + len(keyword) + 60]

    # return the parts with a red colored keyword
    return part_one + Fore.RED + keyword + Fore.RESET + part_three


def process_source(data, keyword):
    # initialize counter
    counter = 1

    # iterate through lines of the response
    for line in data.split('\n'):
        # check if keyword is in line
        if keyword in line:
            # find the keyword position
            keyword_position = line.find(keyword)

            # print in color
            print(Fore.GREEN + ' {} {}:{}'.format(
                # print line and position of the keyword
                counter, keyword_position, keyword_position + len(keyword)
            # reset colors
            ) + Fore.RESET + '>  {}'.format(
                # print 80 characters around the keyword and color the keyword
                color_keyword(line, keyword, keyword_position)
            ))

        # raise the line counter
        counter += 1
    # print a spacer
    print()


def main():
    # initialize argument parser
    parser = argparse.ArgumentParser()

    # add arguments
    parser.add_argument('url')
    parser.add_argument('keyword')

    # get arguments
    args = parser.parse_args()

    # set keyword and url from arguments
    keyword = args.keyword
    url = args.url

    # do a get request and get html from url
    response = do_request(url)

    # check if keyword is in response
    if keyword in response:
        print(Fore.BLUE + '==>' + Fore.RESET + ' {}'.format(url))
        results = process_source(response, keyword)

    # initialize html parser
    parser = HtmlParser()

    # parse links from parser
    links = parser.feed(response)

    # iterate through collected links
    for link in links:
        # get the css or js file behind the links
        response = do_request(link)

        # check if keyword is in css or js file
        if keyword in response:
            print(Fore.BLUE + '==>' + Fore.RESET + ' {}'.format(link))
            results = process_source(response, keyword)
            

    pass


if __name__ == '__main__':
    main()
