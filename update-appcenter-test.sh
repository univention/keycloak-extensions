#!/bin/bash
#
# Also see https://docs.software-univention.de/app-center/5.0/en/configurations.html#installation-scripts
#

set -e
set -x

APP_VERSION="5.0/keycloak-extensions=0.9-ucs1"

selfservice () {
	local uri="https://provider-portal.software-univention.de/appcenter-selfservice/univention-appcenter-control"
	local first=$1
	shift

	# USERNAME="$USER"
	# [ -e "$HOME/.univention-appcenter-user" ] && USERNAME="$(< $HOME/.univention-appcenter-user)"

	# PWDFILE="~/.selfservicepwd"
	# [ -e "$HOME/.univention-appcenter-pwd" ] && PWDFILE="$HOME/.univention-appcenter-pwd"

	# curl -sSfL "$uri" | python2 - "$first" --username=${USERNAME} --pwdfile=${PWDFILE} "$@"
    curl -sSfL "$uri" | python3 - "$first" "$@"
}

die () {
	echo "$@"
	exit 0
}

[ "$IGN_GIT" != "true" ] && test -n "$(git status -s)" && die "Changes in repo, do not upload app! (to override: IGN_GIT=true)"

## Here we could e.g. generate the scripts from templates and adjust things, see e.g.:
## * https://git.knut.univention.de/univention/components/dashboard/admin-dashboard
## * https://git.knut.univention.de/univention/components/oidc-provider

## Some apps use templates to install additional files, e.g.:
cp appcenter/preinst.tmpl appcenter/preinst

# Now we replace the keywords with the contents
tar cjf - -C ./ reCaptcha-theme | base64 >> ./tmp_theme_b64
sed -i -e "/%ARCHIVE_CONTENT%/r ./tmp_theme_b64" -e "/%ARCHIVE_CONTENT%/d" appcenter/preinst

base64 reCaptcha-auth-flow/target/reCaptcha-auth-flow.jar >> ./tmp_jar_b64
sed -i -e "/%KEYCLOAK_RECAPTCHA_JAR%/r ./tmp_jar_b64" -e "/%KEYCLOAK_RECAPTCHA_JAR%/d" appcenter/preinst

## Now we can upload the files for the app to the provider-portal:
## The order of the arguments doesn't matter, the univention-appcenter-control script recongnizes the filenames and file extensions.
selfservice upload "$APP_VERSION" appcenter/compose appcenter/settings appcenter/preinst appcenter/configure_host appcenter/inst appcenter/env appcenter/test appcenter/ini appcenter/uinst

## There are more "magic" files that can be uploaded for specific purposes:
# selfservice upload "$APP_VERSION" app/compose app/settings app/preinst app/configure_host app/inst app/uinst app/env app/test app/setup README_*

## And finally they clean the working directory after upload
rm -f appcenter/preinst ./tmp_jar_b64 ./tmp_theme_b64
