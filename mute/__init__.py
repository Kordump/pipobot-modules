# -*- coding: utf-8 -*-
import random
from threading import Timer

import pipobot.lib.utils
from pipobot.lib.modules import SyncModule, defaultcmd

import xmpp


class CmdMute(SyncModule):
    def __init__(self, bot):
        desc = u"mute [nom]\n[nom] ne peut plus parler sur le salon !!!"
        SyncModule.__init__(self,
                            bot,
                            name="mute",
                            pm_allowed=False,
                            desc=desc)

    def restore(self, name):
        pipobot.lib.utils.unmute(name, self.bot)

    @defaultcmd
    def answer(self, sender, message):
        role_sender = self.bot.occupants.pseudo_to_role(sender)
        reasonfail = [u"%s: TPPT !!!",
                      u"%s: Je n'obéis qu'au personnel compétent",
                      u"%s: Tu crois vraiment que je vais t'obéir",
                      u"%s: Non mais tu te crois où ? oO",
                      u"%s: J'vais l'dire aux modérateurs"]
        reasonkick = [u"TU TE TAIS %s",
                      u"Désolé %s, je ne fais qu'obéir aux ordres"]

        lst = message.split(" ")
        rapport = u""
        if len(lst) == 2:
            if lst[0] == "undo":
                who = lst[1]
                pipobot.lib.utils.unmute(who, self.bot)
                return u"%s peut maintenant parler" % who

        for muted in lst:
            authorised = False
            or_not = False
            if muted == self.bot.name:
                rapport += u"Je vais pas me virer moi-même oO\n"
                continue
            jidmuted = self.bot.occupants.pseudo_to_jid(muted)
            jidsender = self.bot.occupants.pseudo_to_jid(sender)
            if jidmuted == "":
                rapport += u"%s n'est pas dans le salon\n" % muted
                continue
            if jidmuted == jidsender:
                if muted == sender:
                    rapport += u"Tu veux te muter toi-même ?\n"
            elif role_sender != "moderator":
                or_not = True
                authorised = True
                to_mute = sender
                rapport += u"%s n'a pas le droit de muter %s\n" % (sender, muted)
            else:
                authorised = True
                to_mute = muted
                rapport += u"J'ai muté %s pour toi !\n" % muted

            if authorised:
                if self.bot.occupants.pseudo_to_role(to_mute) == "moderator":
                    rapport = u"On ne peut pas muter quelqu'un ayant des droits aussi élevés\n"
                else:
                    t = Timer(30.0, lambda name=to_mute: self.restore(name))
                    t.start()
                    if or_not:
                        pipobot.lib.utils.mute(to_mute,
                                               random.choice(reasonfail) % to_mute,
                                               self.bot)
                    else:
                        pipobot.lib.utils.mute(to_mute,
                                               random.choice(reasonkick) % to_mute,
                                               self.bot)
        return rapport.rstrip()
