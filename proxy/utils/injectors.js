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
}



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
            `onsubmit="login.disabled = true; return true;"`,
            `onsubmit="login.disabled = true; if (grecaptcha.getResponse() === '') {console.log('Captcha not filled'); login.disabled = false; return false;} else {console.log('Captcha filled'); return true;}"`
        )
        .replace(
            `<div class="form-group login-pf-settings">`,
            `<div class="form-group" style="display:flex; justify-content:center; align-items:center">
                <div class="g-recaptcha" data-sitekey="${process.env.CAPTCHA_SITE_KEY}"></div>
            </div>
            <div class="form-group login-pf-settings">`
        );
}

// Other CAPTCHA support such as Cloudflare and so on would go here

module.exports = { injectFingerprintJS, injectGoogleCaptcha }