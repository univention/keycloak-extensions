package de.univention.form.recaptcha.browser;

import org.keycloak.Config;
import org.keycloak.authentication.Authenticator;
import org.keycloak.authentication.authenticators.browser.UsernamePasswordFormFactory;
import org.keycloak.models.*;
import org.keycloak.provider.ProviderConfigProperty;

// import lombok.extern.jbosslog.JBossLog;

import java.util.ArrayList;
import java.util.List;

import static org.keycloak.authentication.forms.RegistrationRecaptcha.*;

public class UsernamePasswordFormRecaptchaAuthenticatorFactory extends UsernamePasswordFormFactory {
	
    protected static final String RECAPTCHA_REQUIRED_AUTH_NOTE = "IsRecaptchaRequired";
    protected static final String G_RECAPTCHA_RESPONSE = "g-recaptcha-response";
	protected static final String SITE_KEY = "site.key";
	protected static final String SITE_SECRET = "secret";

    public static final UsernamePasswordFormRecaptchaAuthenticator SINGLETON = new UsernamePasswordFormRecaptchaAuthenticator();

    public static final String PROVIDER_ID = "recaptcha-username-password-form";

    public static final AuthenticationExecutionModel.Requirement[] REQUIREMENT_CHOICES = {
            AuthenticationExecutionModel.Requirement.REQUIRED,
            AuthenticationExecutionModel.Requirement.DISABLED
    };


    private static final List<ProviderConfigProperty> CONFIG_PROPERTIES = new ArrayList<ProviderConfigProperty>();

    static {
        ProviderConfigProperty property;

        property = new ProviderConfigProperty();
        property.setName(SITE_KEY);
        property.setLabel("reCaptcha Site Key");
        property.setType(ProviderConfigProperty.STRING_TYPE);
        property.setHelpText("Google reCaptcha Site Key");
        CONFIG_PROPERTIES.add(property);

        property = new ProviderConfigProperty();
        property.setName(SITE_SECRET);
        property.setLabel("reCaptcha Secret");
        property.setType(ProviderConfigProperty.STRING_TYPE);
        property.setHelpText("Google reCaptcha Secret");
        CONFIG_PROPERTIES.add(property);
    }

    @Override
    public String getDisplayType() {
        return "Username Password Form With reCaptcha";
    }


    @Override
    public boolean isConfigurable() {
        return true;
    }

    @Override
    public AuthenticationExecutionModel.Requirement[] getRequirementChoices() {
        return REQUIREMENT_CHOICES;
    }

    @Override
    public boolean isUserSetupAllowed() {
        return true;
    }

    @Override
    public String getHelpText() {
        return "When a login request with header `X-SUSPICIOUS-REQUEST` set or not null, Google reCaptcha button is added to the interface. reCaptchas verify that registering is done by a human. The reCaptcha can only be used on systems which are connected to the Internet. When the reCaptcha is enabled, it requires further configuration.";
    }

    @Override
    public List<ProviderConfigProperty> getConfigProperties() {
        return CONFIG_PROPERTIES;
    }

    @Override
    public Authenticator create(KeycloakSession session) {
        return SINGLETON;
    }

    @Override
    public void init(Config.Scope config) {
    	System.out.println("Init");
    }

    @Override
    public void postInit(KeycloakSessionFactory factory) {

    }

    @Override
    public void close() {

    }

    @Override
    public String getId() {
        return PROVIDER_ID;
    }
}
