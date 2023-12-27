/*
 * SPDX-License-Identifier: AGPL-3.0-only
 * SPDX-FileCopyrightText: 2023 Univention GmbH
 */

package de.univention.form.recaptcha;

import com.sun.istack.Nullable;
import org.keycloak.models.AuthenticatorConfigModel;
import org.keycloak.representations.idm.OAuth2ErrorRepresentation;

import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;
import java.util.Map;

public class AuthenticatorUtil {

    public static String getConfigValue(@Nullable AuthenticatorConfigModel configModel, String configKey, String defaultValue) {
        if (configModel == null)
            return defaultValue;
        Map<String, String> configMap = configModel.getConfig();
        if (!configMap.isEmpty()) {
            String configValue = configMap.get(configKey);
            defaultValue = configValue == null ? "" : configValue;
        }
        return defaultValue;
    }

    public static Response errorResponse(Response.Status status, String error, String errorMessage) {
        OAuth2ErrorRepresentation errorRepresentation = new OAuth2ErrorRepresentation(error, errorMessage);
        return Response.status(status).entity(errorRepresentation).type(MediaType.APPLICATION_JSON_TYPE).build();
    }
}
