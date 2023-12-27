/*
 * SPDX-License-Identifier: AGPL-3.0-only
 * SPDX-FileCopyrightText: 2023 Univention GmbH
 */

package de.univention.keycloak.server;

import org.keycloak.common.Version;
import org.keycloak.testsuite.KeycloakServer;

import java.text.SimpleDateFormat;
import java.util.Date;

public class EmbeddedServer {

    public static void main(String[] args) throws Throwable {

    	System.out.println("Starting Keycloak Test Server");
        Version.BUILD_TIME = new SimpleDateFormat("yyyy-MM-dd HH:mm").format(new Date());

        KeycloakServer.bootstrapKeycloakServer(args);
    }

}
