# Github workflow and actions

This repository contains github actions and reusable workflows to
automatically rebuild Android apps and add them to an F-Droid
repository hosted via github pages.

## Setup

To use this repository, first set up a
[Github Pages](https://pages.github.com/) repository following the
instructions in the [example-page](example-page/) directory.

Then set up apps repositories following the instructions in the
[example-app](example-app/) directory. Finally push a tag to an app
repository and the app will be built, attached to a new Github
release, and added to your F-Droid repository.
