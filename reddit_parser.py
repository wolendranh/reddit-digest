import heapq
import os
import re
import urllib.request

import nltk
from bs4 import BeautifulSoup as Soup
import praw
from psaw import PushshiftAPI

from settings import CREDENTIALS, SUBREDDIT


class RedditParser:
    reddit = None
    api = None
    parsed_submissions = []

    def __init__(self,):
        self.reddit = praw.Reddit(**CREDENTIALS)
        self.api = PushshiftAPI(self.reddit)

    def parse(self, ups=None, start=None, end=None, subreddit=SUBREDDIT, limit=None):
        for idx, sub in enumerate(self.get_submissions(ups, start, end, subreddit, limit)):
            self.get_self_text_links(submission=sub)
            # self.store_to_file(submission=sub, identifier=idx)

    def get_submissions(self, ups=None, start=None, end=None, subreddit=None, limit=None):
        if not subreddit:
            raise Exception('please provide subreddit object')

        for sub in self.api.search_submissions(after=start,
                                               before=end,
                                               subreddit=subreddit,
                                               limit=limit,
                                               filter=['url', 'author', 'title', 'subreddit']):
            if ups and sub.ups >= ups:
                yield sub

    def get_highlight_color(self, ups):
        color = ''
        if 100 <= ups < 300:
            color = 'green'
        elif 300 <= ups < 500:
            color = 'orange'
        elif ups >= 500:
            color = 'red'
        return color

    def store_to_file(self, submission, identifier, file_name='links.html',):
        if identifier == 0:
            try:
                os.remove(file_name)
            except OSError:
                pass

        if submission.id not in self.parsed_submissions:
            with open(file_name, 'a') as file:
                file.write("""
                <p>{id}&emsp;<a href='{url}' target='blank'>link</a>&emsp;{title}&emsp;<b style="color:{color}">{ups}</b></p>
                """.format(
                    id=identifier,
                    url=submission.shortlink,
                    title=submission.title,
                    ups=submission.ups,
                    color=self.get_highlight_color(ups=submission.ups)

                ))
            self.parsed_submissions.append(submission.id)

    def get_self_text_links(self, submission):
        if submission.selftext_html:
            html = Soup(submission.selftext_html, 'html.parser')
            for link in html.find_all('a'):
                print(link)
                if link.attrs['href'].startswith('https://medium.com'):
                    self.get_article_text(link.attrs['href'])

    def get_article_text(self, url):
        headers = {'User-Agent': 'Mozilla/5.0'}
        req = urllib.request.Request(url='https://en.wikipedia.org/wiki/Python_(programming_language)', headers=headers)
        article = urllib.request.urlopen(req).read()
        parsed_article = Soup(article, 'html')

        paragraphs = parsed_article.find_all('p')

        article_text = ""

        for p in paragraphs:
            article_text += p.text

        # Removing Square Brackets and Extra Spaces
        article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)
        article_text = re.sub(r'\s+', ' ', article_text)
        # Removing special characters and digits
        formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text)
        formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)

        sentence_list = nltk.sent_tokenize(article_text)

        stopwords = nltk.corpus.stopwords.words('english')

        # calculate frequency
        word_frequencies = {}
        for word in nltk.word_tokenize(formatted_article_text):
            if word not in stopwords:
                if word not in word_frequencies.keys():
                    word_frequencies[word] = 1
                else:
                    word_frequencies[word] += 1

        maximum_frequncy = max(word_frequencies.values())

        for word in word_frequencies.keys():
            word_frequencies[word] = (word_frequencies[word] / maximum_frequncy)

        # calculate score
        sentence_scores = {}
        for sent in sentence_list:
            for word in nltk.word_tokenize(sent.lower()):
                if word in word_frequencies.keys():
                    if len(sent.split(' ')) < 30:
                        if sent not in sentence_scores.keys():
                            sentence_scores[sent] = word_frequencies[word]
                        else:
                            sentence_scores[sent] += word_frequencies[word]

        summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)

        summary = ' '.join(summary_sentences)
        print(summary)
