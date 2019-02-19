from mb.command import build

CONFIG_FILE='/opt/config/test.yml'
INDY_URL_FILE='/opt/config/indy-url'

with open(INDY_URL_FILE) as f:
    indy_url=f.read().rstrip()

command.build( CONFIG_FILE, indy_url, delay=60 )
