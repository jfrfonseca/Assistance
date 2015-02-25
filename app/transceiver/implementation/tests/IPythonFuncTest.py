%%javascript
require.config({
    paths: {
        'three': "http://cdnjs.cloudflare.com/ajax/libs/three.js/r69/three",
    }
});

%%javascript
require(['three'], function() {
    element.append(THREE.REVISION);
});
