#!/usr/bin/env python3
#
# httpgrep
#
# (c) 2018 Daniel Jankowski


from html.parser import HTMLParser


class HtmlParser (HTMLParser):

    # initialize the links array
    __links = []

    def __init_ (self):
        # initialize the html parser
        HTMLParser.__init__(self)

    def handle_starttag(self, tag, attributes):
        # convert attributes to array
        attr = self.__attributesToDict ( attributes )

        # check if script tag with src is the existing tag
        if tag == 'script' and attr['src']:
            # save the link
            self.__links.append(attr['src'])

        # check if link tag is a stylesheet
        elif tag == 'link' and attr['rel'] == 'stylesheet':
            # save the link
            self.__links.append(attr['href'])

    def __attributesToDict (self, attr):
        # initialize the dict
        dict_ = {}

        # iterate through attribute tuples
        for t in attr:
            # set key and value
            dict_[t[0]] = t[1]

        # return the dict
        return dict_

    def feed(self, data):
        # process the data
        super().feed(data)

        # return the links
        return self.__links


