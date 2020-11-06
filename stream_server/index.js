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

app.use('/content',express.static(PUBLIC));

app.get('/',(req,res,next) => {
    res.status(StatusCodes.OK).send('Okaeri');
})

app.use((req,res,next)=>{
    req.url = decodeURI(req.url);
    req.url = req.url.replace('public','content');
    console.log(req.url);
    let fileName = '/'+req.url.slice(1);
    let videoName = path.basename(fileName);
    let videoSource = fileName;
    let subtitleSource = fileName.replace('.mp4','.vtt');
    res.render('displayVideo.mustache',{
        videoName : "The fault in our stars",
        videoSource : fileName,
        subtitleSource : subtitleSource
    });
})

module.exports = app;