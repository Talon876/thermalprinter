paper.install(window);
(function(){ Math.clamp = function(val,min,max){return Math.max(min,Math.min(max,val));} })();

var pixelSize = 16;
var bitmap = [];
var pencil;

var init = function(width, height) {
  bitmap = [];
  for (var row = 0; row < height; row++) {
    var line = [];
    for (var col = 0; col < width; col++) {
      var rect = new Path.Rectangle([col * pixelSize, row * pixelSize], [pixelSize, pixelSize]);
      line.push({rect: rect, value: 0});
    }
    bitmap.push(line);
  }
};

var toTile = function(point) {
  var tx = Math.clamp(Math.floor(point.x / pixelSize), 0, view.viewSize.width / pixelSize - 1);
  var ty = Math.clamp(Math.floor(point.y / pixelSize), 0, view.viewSize.height / pixelSize - 1);
  return {
    tX: tx,
    tY: ty,
    position: [tx * pixelSize + pixelSize/2,
               ty * pixelSize + pixelSize/2]
  }
};

var createIndicator = function() {
  var indicator = new Path.Rectangle([0, 0], [pixelSize, pixelSize]);
  indicator.fillColor = new Color(1, 1, 0, 0.5);
  indicator.strokeColor = 'black';
  indicator.strokeWidth = 2;
  return indicator;
};

var createPencil = function(indicator) {
  pencil = new Tool();
  pencil.onMouseDown = function(event) {
    var tilePoint = toTile(event.point);
    indicator.position = tilePoint.position;
    var pixel = bitmap[tilePoint.tY][tilePoint.tX];

    if (event.event.which === 1) {
      pixel.rect.fillColor = 'black';
      pixel.value = 1;
    } else if (event.event.which === 3) {
      pixel.rect.fillColor = 'white';
      pixel.value = 0;
    }
  };
  pencil.onMouseDrag = pencil.onMouseDown;
  pencil.onMouseUp = function(event) {
    indicator.bringToFront();
  };
  pencil.onMouseMove = function(event) {
    var tilePoint = toTile(event.point);
    indicator.position = tilePoint.position;
  };
};

var setup = function(pxWidth, pxHeight) {
  view.viewSize = [pxWidth, pxHeight];
  init(pxWidth / pixelSize, pxHeight / pixelSize);
};

var pack = function() {
  var data = [];
  bitmap.forEach(function(row, y) {
    row.forEach(function(col, x) {
      var pixel = bitmap[y][x];
      data.push(pixel.value);
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
};

$(document).ready(function() {
  var canvas = document.getElementById('app');
  var width = canvas.width;
  var height = canvas.height;
  canvas.oncontextmenu = function(e) {
    e.preventDefault();
  };
  paper.setup(canvas);
  setup(width, height);

  var indicator = createIndicator();
  createPencil(indicator);

  document.getElementById('clear').onclick = function(e) {
    bitmap.forEach(function(row, y) {
      row.forEach(function(col, x) {
        var pixel = bitmap[y][x];
        pixel.rect.fillColor = 'white';
        pixel.value = 0;
      });
    });
  };

  document.getElementById('save').onclick = function(e) {
    var imageCode = pack();
    console.log(imageCode);
  }

  pencil.activate();
  view.draw();
});

