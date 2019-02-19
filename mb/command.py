import click
import os
from ruamel.yaml import YAML
import mb.util
import mb.builder
import mb.reporter
from Queue import Queue
import time
from datetime import datetime as dt
import requests

@click.command()
@click.argument('testfile', type=click.Path(exists=True))
@click.argument('indy_url')
@click.option('--delay', '-D', help='Delay between starting builds')
def build(testfile, indy_url, delay=0):
    with open(testfile) as f:
        yaml = YAML(typ='safe')
        build_config = yaml.load(f)

    if delay is None:
        delay = 0
    else:
        delay = int(delay)

    cwd = os.getcwd()
    try:
        project_dir = os.path.abspath(os.path.dirname(testfile))
        builds_dir = "builds-%s" % dt.now().strftime("%Y%m%dT%H%M%S")

        tid_base = "build_%s" % os.path.basename(project_dir)

        build = build_config['build']
        report = build_config['report']

        os.chdir(project_dir)

        project_src_dir = build.get('project-dir') or 'project'
        project_src_dir = os.path.join(os.getcwd(), project_src_dir)

        git_branch = build.get('git-branch') or 'master'

        build_queue = Queue()
        report_queue = Queue()

        try:
            for t in range(int(build['threads'])):
                thread = mb.builder.Builder(build_queue, report_queue)
                thread.daemon = True
                thread.start()

            for x in range(build['builds']):
                builddir = mb.util.setup_builddir(builds_dir, project_src_dir, git_branch, tid_base, x)
                build_queue.put((builddir, indy_url, build_config['proxy-port'], (x % int(build['threads']))*int(delay)))

            build_queue.join()

            for t in range(int(report['threads'])):
                thread = mb.reporter.Reporter(report_queue)
                thread.daemon = True
                thread.start()

            report_queue.join()
        except Exception as e:
            print(e)
            print("Quitting.")
    finally:
        os.chdir(cwd)

