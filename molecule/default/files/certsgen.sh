#!/usr/bin/env bash
CANAME=ca
CERTS=( "ca" "server" "$@" )
FOLDER="files/certs"
mkdir -p $FOLDER

if [[ " ${CERTS[*]} " =~ ${CANAME} ]]; then
	echo Generate Root CA cert, key
	# Create a key-pair that will serve both as the root CA and the server key-pair
	# the "ca.crt" name is used to match what it expects later
	openssl req -new -x509 -days 365 -nodes -out "$FOLDER/$CANAME.crt" \
		-keyout "$FOLDER/$CANAME.key" -subj "/CN=$CANAME"

	CERTS=( "${CERTS[@]/$CANAME}" )
fi

for CLIENT in "${CERTS[@]}"
do
	if [ -n "$CLIENT" ]; then
		# Create the client key and CSR and sign with root key
		openssl req -new -nodes -out "$FOLDER/$CLIENT.csr" \
		  -keyout "$FOLDER/$CLIENT.key" -subj "/CN=$CLIENT"

		openssl x509 -req -in "$FOLDER/$CLIENT.csr" -days 365 \
			-CA "$FOLDER/$CANAME.crt" -CAkey "$FOLDER/$CANAME.key" -CAcreateserial \
			-out "$FOLDER/$CLIENT.crt"
	fi
done
chmod og-rwx $FOLDER/*
