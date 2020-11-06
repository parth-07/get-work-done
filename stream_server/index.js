const express = require('express');
const mustacheExpress = require('mustache-express');
const {StatusCodes} = require('http-status-codes');
const serveIndex = require('serve-index');
const app = express();

app.set('views',__dirname+'/views');
app.set('view engine','mustache');
app.engine('mustache',mustacheExpress());

app.use('/public',express.static('public'),serveIndex('public',{
    icons : true
}));

app.get('/',(req,res,next) => {
    res.status(StatusCodes.OK).send('Okaeri');
})

module.exports = app;