# Pages setup

First create a new [Github Pages](https://pages.github.com/) repository.

## Token

Next create a
[Personal Access Token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens).
This will be used to allow workflows in app repos to commit to the
pages repo.

Under your Github user settings scroll down to find Developer
Settings, then Personal Access Tokens, then Fine-grained
tokens. Generate a new token which is only allowed to access your
pages repo, with permissions allowing read-write for Contents.

Save this token somewhere safe for when you set up an app repo, or
come back here later and create one token for each app repo.

## Keys

Next create a new F-Droid signing key using the java keystore utility:
```
keytool -genkey -v -keystore my-keystore.p12 -alias my-key-alias -dname 'CN=my-name, OU=my-org' -keyalg RSA -keysize 4096 -validity 10000 -sigalg SHA256withRSA -storetype pkcs12 
```
Use the same password for the keystore and the key itself.

Navigate to your pages repository Settings -> Secrets and variables ->
Actions. Add a secret named FDROID_KEYSTORE_PASSWORD containing the
password for the keystore.

Encode the keystore using base64 add it as a secret named FDROID_KEYSTORE_BASE64:
```
openssl enc -base64 -A < my-keystore.p12
```

## Configuration file

Adapt the F-Droid example [config.yml](config.yml) file and commit it
to your pages repo.

## Workflow file

Adapt the [update-workflow.yaml](update-workflow.yaml) file as needed
and commit it to your pages repo in the .github/workflows/ directory.

## Template files

Create one or more
[Jinja2](https://jinja.palletsprojects.com/en/stable/templates/)
template files, for example [index.html.jinja2](index.html.jinja2)
and [README.md.jinja2](example-README.md.jinja2). These files must end
with the .jinja2 or .j2 file extension.

Whenever the repo is updated, these templates will be processed and
the result saved into a filename with the .jinja2 or .j2 extension
removed, overwriting whatever file existed there before.

In addition to the standard features mentioned in the
[Jinja2 documentation](https://jinja.palletsprojects.com/en/stable/templates/),
the following filters are available:
- fromtimestamp_millis: Converts a UTC timestamp in milliseconds, such
  as is found in the fdroid metadata, into a python datetime object.
- strftime_millis: With one argument, calls .strftime(arg) on the result
  of the fromtimestamp_millis filter. With no arguments, calls .ctime()

Several variables will be defined as well:
- repo_name: From the fdroid configuration file.
- repo_description: From the fdroid configuration file.
- repo_url: From the fdroid configuration file.
- repo_fingerprint: Fingerprint of the fdroid repository signing certificate.
- repo_url_full: Full repo url with [fdroid.link](https://fdroid.link/)
  prefix and certificate fingerprint.
- repo: From the fdroid index-v2.json metadata. Includes the following keys:
  - address
  - description
  - icon
  - name
  - timestamp
- apps: Dictionary mapping app's package name to app's metadata. All
  app metadata keys from the index-v2.json file are included, such as:
  - added
  - lastUpdated
  - authorName
  - name
  - sourceCode
  - webSite
  Additionally the newest version numbers are included:
  - versionCode
  - versionName

## Updating

The F-Droid repository and templated files will be automatically
regenerated whenever anything is pushed to the branches specified in
the workflow file. Edit the configuration file or a .jinja2 file,
commit, push, then wait a minute or so.
