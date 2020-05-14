import logging
import os
import re
import shutil
import subprocess
import sys


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
logging.basicConfig(level=logging.INFO)
log = logging.getLogger('manage.py')

UUID = '46ea591951824d8e9376b0f98fe4d48a'
PROJECT_NAME = 'PROJECT_' + UUID
APP_NAME = 'APP_' + UUID
APP_UPPER_NAME = 'APP_UPPER_' + UUID
APP_LOWER_NAME = 'app_lower_' + UUID

def showUsage():
    print('''Usage:
    python manage.py <option>
    python manage.py startproject <project-name>
    python manage.py startapp <app-name>
    ''')
    sys.exit()


def sed(old, new, filePath):
    ignoreRegex = re.compile(r'\.((db)|(png)|(js.map))$')
    if ignoreRegex.search(filePath):
        return
    try:
        lines = [i.replace(old, new) for i in open(filePath) if not ignoreRegex.search(filePath)]
        open(filePath, 'w').writelines(lines)
    except UnicodeDecodeError as e:
        log.warning('old = {}, new = {}, filePath = {}'.format(old, new, filePath))
        log.warning(e)


def mv(old, new, filePath):
    if old in filePath:
        cmdStr = r'mv {} {}'.format(filePath, filePath.replace(old, new))
        log.debug(cmdStr)
        os.system(cmdStr)


# def opt_testTransferFromMepServices():
#     os.system(r'rm -rf {} && cp -r {} {} && rm -rf {} {}'.format(
#         os.path.join(BASE_DIR, 'template'),
#         os.path.join(BASE_DIR, 'mep-services'),
#         os.path.join(BASE_DIR, 'template'),
#         os.path.join(BASE_DIR, 'template', 'dist'),
#         os.path.join(BASE_DIR, 'template', 'doc')
#         ))
#     for root, dirs, files in os.walk(os.path.join(BASE_DIR, 'template')):
#         for name in dirs:
#             absPath = os.path.join(root, name)
#             mv('mep', APP_NAME, absPath)
#     for root, dirs, files in os.walk(os.path.join(BASE_DIR, 'template')):
#         for name in files:
#             absPath = os.path.join(root, name)
#             sed('mep-services', PROJECT_NAME, absPath)
#             sed('mep_lower', APP_LOWER_NAME, absPath)
#             sed('mep', APP_NAME, absPath)
#             sed('MEP', APP_UPPER_NAME, absPath)
#             mv('mep', APP_NAME, absPath)


def opt_startproject(projectName):
    log.info('startproject: {}'.format(projectName))


def opt_startapp(appName):
    log.info("startapp: {}".format(appName))


def _assert_cmd_exist(cmd):
    try:
        subprocess.call(cmd)
    except Exception as e:
        log.warning('{}->{}'.format(type(e), e))
        log.error('Command "{}" not exist!'.format(cmd))
        sys.exit()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        showUsage()

    selfModule = __import__(__name__)
    optFunName = 'opt_' + sys.argv[1].strip()
    if optFunName not in selfModule.__dict__:
        showUsage()

    if BASE_DIR.strip():
        os.chdir(BASE_DIR)
    try:
        selfModule.__dict__[optFunName](*sys.argv[2:])
    except TypeError as e:
        log.error('{} failed: {}'.format(optFunName, e))
        raise
