# -*- mode: Python -*-

config.define_string(
    "univention-project-username",
    args=False,
    usage="Username for Univention project at gitlab.souvap-univention.de"
)
config.define_string(
    "gitlab-access-token",
    args=False,
    usage="Access token from gitlab.souvap-univention.de with read_registry scope"
)
cfg = config.parse()

univention_project_username = cfg.get("univention-project-username")
if not univention_project_username:
    print("Please specify a username for the Univention project at gitlab.souvap-univention.de")
    exit("No username specified")

gitlab_access_token = cfg.get("gitlab-access-token")
if not gitlab_access_token:
    print("Please specify an access token from gitlab.souvap-univention.de with read_registry scope")
    exit("No access token specified")

# Defaults to `gaia` cluster
allow_k8s_contexts('kubernetes-admin@cluster.local')

namespace = k8s_namespace()
if namespace == 'default':
    print("Please specify a namespace in the Kubeconfig")
    exit("No namespace specified")

docker_build(
    'registry.souvap-univention.de/souvap/tooling/images/keycloak-extensions/keycloak-handler:development',
    'handler',
    dockerfile='docker/keycloak-handler/Dockerfile',
)

docker_build(
    'registry.souvap-univention.de/souvap/tooling/images/keycloak-extensions/keycloak-proxy:development',
    'proxy',
    dockerfile='docker/keycloak-proxy/Dockerfile',
)

local("""
    kubectl get secret --namespace {namespace} | grep souvap-gitlab || \
    kubectl create secret docker-registry souvap-gitlab --docker-server=registry.souvap-univention.de --docker-username={univention_project_username} --docker-password={gitlab_access_token} -n {namespace}
    """.format(
    univention_project_username=univention_project_username,
    gitlab_access_token=gitlab_access_token,
    namespace=namespace
))

local("helm get values ums-keycloak-extensions --namespace {namespace} > keycloak-extensions-values.yaml".format(namespace=namespace))

k8s_yaml(
    helm(
        "helm/keycloak-extensions",
        name='ums-keycloak-extensions',
        namespace=namespace,
        values='keycloak-extensions-values.yaml',
        set=[
            'global.imagePullSecrets[0]=souvap-gitlab',
            'handler.image.imagePullPolicy=Always',
            'handler.image.registry=registry.souvap-univention.de',
            'handler.image.repository=souvap/tooling/images/keycloak-extensions/keycloak-handler',
            'handler.image.tag=development',
            'proxy.image.imagePullPolicy=Always',
            'proxy.image.registry=registry.souvap-univention.de',
            'proxy.image.repository=souvap/tooling/images/keycloak-extensions/keycloak-proxy',
            'proxy.image.tag=development',
        ]
    )
)
