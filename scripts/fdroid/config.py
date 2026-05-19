from argparse import ArgumentParser
import os

from cryptography.hazmat.primitives.serialization import pkcs12
import yaml


def main():
    parser = ArgumentParser()
    parser.add_argument('-a', '--key-alias', required=True)
    parser.add_argument('-k', '--keystore', required=True)
    parser.add_argument('-i', '--input', required=True)
    parser.add_argument('-p', '--passphrase-variable', required=True)
    parser.add_argument('-o', '--output', required=True)
    args = parser.parse_args()

    passwd = os.getenv(args.passphrase_variable)
    with open(args.keystore, 'rb') as fh:
        key, cert, extra = pkcs12.load_key_and_certificates(
            fh.read(), passwd.encode())

    with open(args.input, 'r') as fh:
        conf = yaml.safe_load(fh)

    conf.update({
        'keydname': cert.subject.rfc4514_string(),
        'keystore': os.path.abspath(args.keystore),
        'keystorepass': passwd,
        'keypass': passwd,
        'repo_keyalias': args.key_alias,
    })

    fd = os.open(args.output, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, 'w') as fh:
        yaml.safe_dump(conf, fh)


if __name__ == '__main__':
    main()
