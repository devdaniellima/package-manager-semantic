#!/bin/bash
echo '@@@' > package_list_info.txt

for package in $(cat package_list.txt)
do
  echo $package
  { apt-cache show $package && (apt show $package | grep 'APT-Sources: ') && echo '@@@'; } >> package_list_info.txt
done