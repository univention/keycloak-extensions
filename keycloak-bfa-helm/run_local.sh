#! /bin/bash

LOCAL_CLUSTER_NAME=kc-bfa

kind create cluster -n kc-bfa

helm install --create-namespace --namespace kc-bfa dev .
