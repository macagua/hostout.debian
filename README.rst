hostout.debian
**************

A plugin for collective.hostout_ for debian host.

- Code repository: http://github.com/macagua/hostout.debian
- Questions and comments to http://github.com/macagua/hostout.debian/issues
- Report bugs at http://github.com/macagua/hostout.debian/issues

.. contents::

What does it do?
****************

If you are new to remote application management on debian_ host, hostout.debian can help you to
deploy your first site in minutes. hostout.debian is compatible with Plone on Debian Lenny and 
Debian Squeeze or any other buildout based environment.
    
hostout.debian is a Plugin for collective.hostout_ that is a zc.buildout recipe_
Hostout generates a script which logs into your remote host(s) and performs preset and customizable commands. e.g.

$ bin/hostout productionserver deploy

$ bin/hostout server1 server2 supervisorctl restart instance1

$ bin/hostout all cmd ls -al

$ bin/hostout staging mylocalfabriccommand

How does it do that?
********************

Commands can easily be added from a local fabric_ script, hostout command plugins or just the
builtin commands to help you bootstrap and deploy your buildout to remote hosts.

Why is hostout awesome?
***********************
Managing multiple environments can be a real pain and a barrier to development.
Hostout puts all of the settings for all of your environments in an easy-to-manage format.

.. _collective.hostout: http://pypi.python.org/pypi/collective.hostout
.. _debian: http://www.debian.org/
.. _recipe: http://pypi.python.org/pypi/zc.buildout#recipes
.. _fabric: http://fabfile.org

