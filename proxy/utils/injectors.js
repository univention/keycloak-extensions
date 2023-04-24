/*
 * Like what you see? Join us!
 * https://www.univention.com/about-us/careers/vacancies/
 *
 * Copyright 2020-2023 Univention GmbH
 *
 * https://www.univention.de/
 *
 * All rights reserved.
 *
 * The source code of this program is made available
 * under the terms of the GNU Affero General Public License version 3
 * (GNU AGPL V3) as published by the Free Software Foundation.
 *
 * Binary versions of this program provided by Univention to you as
 * well as other copyrighted, protected or trademarked materials like
 * Logos, graphics, fonts, specific documentations and configurations,
 * cryptographic keys etc. are subject to a license agreement between
 * you and Univention and not subject to the GNU AGPL V3.
 *
 * In the case you use this program under the terms of the GNU AGPL V3,
 * the program is provided in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public
 * License with the Debian GNU/Linux or Univention distribution in file
 * /usr/share/common-licenses/AGPL-3; if not, see
 * <https://www.gnu.org/licenses/>.
 */

/**
 * Injects the JavaScript needed for FingerprintJS (v3)
 * into the provided Keycloak login page.
 * The return value is a valid HTML formatted string.
 * @param {string} html - The Keycloak login template HTML as string
 */
const injectFingerprintJS = (html) => {
  return html
    .replace(
      "</head>" ,
      `<script>
                // Initialize the agent at application startup.
                const fpPromise = import('/fingerprintjs/v3.js')
                    .then(FingerprintJS => FingerprintJS.load())

                // Get the visitor identifier when you need it.
                fpPromise
                    .then(fp => fp.get())
                    .then(result => {
                    // This is the visitor identifier:
                    const visitorId = result.visitorId;
                    document.cookie = 'DEVICE_FINGERPRINT=' + visitorId+ ';path=/;SameSite=None;Secure=false';
                    })
            </script>
            </head>`);
};



/**
 * Injects the JavaScript and HTML needed for Google reCAPTCHA
 * into the provided Keycloak login page.
 * The return value is a valid HTML formatted string.
 * @param {string} html - The Keycloak login template HTML as string
 */
const injectGoogleCaptcha = (html) => {
  return html
    .replace(
      "</head>",
      `<script src="https://www.google.com/recaptcha/api.js" async defer></script>
            </head>`)
    .replace(
      "onsubmit=\"login.disabled = true; return true;\"",
      "onsubmit=\"login.disabled = true; if (grecaptcha.getResponse() === '') {console.log('Captcha not filled'); login.disabled = false; return false;} else {console.log('Captcha filled'); return true;}\""
    )
    .replace(
      "<div class=\"form-group login-pf-settings\">",
      `<div class="form-group" style="display:flex; justify-content:center; align-items:center">
                <div class="g-recaptcha" data-sitekey="${process.env.CAPTCHA_SITE_KEY}"></div>
            </div>
            <div class="form-group login-pf-settings">`
    );
};

// Other CAPTCHA support such as Cloudflare and so on would go here

module.exports = { injectFingerprintJS, injectGoogleCaptcha };
