import os
import logging
import flask


class Fingerprint:

    def __init__(self):
        self.script = """<script>
      // Initialize the agent at application startup.
      const fpPromise = import('/fingerprintjs/v3')
        .then(FingerprintJS => FingerprintJS.load())

      // Get the visitor identifier when you need it.
      fpPromise
        .then(fp => fp.get())
        .then(result => {
          // This is the visitor identifier:
          const visitorId = result.visitorId
          console.log(visitorId)
          document.cookie = 'DEVICE_FINGERPRINT=' + visitorId+ ';path=/';
        })
        </script> """.encode()

        # Configure logging
        log_level = os.environ.get('LOG_LEVEL', 'INFO')
        logging.basicConfig(
            format='%(asctime)s %(levelname)s %(message)s',
            datefmt='%d/%m/%Y %I:%M:%S',
            level=log_level)
        self.logger = logging.getLogger(__name__)

    def inject_fingerprint(self, r, backend_headers):
        """
        Injects fingerprintjs script into the html
        """
        response = None
        self.logger.info("Injecting fingerprintjs script")
        response = flask.Response(
            r.content + self.script, r.status_code, headers=backend_headers)
        return response
