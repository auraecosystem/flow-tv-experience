```js
var url = 'https://api.sketchfab.com/v3/models/49d97ca2fbf34f85b6c88ae8ebc7514f/download';
var options = {
    method: 'GET',
    headers: {
        Authorization: 'Bearer {INSERT_OAUTH_ACCESS_TOKEN_HERE}',
    },
    mode: 'cors'
};

fetch(url, options).then(function(response){
    return response.json();
}).then(function(data){
    console.log(data);
});

# This request will return something like:
```ja
{
    "gltf": {
        "url": "https://sketchfab-prod-media.s3.amazonaws.com/archives/799f8c4511f84fab8c3f12887f7e6b36/gltf/...",
        "size": 45388265,
        "expires": 300
    },
    "usdz": {
        "url": "https://sketchfab-prod-media.s3.amazonaws.com/archives/799f8c4511f84fab8c3f12887f7e6b36/usdz/...",
        "size": 6394777,
        "expires": 300
    }
}
```

# The response contains all the information needed to download the archive. All you need to do is request the URL contained in gltf.url to download the archive.

IMPORTANT: The archive URL is only valid for a short period of time. Your application shouldn’t cache it.

Downloading a model archive

To download the zip archive, you can make a HTTP GET request to the url provided by the /v3/models/{uid}/download endpoint. Instead of making the request yourself, we recommend using zip.js which will download the file and decompress it into memory.
```bash
<!-- Download zip.js from https://gildas-lormeau.github.io/zip.js/ -->
<script type="text/javascript" src="/lib/zip.js"></script>
<script type="text/javascript" src="/lib/zip-ext.js"></script>
zip.workerScriptsPath = '/lib/';
var reader = new zip.HttpReader(url);
zip.createReader(
    reader,
    function(zipReader) {
        zipReader.getEntries(function(entries){
            console.log(entries);
        });
    },
    function(error) {
        console.error(error);
    }
);
```
# This will return an array of entries that represent files in the zip. It looks something like this:
```
[
    ...,
    {
        "_worker": {
            "crcTime": 0,
            "codecTime": 0
        },
        "version": 788,
        "bitFlag": 0,
        "compressionMethod": 8,
        "lastModDateRaw": 1267768440,
        "lastModDate": "2017-12-16T18:35:48.000Z",
        "crc32": 2072282119,
        "compressedSize": 9978,
        "uncompressedSize": 73359,
        "filenameLength": 10,
        "extraFieldLength": 0,
        "commentLength": 0,
        "directory": false,
        "offset": 341906,
        "filename": "scene.gltf",
        "comment": ""
    },
    ...
]
```
Loading a USDZ model

iOS devices can open USDZ file URLs directly in Safari. For more details, visit the USDZ documentation from Apple and Pixar.

Loading a glTF model

Once the archive has been downloaded and unzipped, all unzipped files are stored in memory as Entry objects.

If your app is using a 3D framework, it probably has a glTF plugin for reading glTF files:

````three.js GLTF Loader
````babylon.js
.glTF File loader plugin
````OSG.JS

```

//  The final step is to convert the Entry objects into something that these frameworks can load

# Generating URLs for every Entry

# First, write the Entry content to Blob objects and generate URLs for each Blob:
```js
entry.getData(new zip.BlobWriter('text/plain'), function onEnd(data) {
    var url = window.URL.createObjectURL(data);
    console.log(url);
});
This will generate URLs that look like this:

blob:http://example.com/59b3c659-d042-4a7f-bfb9-5c4c798fc0ed
Rewriting paths to URLs in scene.gltf

A glTF file is actually a JSON file. It contains all the information about the model, and links to other resources like geometry buffers and images. You will then need to rewrite the path of these resources to point to the URLs generated in the previous step.

// sceneFileContent is the content of scene.gltf
// and fileUrls is a key/value object,
// keys being filenames and values being corresponding URLs

var json = JSON.parse(sceneFileContent);

// Replace original buffers and images by blob URLs
if (json.hasOwnProperty('buffers')) {
    for (var i = 0; i < json.buffers.length; i++) {
        json.buffers[i].uri = fileUrls[json.buffers[i].uri];
    }
}

if (json.hasOwnProperty('images')) {
    for (var i = 0; i < json.images.length; i++) {
        json.images[i].uri = fileUrls[json.images[i].uri];
    }
}

var updatedSceneFileContent = JSON.stringify(json, null, 2);
var updatedBlob = new Blob([updatedSceneFileContent], { type: 'text/plain' });
var updatedUrl = window.URL.createObjectURL(updatedBlob);
// -> blob:http://example.com/a9b5c659-b032-4b7e-df19-5c42798fc049
Once all paths have been replaced, you can pass the URL of the updated scene.gltf file to your 3D framework to load the model.

// three.js

// URL corresponding to scene.gltf
var url = 'blob:http://example.com/a9b5c659-b032-4b7e-df19-5c42798fc049';

var loader = new THREE.GLTFLoader();
loader.load(url, function(gltf){
    scene.add( gltf.scene );
}, undefined, function(error){
    console.error( error );
});
// babylon.js

// URL corresponding to scene.gltf
var url = 'blob:http://example.com/a9b5c659-b032-4b7e-df19-5c42798fc049';

BABYLON.SceneLoader.ImportMesh('', '', url, scene, function onSuccess() {
    console.log('Loaded');
}, function onProgress() {
    console.log('Progress');
}, function onError(e) {
    console.error(e);
}, '.gltf');
