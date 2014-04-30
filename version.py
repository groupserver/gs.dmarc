# -*- coding: utf-8 -*-
version = '2.0.0'
release = False

#-----------------------------------------------------------------------------#
import sys
if (sys.version_info < (3, )):
    from commands import getstatusoutput
else:
    from subprocess import getstatusoutput  # lint:ok
import datetime
import os
import glob


class CommandError(Exception):
    pass


def execute_command(commandstring):
    status, output = getstatusoutput(commandstring)
    if status != 0:
        m = 'Command "{0}" exited with status {1}'
        msg = m.format(commandstring, status)
        raise CommandError(msg)
    return output


def parse_version_from_package():
    try:
        pkginfo = os.path.join(glob.glob('*.egg-info')[0],
                                         'PKG-INFO')
    except:
        pkginfo = ''

    version_string = ''
    if os.path.exists(pkginfo):
        for line in open(pkginfo):
            if line.find('Version: ') == 0:
                version_string = line.strip().split('Version: ')[1].strip()
        if not version_string:
            version_string = '%s-dev' % version
    else:
        version_string = version

    return version_string


def get_version():
    try:
        globalid = execute_command("hg identify -i").strip('+')
        c = "hg log -r %s --template '{date|isodatesec}'" % globalid
        commitdate = execute_command(c)
        # convert date to UTC unix timestamp, using the date command because
        # python date libraries do not stabilise till about 2.6
        timestamp = int(execute_command('date -d"%s" --utc +%%s' % commitdate))

        # finally we have something we can use!
        dt = datetime.datetime.utcfromtimestamp(timestamp)
        datestring = dt.strftime('%Y%m%d%H%M%S')
        if release:
            version_string = version
        else:
            version_string = "%s.dev%s-%s" % (version, datestring, globalid)

    except (CommandError, ValueError, TypeError):
        # --=mpj17=-- Usually because we are building out a source-egg, rather
        # than from a Hg source-directory.
        version_string = parse_version_from_package()

    return version_string

if __name__ == '__main__':
    import sys
    sys.stdout.write('{0}\n'.format(get_version()))
