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

    # Update from sources list repositories
    api.sudo('aptitude -y update')

    # A safe upgrade of debian
    api.sudo('aptitude -y safe-upgrade ')
    
    version = api.env['python-version']
    major = '.'.join(version.split('.')[:2])
    
    #Install and Update Dependencies

    #contrib.files.append(apt_source, '/etc/apt/source.list', use_sudo=True)
    api.sudo('aptitude -yq install '
             'build-essential '
             'python%(major)s python%(major)s-dev '
             'python-libxml2 '
             'ncurses-dev '
             'libncurses5-dev '
             'libz-dev '
             'libdb4.6 '
             'libxp-dev '
             'libssl-dev '
             'libreadline5-dev '
             'readline-common '
             'libxml2-dev '
             'tar '
             'unzip '
             'bzip2 '
             'wv '
             'xpdf-utils '
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

    # python-profiler?
    api.sudo('aptitude -yq install python-profiler' % locals())

    # Repository control version tools
    api.sudo('aptitude -yq install subversion git-core' % locals())

    #ensure bootstrap files have correct owners
    hostout.setowners()


def predeploy():
    path = api.env.path
    api.env.cwd = ''

    if api.sudo("ls  %(path)s/bin/buildout || echo 'bootstrap' " % locals()) == 'bootstrap':
        bootstrap()
    #bootstrap()


def installPIP():
    """ Install dependecies for PIP Tool on debian """
    version = api.env['python-version']
    major = '.'.join(version.split('.')[:2])
    
    #to install PIP tool
    api.sudo('aptitude -yq install python-setuptools' % locals())
    api.sudo('easy_install-%(major)s pip' % locals())


def installPIL():
    """ Install dependecies for PIL on debian """
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

