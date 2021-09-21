const numLeds = 150
const numPlayers = 6

function getLeds() {
    var element = document.getElementById('mtgTableCenter').getBoundingClientRect();
    console.info("top: " + element.top + " left: " + element.left);
    console.info("bottom: " + element.bottom + " right: " + element.right);
    console.info('width: ' + element.width);
    centerLeds(element);
    leftLeds();
    rightLeds();
    mtgLogo();
}

function centerLeds(mtgTable) {
    var parent = document.getElementById('mtgTable');
    const sideLeds = numLeds/3 - 1;
    for (i = 0; i < sideLeds; i++) {
        parent.appendChild(createLed(mtgTable.top, mtgTable.left + mtgTable.width / sideLeds * i));
        parent.appendChild(createLed(mtgTable.bottom, mtgTable.left + mtgTable.width / sideLeds * i));
    }

    parent.appendChild(createLed(mtgTable.top, mtgTable.right));
    parent.appendChild(createLed(mtgTable.bottom, mtgTable.right));
}

function leftLeds() {
    const curveLeds = numLeds / 6;
    var parent = document.getElementById('mtgTable');
    var leftCircle = document.getElementById('mtgTableLeft').getBoundingClientRect();
    console.info(leftCircle.left);
    var centerX = leftCircle.left + leftCircle.width / 2;
    var centerY = leftCircle.top + leftCircle.height / 2;
    console.info("X=" + centerX + " Y=" + centerY);
    for (i = 1; i < curveLeds; i++) {
        coords = findPointOnCircle(centerX, centerY, leftCircle.width / 2, Math.PI/curveLeds * i + Math.PI/2);
        parent.appendChild(createLed(coords.y, coords.x));
    }
}

function rightLeds() {
    const curveLeds = numLeds / 6;
    var parent = document.getElementById('mtgTable');
    var rightCircle = document.getElementById('mtgTableRight').getBoundingClientRect();
    var centerX = rightCircle.left + rightCircle.width/2;
    var centerY = rightCircle.top + rightCircle.height/2;
    for (i = 1; i < curveLeds; i++) {
        coords = findPointOnCircle(centerX, centerY, rightCircle.width / 2, Math.PI/curveLeds * i - Math.PI/2);
        parent.appendChild(createLed(coords.y, coords.x));
    }
}

function findPointOnCircle(centerX, centerY, radius, angleRadians) {
    var newX = radius * Math.cos(angleRadians) + centerX;
    var newY = radius * Math.sin(angleRadians) + centerY;

    return {'x': newX, 'y': newY};
}

function createLed(top, left, size) {
    const led = document.createElement('div');
    led.className = 'led';
    led.style.left = left;
    led.style.top = top;
    if (size) {
        led.style.width = size;
        led.style.height = size;
    }
    return led;
}

function mtgLogo() {
    var parent = document.getElementById('mtgTable');
    const img = document.createElement('img');
    img.src = 'mtgtableart.png';
    img.style.height = 50;
    img.style.width = 50;
    img.style.top = 55;
    img.style.left = 135;
    img.style.position = 'fixed';
    img.style.zIndex = 1;
    parent.appendChild(img);
}