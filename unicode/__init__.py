# -*- coding: utf-8 -*-
import os

from pipobot.lib.modules import SyncModule, defaultcmd

# Maximum de réponse :
MAX = 5
# On charge en RAM le fichier Unicode
# Récupéré de http://unicode.org/Public/UNIDATA/UnicodeData.txt
# with open('UnicodeDataLower.txt') as unicode_file: => Pas de python >2.5 sur vega
#     unicodes = [l.split(";")[0:2] for l in unicode_file]


class CmdUnicode(SyncModule):
    def __init__(self, bot):
        desc = """Unicode caractère
    Affiche des informations sur le caractère unicode « caractère »
unicode nom
    Recherche le caractère unicode donc le nom ressemble à « nom »
"""
        unicode_file = open(os.path.join(os.path.dirname(__file__), 'UnicodeDataLower.txt'))

        # unicode_file = open(os.path.join(config_dir, 'UnicodeDataLower.txt'))
        self.unicodes = [l.split(";")[0:2] for l in unicode_file]
        unicode_file.close()

        SyncModule.__init__(self,
                            bot,
                            desc=desc,
                            name="unicode")

    @defaultcmd
    def answer(self, sender, message):
        m = message.lower()

        if type(message) == str:
            message = message.decode('utf8')

        if len(message) == 1:
            code_rech = "%04x" % ord(m)
            for code, name in self.unicodes:
                if code == code_rech:
                    return u"⌞%s⌟ : %s, code %s" % (message, name, code_rech)

            return u"%s ? C’est quoi ?" % message

        if len(message) < 3:
            return "Minimum 3 caractères"

        send = u''
        c = 0
        for code, name in self.unicodes:
            if m in name and name != '<control>':
                if c != 0:
                    send += u"\n"
                send += u"* %s, code %s => %c" % (name, code, int(code, 16))
                c += 1
            if c >= MAX:
                break
        return send if send != u'' else u'Aucun résultat trouvé'
