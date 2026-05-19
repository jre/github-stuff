from argparse import ArgumentParser
import datetime
import json
import os

from cryptography.hazmat.primitives.serialization import pkcs12
from cryptography.hazmat.primitives import hashes
import jinja2
import yaml


jinja2_extensions = ('.jinja2', '.j2')


def target_filename(name):
    for ext in jinja2_extensions:
        if name.endswith(ext):
            return name[:-len(ext)]


class UndercomplicatedLoader(jinja2.BaseLoader):
    def get_source(self, environment, template):
        if not os.path.exists(template):
            raise jinja2.TemplateNotFound(template)
        mtime = os.path.getmtime(template)
        with open(template) as fh:
            data = fh.read()
        return data, template, lambda: mtime == os.path.getmtime(template)


def fromtimestamp_millis_filter(millis):
    return datetime.datetime.fromtimestamp(millis/1000, datetime.UTC)


def strftime_millis_filter(millis, format=None):
    dt = fromtimestamp_millis_filter(millis)
    if format is None:
        return dt.ctime()
    return dt.strftime(format)


def read_fdroid(base):
    with open(os.path.join(base, 'repo/index-v2.json'), 'r') as fh:
        index = json.load(fh)
    with open(os.path.join(base, 'config.yml'), 'r') as fh:
        conf = yaml.safe_load(fh)
    with open(conf['keystore'], 'rb') as fh:
        key, cert, extra = pkcs12.load_key_and_certificates(
            fh.read(), conf['keystorepass'].encode())

    env = {
        'repo_fingerprint': cert.fingerprint(hashes.SHA256()).hex(),
        'repo': index['repo'],
        'apps': {},
    }

    for key in ('repo_name', 'repo_description', 'repo_url'):
        if key in conf:
            env[key] = conf[key]
    if 'repo_url' in env:
        env['repo_url_full'] = 'https://fdroid.link/#' + \
            '%(repo_url)s?fingerprint=%(repo_fingerprint)s' % env

    for name, pkg in index['packages'].items():
        latest = max(pkg['versions'].values(),
                     key=lambda v: v['manifest']['versionCode'])
        env['apps'][name] = pkg['metadata']
        for key in ('versionCode', 'versionName'):
            env['apps'][name][key] = latest['manifest'][key]

    return env


def process_files(vars, files):
    autoesc = jinja2.select_autoescape()
    env = jinja2.Environment(loader=UndercomplicatedLoader(),
                             autoescape=lambda f: autoesc(target_filename(f)))
    env.filters['fromtimestamp_millis'] = fromtimestamp_millis_filter
    env.filters['strftime_millis'] = strftime_millis_filter

    for src in files:
        dest = target_filename(src)
        assert dest is not None
        with open(dest, 'w') as fh:
            env.get_template(src).stream(vars).dump(fh)


def main():
    parser = ArgumentParser()
    parser.add_argument('-f', '--fdroid-directory', required=True)
    parser.add_argument('files', nargs='*')
    args = parser.parse_args()

    for name in args.files:
        if target_filename(name) is None:
            parser.error('missing jinja2 file extension: %s' % (name,))

    process_files(read_fdroid(args.fdroid_directory), args.files)


if __name__ == '__main__':
    main()
