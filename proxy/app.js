const express = require("express");
var cookieParser = require('cookie-parser');



const { proxy } = require("./routes");
const { logger } = require("./utils");
  
var app = express();
app.use(express.static('public'));
app.use(cookieParser());

/**
 * @name /test
 * @desc
 * Simple endpoint to check if everything is working
 */
app.get("/test", function (req, res) {
    res.send("<p>Hello</p>");
  });

/**
 * @name /
 * @desc
 * Proxy endpoint to handle all requests
 */
app.use("/", proxy);



var server = app.listen(process.env.PORT, function () {
    var host = server.address().address;
    var port = server.address().port;
    logger.info(`Proxy running at http://${host}:${port}`);
  });
  
  