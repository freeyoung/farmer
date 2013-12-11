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
    sudo = models.BooleanField(default = False) 

    # for example: ansible web_servers -m shell -a 'du -sh /tmp'
    # the 'du -sh /tmp' is cmd here
    cmd = models.TextField(null = False, blank = False)

    # return code of this job
    rc = models.IntegerField(null = False) 

    # failed hosts
    inventories_failure = models.TextField(null = True, blank = True)

    stdout = models.TextField(null = True, blank = True)
    stderr = models.TextField(null = True, blank = True)

    date_created = models.DateTimeField()
    date_done = models.DateTimeField()

    @property
    def cmd_shell(self):
        option = self.sudo == '0' and '--sudo -m shell -a' or '-m shell -a'
        return 'ansible %s %s "%s"' % (self.inventories, option, self.cmd)

    def run(self):
        if 0 == 0:
            tmpdir = '/tmp/ansible_%s' % time.time()
            os.mkdir(tmpdir)
            cmd_shell = self.cmd_shell + ' -t ' + tmpdir
            self.date_created = datetime.now()
            status, output = getstatusoutput(cmd_shell)
            print output
            self.date_done = datetime.now()

            inventories_failure = []
            stdout = {}
            stderr = {}

            for f in os.listdir(tmpdir):
                var = json.loads(open(tmpdir + '/' + f).read())
                if var.get('rc') != 0:
                    inventories_failure.append(f)
                stdout[f] = var['stdout']
                stderr[f] = var['stderr']
                
            self.rc = status
            self.inventories_failure = ':'.join(inventories_failure)
            self.stdout = json.dumps(stdout)
            self.stderr = json.dumps(stderr)
            self.save()
        

    def __unicode__(self):
        return self.cmd_shell


