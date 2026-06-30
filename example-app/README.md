# App setup

First create a new Github repository for your app if it doesn't
already exist.

## Keys

Next create a new android app signing keystore, use either Android
Studio or the Java keytool utility:
```
keytool -genkey -v -keystore my-keystore.jks -alias my-key-alias -keyalg RSA -keysize 4096 -validity 10000
```
Use the same password for the keystore and the key itself.

Navigate to your app repository Settings -> Secrets and variables ->
Actions. Add a secret named APP_KEYSTORE_PASSWORD containing the
password for the keystore.

Encode the keystore using base64 add it as a secret named APP_KEYSTORE_BASE64:
```
openssl enc -base64 -A < my-keystore.jks
```

## Token

Add another secret named FDROID_PAGES_TOKEN containing a Personal
Access Token as described in the [pages README](../example-page/README.md).

## Gradle

Edit your app/build.gradle.kts file to merge in the
[example build.gradle.kts](build.gradle.kts) here. Gradle will now try
to read signing information from a keystore.properties file in the app
repository root. This file contains passwords and must not be
committed.

To mitigate the risk of accidentally committing a keystore.properties
file containing key passwords, add it to .gitignore:
```
echo /keystore.properties >> .gitignore
```

When building signed .apk files on your local machine, you will need to
create a keystore.properties file and keep a copy of your keystore on
your dev machine. You may wish to commit the
[keystore.properties.example](keystore.properties.example)
file into your app repository as a reminder of the format of this
file.

## F-Droid metadata

Adapt the example [fdroid-metadata.yml](fdroid-metadata.yml) file and
commit it to your app repo.

## Workflow files

Adapt the [debug-workflow.yaml](debug-workflow.yaml) and
[release-workflow.yaml](release-workflow.yaml) file as needed and
commit them to your app repo in the .github/workflows/ directory.

## Updating

A debug version of your app will be automatically build whenever
anything is pushed to the branches specified in the debug workflow
file. If you wish to make these debug builds easily accessable,
consider using the [nightly.link](https://nightly.link/) service.

When a tag matching the pattern specified in the release workflow is
pushed then a release version of the app will be build, a Github
release created with the .apk file attached, and the apk and updated
metadata committed to your pages repo. The pages repo will then update
itself.
