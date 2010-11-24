import os
import os.path
from fabric import api,contrib

src_lenny="""
deb http://ftp.us.debian.org/debian/ lenny main contrib non-free
deb-src http://ftp.us.debian.org/debian/ lenny main contrib non-free
deb http://security.debian.org/ lenny/updates main contrib non-free
deb-src http://security.debian.org/ lenny/updates main contrib non-free
deb http://www.debian-multimedia.org lenny main non-free
deb http://backports.debian.org/debian-backports lenny-backports main
"""
src_squeeze="""
deb http://ftp.us.debian.org/debian/ squeeze main contrib non-free
deb-src http://ftp.us.debian.org/debian/ squeeze main contrib non-free
deb http://security.debian.org/ squeeze/updates main contrib non-free
deb-src http://security.debian.org/ squeeze/updates main contrib non-free
deb http://www.debian-multimedia.org squeeze main non-free
deb http://www.backports.org/debian squeeze-backports main contrib non-free
"""

def bootstrap():
    """Update debian with build tools, python and bootstrap buildout"""
    hostout = api.env.get('hostout')
    path = api.env.path
 
    # Add the plone user:
    hostout.setupusers()
    api.sudo('mkdir -p %(path)s' % locals())
    hostout.setowners()

    #http://wiki.linuxquestions.org/wiki/Find_out_which_linux_distribution_a_system_belongs_to
    d = api.run(
    #            "[ -e /etc/SuSE-release ] && echo SuSE "
    #            "[ -e /etc/redhat-release ] && echo redhat"
    #            "[ -e /etc/fedora-release ] && echo fedora || "
                "lsb_release -rd "
    #            "[ -e /etc/debian_version ] && echo debian || "
    #            "[ -e /etc/debian-version ] && echo ubuntu || "
    #            "[ -e /etc/slackware-version ] && echo slackware"
               )
    print d
    api.run('uname -r')

#    api.sudo('aptitude -y update')
#    api.sudo('aptitude -y safe-upgrade ')
    
    
    version = api.env['python-version']
    major = '.'.join(version.split('.')[:2])
    
    #Install and Update Dependencies

    #contrib.files.append(apt_source, '/etc/apt/source.list', use_sudo=True)
    api.sudo('aptitude -yq install '
             'build-essential '
#             'python%(major)s python%(major)s-dev '
#             'python-libxml2 '
#             'python-elementtree '
#             'python-celementtree '
             'ncurses-dev '
             'libncurses5-dev '
# needed for lxml on lucid
             'libz-dev '
             'libdb4.6 '
             'libxp-dev '
             'libreadline5 '
             'libreadline5-dev '
             % locals())

    try:
        api.sudo('aptitude -yq install python%(major)s python%(major)s-dev '%locals())
        #install buildout
        api.env.cwd = api.env.path
        api.sudo('wget -O bootstrap.py http://python-distribute.org/bootstrap.py')
        api.sudo('echo "[buildout]" > buildout.cfg')
        api.sudo('python%(major)s bootstrap.py' % locals())
    except:
        hostout.bootstrapsource()

    #api.sudo('aptitude -yq update; aptitude safe-upgrade; aptitude dist-upgrade')

#    api.sudo('apt-get install python2.4=2.4.6-1ubuntu3.2.9.10.1 python2.4-dbg=2.4.6-1ubuntu3.2.9.10.1 \
# python2.4-dev=2.4.6-1ubuntu3.2.9.10.1 python2.4-doc=2.4.6-1ubuntu3.2.9.10.1 \
# python2.4-minimal=2.4.6-1ubuntu3.2.9.10.1')
    #wget http://mirror.aarnet.edu.au/pub/ubuntu/archive/pool/main/p/python2.4/python2.4-minimal_2.4.6-1ubuntu3.2.9.10.1_i386.deb -O python2.4-minimal.deb
    #wget http://mirror.aarnet.edu.au/pub/ubuntu/archive/pool/main/p/python2.4/python2.4_2.4.6-1ubuntu3.2.9.10.1_i386.deb -O python2.4.deb
    #wget http://mirror.aarnet.edu.au/pub/ubuntu/archive/pool/main/p/python2.4/python2.4-dev_2.4.6-1ubuntu3.2.9.10.1_i386.deb -O python2.4-dev.deb
    #sudo dpkg -i python2.4-minimal.deb python2.4.deb python2.4-dev.deb
    #rm python2.4-minimal.deb python2.4.deb python2.4-dev.deb

    # python-profiler?
    

    #ensure bootstrap files have correct owners
    hostout.setowners()


def predeploy():
    path = api.env.path
    api.env.cwd = ''

    if api.sudo("ls  %(path)s/bin/buildout || echo 'bootstrap' " % locals()) == 'bootstrap':
        bootstrap()
    #bootstrap()

def installPIL():
    """ Install dependecies for PIL on ubuntu """
    hostout = api.env.get('hostout')

    version = api.env['python-version']
    major = '.'.join(version.split('.')[:2])
    
    api.sudo('aptitude -ym install '
             'python-imaging '
             'libjpeg-dev '
             'libfreetype6-dev '
             'zlib1g-dev '
             'libjpeg62-dev ')

    #to install Python tools 2.4
    api.sudo('wget http://peak.telecommunity.com/dist/ez_setup.py')
    api.sudo('python%(major)s ez_setup.py' % locals())

    #to install PIL
    api.sudo('easy_install-%(major)s --find-links http://download.zope.org/distribution PILwoTK' % locals())
    api.sudo('easy_install-%(major)s --find-links http://dist.repoze.org/PIL-1.1.6.tar.gz PIL' % locals())

    #if its ok you will see something like this:
    #--------------------------------------------------------------------

    #*** TKINTER support not available

    #--- JPEG support ok

    #--- ZLIB (PNG/ZIP) support ok

    #--- FREETYPE2 support ok

    #--------------------------------------------------------------------



