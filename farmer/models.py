#coding=utf8

import os
import time
import json
from datetime import datetime
from commands import getstatusoutput

from django.db import models

class Job(models.Model):

    # hosts, like web_servers:host1 .
    inventories = models.TextField(null = False, blank = False)

    # 0, do not use sudo; 1, use sudo .
    sudo = models.BooleanField(default = True) 

    # for example: ansible web_servers -m shell -a 'du -sh /tmp'
    # the 'du -sh /tmp' is cmd here
    cmd = models.TextField(null = False, blank = False)

    # return code of this job
    rc = models.IntegerField(null = True) 

    result = models.TextField(null = True)

    start = models.DateTimeField(null = True)
    end = models.DateTimeField(null = True)

    @property
    def cmd_shell(self):
        option = self.sudo and '--sudo -m shell -a' or '-m shell -a'
        return 'ansible %s %s "%s"' % (self.inventories, option, self.cmd)

    def run(self):
        if os.fork() == 0:
            tmpdir = '/tmp/ansible_%s' % time.time()
            os.mkdir(tmpdir)
            self.start = datetime.now()
            self.save()
            cmd_shell = self.cmd_shell + ' -t ' + tmpdir
            status, output = getstatusoutput(cmd_shell)
            self.end = datetime.now()
            result = {}
            for f in os.listdir(tmpdir):
                result[f] = json.loads(open(tmpdir + '/' + f).read())
            self.rc = status
            self.result = json.dumps(result)
            self.save()
            os.system('rm -rf ' + tmpdir)

    def __unicode__(self):
        return self.cmd_shell


