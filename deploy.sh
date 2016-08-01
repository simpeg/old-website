#!/bin/bash

if [ "$TRAVIS_BRANCH" = "master" -a "$TRAVIS_PULL_REQUEST" = "false" ]; then
  export GAE_PROJECT=simpegxyz
  export APP_VERSION="$(echo $TRAVIS_COMMIT | cut -c -7)"
  export PROMOTE=Yes
fi

if [ -z "$GAE_PROJECT" ]; then
  exit 0;
fi

# Unpack credentials
openssl aes-256-cbc -K $encrypted_050daccd65cb_key -iv $encrypted_050daccd65cb_iv \
  -in credentials.tar.gz.enc -d | tar -xzf -
cp credentials/${GAE_PROJECT}/* ./

# Do deploy
gcloud -q components update gae-python
gcloud auth activate-service-account --key-file client-secret.json
gcloud config set project $GAE_PROJECT
gcloud preview datastore create-indexes ./www/index.yaml --project $GAE_PROJECT
if [ "$PROMOTE" == "Yes" ]; then
  gcloud preview app deploy ./www/app.yaml --project $GAE_PROJECT --version $APP_VERSION --promote;
else
  gcloud preview app deploy ./www/app.yaml --project $GAE_PROJECT --version $APP_VERSION --no-promote;
fi
