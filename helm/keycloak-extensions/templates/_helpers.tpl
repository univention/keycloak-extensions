{{- /*
SPDX-FileCopyrightText: 2024 Univention GmbH
SPDX-License-Identifier: AGPL-3.0-only
*/}}

{{- /*
These template definitions are only used in this chart and do not relate to templates defined elsewhere.
*/}}
{{- define "keycloak-extensions.postgresql.connection.host" -}}
{{- if .Values.postgresql.connection.host -}}
{{- .Values.postgresql.connection.host -}}
{{- else if .Values.global.nubusDeployment -}}
{{- printf "%s-postgresql" .Release.Name -}}
{{- else -}}
{{- required ".Values.postgresql.connection.host must be defined." .Values.postgresql.connection.host -}}
{{- end -}}
{{- end -}}

{{- define "keycloak-extensions.postgresql.connection.port" -}}
{{- if .Values.postgresql.connection.port -}}
{{- .Values.postgresql.connection.port -}}
{{- else -}}
5432
{{- end -}}
{{- end -}}

{{- define "keycloak-extensions.postgresql.auth.username" -}}
{{- if .Values.postgresql.auth.username -}}
{{- .Values.postgresql.auth.username -}}
{{- else if .Values.global.nubusDeployment -}}
keycloak_extensions
{{- else -}}
{{- required ".Values.postgresql.auth.username must be defined." .Values.postgresql.auth.username -}}
{{- end -}}
{{- end -}}

{{- define "keycloak-extensions.postgresql.auth.credentialSecret.name" -}}
{{- if .Values.postgresql.auth.credentialSecret.name -}}
{{- .Values.postgresql.auth.credentialSecret.name -}}
{{- else if .Values.global.nubusDeployment -}}
{{- printf "%s-keycloak-extensions-postgresql-credentials" .Release.Name -}}
{{- end -}}
{{- end -}}

{{- define "keycloak-extensions.postgresql.auth.password" -}}
{{- if .Values.postgresql.auth.credentialSecret.name -}}
valueFrom:
  secretKeyRef:
    name: {{ .Values.postgresql.auth.credentialSecret.name | quote }}
    key: {{ .Values.postgresql.auth.credentialSecret.key | quote }}
{{- else if .Values.global.nubusDeployment -}}
valueFrom:
  secretKeyRef:
    name: {{ include "keycloak-extensions.postgresql.auth.credentialSecret.name" . | quote }}
    key: {{ .Values.postgresql.auth.credentialSecret.key | quote }}
{{- else -}}
value: {{ required ".Values.postgresql.auth.password is required." .Values.postgresql.auth.password | quote }}
{{- end -}}
{{- end -}}

{{- define "keycloak-extensions.postgresql.auth.database" -}}
{{- if .Values.postgresql.auth.database -}}
{{- .Values.postgresql.auth.database -}}
{{- else if .Values.global.nubusDeployment -}}
keycloak
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

{{- define "keycloak-extensions.keycloak.auth.username" -}}
{{- if .Values.keycloak.auth.username -}}
{{- .Values.keycloak.auth.username -}}
{{- else if .Values.global.nubusDeployment -}}
kcadmin
{{- else -}}
{{- required ".Values.keycloak.auth.username must be defined." .Values.keycloak.auth.username -}}
{{- end -}}
{{- end -}}

{{- define "keycloak-extensions.keycloak.auth.credentialSecret.name" -}}
{{- if .Values.keycloak.auth.credentialSecret.name -}}
{{- .Values.keycloak.auth.credentialSecret.name -}}
{{- else if .Values.global.nubusDeployment -}}
{{- printf "%s-keycloak-extensions-keycloak-credentials" .Release.Name -}}
{{- end -}}
{{- end -}}

{{- define "keycloak-extensions.keycloak.auth.password" -}}
{{- if .Values.keycloak.auth.credentialSecret.name -}}
valueFrom:
  secretKeyRef:
    name: {{ .Values.keycloak.auth.credentialSecret.name | quote }}
    key: {{ .Values.keycloak.auth.credentialSecret.key | quote }}
{{- else if .Values.global.nubusDeployment -}}
valueFrom:
  secretKeyRef:
    name: {{ include "keycloak-extensions.keycloak.auth.credentialSecret.name" . | quote }}
    key: {{ .Values.keycloak.auth.credentialSecret.key | quote }}
{{- else -}}
value: {{ required ".Values.keycloak.auth.password is required." .Values.keycloak.auth.password | quote }}
{{- end -}}
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

{{- define "keycloak-extensions.smtp.auth.username" -}}
{{- .Values.smtp.auth.username -}}
{{- end -}}

{{- define "keycloak-extensions.smtp.auth.credentialSecret.name" -}}
{{- if .Values.smtp.auth.credentialSecret.name -}}
{{- .Values.smtp.auth.credentialSecret.name -}}
{{- else if .Values.global.nubusDeployment -}}
{{- printf "%s-keycloak-extensions-smtp-credentials" .Release.Name -}}
{{- end -}}
{{- end -}}

{{- define "keycloak-extensions.smtp.auth.password" -}}
{{- if .Values.smtp.auth.credentialSecret.name -}}
valueFrom:
  secretKeyRef:
    name: {{ .Values.smtp.auth.credentialSecret.name | quote }}
    key: {{ .Values.smtp.auth.credentialSecret.key | quote }}
{{- else if .Values.global.nubusDeployment -}}
valueFrom:
  secretKeyRef:
    name: {{ include "keycloak-extensions.smtp.auth.credentialSecret.name" . | quote }}
    key: {{ .Values.smtp.auth.credentialSecret.key | quote }}
{{- else -}}
value: {{ .Values.smtp.auth.password | quote }}
{{- end -}}
{{- end -}}

{{- define "keycloak-extensions.captcha.credentialSecret.name" -}}
{{- if .Values.smtp.auth.credentialSecret.name -}}
{{- .Values.smtp.auth.credentialSecret.name -}}
{{- else if .Values.global.nubusDeployment -}}
{{- printf "%s-keycloak-extensions-captcha-credentials" .Release.Name -}}
{{- end -}}
{{- end -}}

{{- define "keycloak-extensions.captcha.captchaSiteKey" -}}
{{- if .Values.proxy.appConfig.captcha.credentialSecret.name -}}
valueFrom:
  secretKeyRef:
    name: {{ .Values.proxy.appConfig.captcha.credentialSecret.name | quote }}
    key: {{ .Values.proxy.appConfig.captcha.credentialSecret.siteKeyKey | quote }}
{{- else -}}
value: {{ required ".Values.proxy.appConfig.captcha.captchaSiteKey required." .Values.proxy.appConfig.captcha.captchaSiteKey | quote }}
{{- end -}}
{{- end -}}

{{- define "keycloak-extensions.captcha.captchaSecretKey" -}}
{{- if .Values.proxy.appConfig.captcha.credentialSecret.name -}}
valueFrom:
  secretKeyRef:
    name: {{ .Values.proxy.appConfig.captcha.credentialSecret.name | quote }}
    key: {{ .Values.proxy.appConfig.captcha.credentialSecret.secretKeyKey | quote }}
{{- else -}}
value: {{ required ".Values.proxy.appConfig.captcha.captchaSecretKey required." .Values.proxy.appConfig.captcha.captchaSecretKey | quote }}
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
{{- if .Values.global.nubusDeployment -}}
{{- printf "%s-keycloak-extensions-proxy-tls" .Release.Name -}}
{{- else -}}
{{- required ".Values.proxy.ingress.tls.secretName must be defined." .Values.proxy.ingress.tls.secretName -}}
{{- end -}}
{{- end -}}
