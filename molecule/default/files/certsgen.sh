#!/bin/bash
CANAME=root-ca
CERTS=( root-ca $@ )

# mkdir -p certs

if [[ " ${CERTS[*]} " =~ " ${CANAME} " ]]; then
	echo Generate Root CA cert, key
	# Create a key-pair that will serve both as the root CA and the server key-pair
	# the "ca.crt" name is used to match what it expects later
	openssl req -new -x509 -days 365 -nodes -out certs/ca.crt \
		-keyout certs/ca.key -subj "/CN=$CANAME"
	
	CERTS=( "${CERTS[@]/$CANAME}" )
fi

for CLIENT in "${CERTS[@]}"
do
	# Create the client key and CSR and sign with root key
	openssl req -new -nodes -out certs/$CLIENT.csr \
	  -keyout certs/$CLIENT.key -subj "/CN=$CLIENT"

	openssl x509 -req -in certs/$CLIENT.csr -days 365 \
	    -CA certs/ca.crt -CAkey certs/ca.key -CAcreateserial \
	    -out certs/$CLIENT.crt
done
chmod og-rwx certs/*

