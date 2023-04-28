#!/bin/bash
CANAME=root-ca
CERTS=( root-ca $@ )
FOLDER="files/certs"
mkdir -p $FOLDER

if [[ " ${CERTS[*]} " =~ " ${CANAME} " ]]; then
	echo Generate Root CA cert, key
	# Create a key-pair that will serve both as the root CA and the server key-pair
	# the "ca.crt" name is used to match what it expects later
	openssl req -new -x509 -days 365 -nodes -out $FOLDER/ca.crt \
		-keyout $FOLDER/ca.key -subj "/CN=$CANAME"
	
	CERTS=( "${CERTS[@]/$CANAME}" )
fi

for CLIENT in "${CERTS[@]}"
do
	if [ ! -z "$CLIENT" ]; then
		# Create the client key and CSR and sign with root key
		openssl req -new -nodes -out $FOLDER/$CLIENT.csr \
		  -keyout $FOLDER/$CLIENT.key -subj "/CN=$CLIENT"

		openssl x509 -req -in $FOLDER/$CLIENT.csr -days 365 \
			-CA $FOLDER/ca.crt -CAkey $FOLDER/ca.key -CAcreateserial \
			-out $FOLDER/$CLIENT.crt
	fi
done
chmod og-rwx $FOLDER/*
