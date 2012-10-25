#-*- coding: utf-8 -*-

import random
import urllib
import pipobot.lib.utils
from BeautifulSoup import BeautifulSoup
from pipobot.lib.abstract_modules import FortuneModule
from pipobot.lib.module_test import ModuleTest


class CmdScmb(FortuneModule):
    def __init__(self, bot):
        desc = u"""Pour appendre des choses grâce à secouchermoinsbete.fr
scmb : Retourne une information aléatoire.
scmb [n] : Affiche l'information [n]"""
        FortuneModule.__init__(self,
                               bot,
                               desc=desc,
                               command="scmb",
                               url_random="http://www.secouchermoinsbete.fr/au-hasard",
                               url_indexed='http://www.secouchermoinsbete.fr/%s-content',
                               lock_time=5,
                               )

    def extract_data(self, html_content):
        soup = BeautifulSoup(html_content)
        error_title = soup.find("h2", {"class": "page-title"})
        if error_title is not None and "Page non trouv" in error_title.text:
            return u"La quote demandée n'existe pas. (Erreur 404)"
        else:
            sections = soup.findAll("p", {"class": "anecdote-summary"})
            details = soup.findAll("p", {"class": "anecdote-details"})
            # If we are in a random page, we select a quote then continue parsing
            if len(sections) != 1:
                quotes = soup.findAll("h3", {"class": "anecdotes title"})
                if quotes == []:
                    return u"scmb invalide !!"
                choiced = random.choice(quotes)
                url = choiced.a.get("href")
                page = urllib.urlopen(url)
                content = page.read()
                page.close()
                soup = BeautifulSoup(content)
                sections = soup.findAll("p", {"class": "anecdote-summary"})
                details = soup.findAll("p", {"class": "anecdote-details"})
            if sections == []:
                return u"scmb invalide !!"
            summary = sections[0].text
            div = soup.find("div", {"class": "anecdote box-container"})
            nb = div.get("id").split("-", 1)[1]
            if details != []:
                summary = u"%s\n%s" % (summary, details[0].text)
            full_quote = pipobot.lib.utils.xhtml2text(unicode(summary))
            result = u"scmb#%s : \n%s" % (nb, full_quote)
            return result.rstrip()


class ScmbTest(ModuleTest):
    def test_random(self):
        self.assertRegexpListMatches(self.bot_answer("!scmb"),
                                     ["scmb invalide !!", r"scmb#(\d+) : .*"])

    def test_fail(self):
        self.assertEqual(self.bot_answer("!scmb 42"), "scmb invalide !!")

    def test_ok(self):
        self.assertRegexpMatches(self.bot_answer("!scmb 133"), r"scmb#(\d+) : .*")
