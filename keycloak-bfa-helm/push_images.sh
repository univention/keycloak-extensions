#! /bin/sh

export ACCESS_TOKEN=<ENTER_TOKEN_HERE>
export REGISTRY_BASE=gitregistry.knut.univention.de/univention/customers/dataport/upx/pocs/keycloak-bfa-and-security-poc
export HANDLER_IMG=keycloak-extensions-handler:develop
export HANDLER_NEW_IMG=$REGISTRY_BASE:handler-develop

export PROXY_IMG=keycloak-extensions-proxy:develop
export PROXY_NEW_IMG=$REGISTRY_BASE:proxy-develop

docker tag $HANDLER_IMG $HANDLER_NEW_IMG
docker tag $PROXY_IMG $PROXY_NEW_IMG

docker login gitregistry.knut.univention.de -u irumyantsev -p $ACCESS_TOKEN

docker push $HANDLER_NEW_IMG
docker push $PROXY_NEW_IMG
