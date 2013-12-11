#coding=utf8

from django.db import models

class Job(models.Model):

    # hosts, like web_servers:host1 .
    inventories = models.TextField(null = False, blank = False)

    # 0, do not use sudo; 1, use sudo .
    sudo = models.CharField(null = False, blank = False, default = '0') 

    # for example: ansible web_servers -m shell -a 'du -sh /tmp'
    # the 'du -sh /tmp' is cmd here
    cmd = models.TextField(null = False, blank = False)

    # return code of this job
    rc = models.CharField(null = False, blank = False, default = '0') 

    # failed hosts
    inventories_failure = models.TextField(null = False, blank = False)

    stdout = models.TextField(null = True, blank = True)
    stderr = models.TextField(null = True, blank = True)

    date_created = models.DateTimeField(auto_now_add=True)
    date_done = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        option = self.sudo == '0' and '--sudo -m shell -a' or '-m shell -a'
        return 'ansible %s %s "%s"' % (self.inventories, option, self.cmd)


