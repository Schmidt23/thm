#!/bin/bash

for i in $(seq 0 100); do
	printf "%s\n" "$i" | md5sum | awk '{print $1}' >> md5_wordlist.txt 
done
