const express = require('express');
const mustacheExpress = require('mustache-express');
const {StatusCodes} = require('http-status-codes');
const serveIndex = require('serve-index');
const url = require('url');
const path = require('path');

const app = express();

app.set('views',__dirname+'/views');
app.set('view engine','mustache');
app.engine('mustache',mustacheExpress());

// const PUBLIC = '/media/parth/8050EED950EED4C6/Movies';
const PUBLIC = 'public';

app.use('/public',serveIndex(PUBLIC,{
    icons : true
}));

app.get('/',(req,res,next) => {
    res.status(StatusCodes.OK).send('Okaeri');
})

/* app.get('/public/[a-zA-Z0-9%/\(\).]+',(req,res,next) => {
    let name = req.url;
    console.log(name);
    // res.render('displayVideo.mustache',{
    //     videoName : "The fault in our stars",
    //     videoSource : videoSource,
    //     subtitleSource : subtitleSource
    // });
}); */

app.use((req,res,next)=>{
    req.url = decodeURI(req.url);
    console.log(req.url);
    let fileName = req.url.slice(1);
    let videoName = path.basename(fileName);
    let videoSource = fileName;
    // let subtitleSource = videoName+'.vtt';
    let subtitleSource= '';
    res.render('displayVideo.mustache',{
        videoName : "The fault in our stars",
        videoSource : videoName,
        subtitleSource : subtitleSource
    });
})

module.exports = app;