{{- /*
SPDX-FileCopyrightText: 2024 Univention GmbH
SPDX-License-Identifier: AGPL-3.0-only
*/}}

{{- /*
These template definitions are only used in this chart and do not relate to templates defined elsewhere.
*/}}
{{- define "keycloak-extensions.postgresql.connection.host" -}}
{{- if or .Values.postgresql.connection.host .Values.global.postgresql.connection.host -}}
{{- tpl ( coalesce .Values.postgresql.connection.host .Values.global.postgresql.connection.host ) . -}}
{{- else if .Values.global.nubusDeployment -}}
{{- printf "%s-postgresql" .Release.Name -}}
{{- else -}}
{{- required ".Values.postgresql.connection.host or .Values.global.postgresql.connection.host must be defined." (coalesce .Values.postgresql.connection.host .Values.global.postgresql.connection.host) -}}
{{- end -}}
{{- end -}}

{{- define "keycloak-extensions.postgresql.connection.port" -}}
{{- if or .Values.postgresql.connection.port .Values.global.postgresql.connection.port -}}
{{- tpl ( coalesce .Values.postgresql.connection.port .Values.global.postgresql.connection.port ) . -}}
{{- else -}}
5432
{{- end -}}
{{- end -}}

{{- define "keycloak-extensions.postgresql.auth.database" -}}
{{- if .Values.postgresql.auth.database -}}
{{- .Values.postgresql.auth.database -}}
{{- else if .Values.global.nubusDeployment -}}
keycloak_extensions
{{- else -}}
{{- required ".Values.postgresql.auth.database must be defined." .Values.postgresql.auth.database -}}
{{- end -}}
{{- end -}}

{{- define "keycloak-extensions.keycloak.connection.protocol" -}}
{{- if .Values.keycloak.connection.protocol -}}
{{- .Values.keycloak.connection.protocol -}}
{{- else -}}
http
{{- end -}}
{{- end -}}

{{- define "keycloak-extensions.keycloak.connection.host" -}}
{{- if .Values.keycloak.connection.host -}}
{{- .Values.keycloak.connection.host -}}
{{- else if .Values.global.nubusDeployment -}}
{{- printf "%s-keycloak" .Release.Name -}}
{{- else -}}
{{- required ".Values.keycloak.connection.host must be defined." .Values.keycloak.connection.host -}}
{{- end -}}
{{- end -}}

{{- define "keycloak-extensions.keycloak.connection.port" -}}
{{- if .Values.keycloak.connection.port -}}
{{- .Values.keycloak.connection.port -}}
{{- else -}}
8080
{{- end -}}
{{- end -}}

{{- define "keycloak-extensions.keycloak.connection.baseUrl" -}}
{{- $protocol := include "keycloak-extensions.keycloak.connection.protocol" . -}}
{{- $host := include "keycloak-extensions.keycloak.connection.host" . -}}
{{- $port := include "keycloak-extensions.keycloak.connection.port" . -}}
{{- printf "%s://%s:%s" $protocol $host $port -}}
{{- end -}}

{{- define "keycloak-extensions.keycloak.connection.authUrl" -}}
{{- $baseUrl := include "keycloak-extensions.keycloak.connection.baseUrl" . -}}
{{- printf "%s/admin" $baseUrl -}}
{{- end -}}

{{- define "keycloak-extensions.keycloak.auth.realm" -}}
{{- if .Values.keycloak.auth.realm -}}
{{- .Values.keycloak.auth.realm -}}
{{- else if .Values.global.nubusDeployment -}}
{{- coalesce .Values.keycloak.auth.realm .Values.global.keycloak.realm "nubus" -}}
{{- else -}}
{{- required ".Values.keycloak.auth.realm must be defined." .Values.keycloak.auth.realm -}}
{{- end -}}
{{- end -}}

{{- define "keycloak-extensions.keycloak.auth.masterRealm" -}}
{{- if .Values.keycloak.auth.masterRealm -}}
{{- .Values.keycloak.auth.masterRealm -}}
{{- else if .Values.global.nubusDeployment -}}
master
{{- else -}}
{{- required ".Values.keycloak.auth.masterRealm must be defined." .Values.keycloak.auth.masterRealm -}}
{{- end -}}
{{- end -}}

{{- define "keycloak-extensions.smtp.connection.host" -}}
{{- if .Values.smtp.connection.host -}}
{{- .Values.smtp.connection.host -}}
{{- else if .Values.global.nubusDeployment -}}
{{- printf "%s-smtp" .Release.Name -}}
{{- end -}}
{{- end -}}

{{- define "keycloak-extensions.smtp.connection.port" -}}
{{- if .Values.smtp.connection.port -}}
{{- .Values.smtp.connection.port -}}
{{- else -}}
587
{{- end -}}
{{- end -}}

{{- define "keycloak-extensions.ingress.certManagerIssuer" -}}
{{- if .Values.global.certManagerIssuer -}}
{{- .Values.global.certManagerIssuer -}}
{{- end -}}
{{- end -}}

{{- define "keycloak-extensions.ingress.ingressClassName" -}}
{{- required "Either .Values.proxy.ingress.ingressClassName or .Values.global.ingressClass must be defined. " (coalesce .Values.proxy.ingress.ingressClassName .Values.global.ingressClass) -}}
{{- end -}}

{{- define "keycloak-extensions.ingress.proxy.host" -}}
{{- if .Values.proxy.ingress.host -}}
{{- .Values.proxy.ingress.host -}}
{{- else if .Values.global.nubusDeployment -}}
{{- printf "%s.%s" .Values.global.subDomains.keycloak .Values.global.domain -}}
{{- end -}}
{{- end -}}

{{- define "keycloak-extensions.ingress.proxy.tls.secretName" -}}
{{- if .Values.proxy.ingress.tls.secretName -}}
{{- tpl .Values.proxy.ingress.tls.secretName . -}}
{{- else if .Values.global.nubusDeployment -}}
{{- printf "%s-keycloak-extensions-proxy-tls" .Release.Name -}}
{{- else -}}
{{- required ".Values.proxy.ingress.tls.secretName must be defined." .Values.proxy.ingress.tls.secretName -}}
{{- end -}}
{{- end -}}
