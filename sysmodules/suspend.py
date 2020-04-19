# -*- coding: utf-8 -*-
# Coded by @maxunof with power of Senko!

import moduling
import time
import utils

class Module(moduling.Module):
    def __init__(self):
        self.name = "Suspension"

    async def suspendcmd(self, db, client, message, cmd):
        try:
            seconds = int(cmd.arg)
            await utils.send(message, "<b>Bot is sleeping for {} seconds 😴</b>".format(seconds))
            time.sleep(seconds)
        except ValueError:
            await utils.send(message, "<b>Invalid suspension time.</b>")
