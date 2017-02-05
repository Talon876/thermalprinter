var pixelSize = 8;

function getMousePos(canvas, evt) {
    var rect= canvas.getBoundingClientRect();
    var x = evt.clientX - rect.left;
    var y = evt.clientY - rect.top;
    return {
        x: x,
        y: y,
        tX: Math.floor(x / pixelSize),
        tY: Math.floor(y / pixelSize),
    };
}

function fillRect(ctx, color, tileX, tileY) {
    ctx.fillStyle = color;
    ctx.fillRect(tileX * pixelSize, tileY * pixelSize, pixelSize, pixelSize);
}

function strokeRect(ctx, color, tileX, tileY) {
    ctx.strokeStyle = color;
    ctx.strokeRect(tileX * pixelSize, tileY * pixelSize, pixelSize, pixelSize);
}


var bitmap = [];
function init(width, height) {
    bitmap = [];
    for (var row = 0; row < height; row++) {
        var line = [];
        for (var i = 0; i < width; i++) {
            line.push(0);
        }
        bitmap.push(line);
    }
}

function render(ctx, canvas) {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    bitmap.forEach(function(row, y) {
        row.forEach(function(col, x) {
            var pixel = bitmap[y][x];
            if (pixel === 1) {
                fillRect(ctx, 'black', x, y);
            }
        });
    });
    document.getElementById('out').innerHTML = pack();
}

function pack() {
    var idx = 0;
    var data = [];
    bitmap.forEach(function(row, y) {
        row.forEach(function(col, x) {
            var pixel = bitmap[y][x];
            data.push(pixel);
            idx += 1;
        });
    });

    var imageString = data.join('');
    var chunks = imageString.match(/.{1,32}/g);
    var packedChunks = chunks.map(function(chunk) {
        var binaryNum = parseInt(chunk, 2);
        var decimalNum = binaryNum.toString(16);
        return decimalNum;
    });
    return packedChunks.join('-');
}

(function() {
    var canvas = document.getElementById('app');
    var ctx = canvas.getContext('2d');
    var imageWidth = canvas.width / pixelSize;
    var imageHeight = canvas.height / pixelSize;
    init(imageWidth, imageHeight);
    render(ctx, canvas);

    var handleEvent = function(e) {
        var mouse = getMousePos(canvas, e);
        render(ctx, canvas);
        if (e.which === 1) {
            bitmap[mouse.tY][mouse.tX] = 1;
        } else if (e.which === 3) {
            bitmap[mouse.tY][mouse.tX] = 0;
            render(ctx, canvas);
        } else {
            ctx.fillStyle = 'yellow';
            ctx.fillRect(mouse.tX * pixelSize + 1, mouse.tY * pixelSize + 1, pixelSize - 2, pixelSize - 2);
        }
    };

    canvas.onmousemove = handleEvent;
    canvas.onclick = handleEvent;
    canvas.oncontextmenu = function(e) {
        e.preventDefault();
    };
    document.getElementById('clear').onclick = function(e) {
        init(imageWidth, imageHeight);
        render(ctx, canvas);
    };
})();
