const maxLeds = 148;
const maxPlayers = 6;
let currentPlayers = [1,2,3,4,5,6];
const leds = [];
let currPlayer = 0;

function getLeds() {
    var element = document.getElementById('mtgTableCenter').getBoundingClientRect();
    topLeds(element);
    rightLeds(document.getElementById('mtgTableRight').getBoundingClientRect());
    bottomLeds(element);
    leftLeds(document.getElementById('mtgTableLeft').getBoundingClientRect());
    mtgLogo(element);
}

function newGame(players) {
    resetLeds();
    currentPlayers = players;
}

function topLeds(parentRect) {
    const sideLeds = maxLeds / 3;
    for (i = 0; i < sideLeds; i++) {
        createLed(parentRect.top, parentRect.left + parentRect.width / sideLeds * i, i <= sideLeds / 2 ? 1 : 2);
    }
}

function bottomLeds(parentRect) {
    const sideLeds = maxLeds / 3;
    for (i = sideLeds; i >= 0; i--) {
        createLed(parentRect.bottom, parentRect.left + parentRect.width / sideLeds * i, i <= sideLeds / 2 ? 5: 4);
    }
}

function leftLeds(parentRect) {
    const curveLeds = maxLeds / 6;
    var centerX = parentRect.left + parentRect.width / 2;
    var centerY = parentRect.top + parentRect.height / 2;
    for (i = 1; i < curveLeds; i++) {
        const coords = findPointOnCircle(centerX, centerY, parentRect.width / 2, Math.PI/curveLeds * i + Math.PI/2);
        createLed(coords.y, coords.x, 6);
    }
}

function rightLeds(parentRect) {
    const curveLeds = maxLeds / 6;
    var centerX = parentRect.left + parentRect.width/2;
    var centerY = parentRect.top + parentRect.height/2;
    for (i = 1; i < curveLeds; i++) {
        const coords = findPointOnCircle(centerX, centerY, parentRect.width / 2, Math.PI/curveLeds * i - Math.PI/2);
        createLed(coords.y, coords.x, 3);
    }
}

function findPointOnCircle(centerX, centerY, radius, angleRadians) {
    var newX = radius * Math.cos(angleRadians) + centerX;
    var newY = radius * Math.sin(angleRadians) + centerY;

    return {'x': newX, 'y': newY};
}

function createLed(top, left, player_id, size=4) {
    const mtgTable = document.getElementById('mtgTable');
    let led = document.createElement('div');
    led.className = 'led';
    led.style.left = left;
    led.style.top = top;
    if (size) {
        led.style.width = size;
        led.style.height = size;
    }

    led = mtgTable.appendChild(led);
    leds.push(new Led(led, player_id))
    return led;
}

function mtgLogo() {
    var parent = document.getElementById('mtgTable');
    var tableCenter = document.getElementById('mtgTableCenter').getBoundingClientRect();
    const img = document.createElement('img');
    img.src = 'mtgtableart.png';
    img.style.height = tableCenter.height * 0.8;
    img.style.width = tableCenter.height * 0.8;
    img.style.top = tableCenter.top + tableCenter.height * .1;
    img.style.left = tableCenter.left + tableCenter.width / 2 - (tableCenter.height * 0.8 / 2);
    img.style.position = 'fixed';
    img.style.zIndex = 1;
    parent.appendChild(img);
}

function nextTurn() {
    resetLeds();

    do {
        currPlayer = currPlayer == maxPlayers ? 1 : currPlayer + 1;
    } while (!currentPlayers.includes(currPlayer));

    console.info(`Player ${currPlayer}'s turn!`);
    leds.filter(l => l.playerId == currPlayer).forEach(l => {
        console.info('Setting to green');
        l.element.style.backgroundColor = 'green'
    });
    
}

async function playAnimation(playerId) {
    playerLeds = leds.filter(l => l.playerId == playerId).forEach(l => {
        const color = randomColor();
        console.info(`Setting color to ${color}`);
        l.element.style.backgroundColor = 'yellow';
        pause(50);
    });
}

function pause(millis) {
    var date = Date.now();
    var curDate = null;
    do {
        curDate = Date.now();
    } while (curDate - date < millis);
}

function randomColor() {
    return `#${Math.floor(Math.random() * 16777215).toString(16)}`
}

// reset all LEDs to red
function resetLeds() {
    leds.forEach(l => l.element.style.backgroundColor = "red");
}

class Led {
    constructor(element, playerId) {
        this.element = element;
        this.playerId = playerId;
    }
}