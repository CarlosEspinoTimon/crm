#!/bin/bash

# File where changes are going to be made
file="$1"

# Replacements to do
sed -i "s*YOUR_DATABASE_URI*${DATABASE_URI}*" "$file"
echo "1"
sed -i "s*YOUR_GOOGLE_CLIENT_ID*${GOOGLE_CLIENT_ID}*" "$file"
echo "2"
sed -i "s*YOUR_GOOGLE_CLIENT_SECRET*${GOOGLE_CLIENT_ID_SECRECT}*" "$file"
echo "3"
sed -i "s*YOUR_GOOGLE_APPLICATION_CREDENTIALS*${GOOGLE_APPLICATION_CREDENTIALS}*" "$file"
echo "4"
sed -i "s*YOUR_GOOGLE_PROJECT*${GOOGLE_PROJECT}*" "$file"
echo "5"
sed -i "s*YOUR_GOOGLE_BUCKET*${GOOGLE_BUCKET}*" "$file"
echo "6"
sed -i "s*YOUR_FACEBOOK_CLIENT_ID*${FACEBOOK_CLIENT_ID}*" "$file"
echo "7"
sed -i "s*YOUR_FACEBOOK_CLIENT_SECRET*${FACEBOOK_CLIENT_SECRET}*" "$file"
echo "8"
