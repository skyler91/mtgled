<script>
import { onMount } from 'svelte';

let mtgTable, mtgTableLeft, mtgTableRight;

const maxLeds = 148;
const maxPlayers = 6;
let currentPlayers = [1,2,3,4,5,6];
const leds = [];
let currPlayer = 0;

function getLeds() {
    console.info(`element: ${mtgTable}`);
    topLeds(mtgTable.getBoundingClientRect());
    rightLeds(mtgTableRight.getBoundingClientRect());
    bottomLeds(mtgTable.getBoundingClientRect());
    leftLeds(mtgTableLeft.getBoundingClientRect());
    //mtgLogo(mtgTable.getBoundingClientRect());
}

onMount(() => {
    getLeds()
});

function newGame(players) {
    resetLeds();
    currentPlayers = players;
}

function topLeds(parentRect) {
    const sideLeds = maxLeds / 3;
    for (let i = 0; i < sideLeds; i++) {
        createLed(parentRect.top, parentRect.left + parentRect.width / sideLeds * i, i <= sideLeds / 2 ? 1 : 2);
    }
}

function bottomLeds(parentRect) {
    const sideLeds = maxLeds / 3;
    for (let i = sideLeds; i >= 0; i--) {
        createLed(parentRect.bottom, parentRect.left + parentRect.width / sideLeds * i, i <= sideLeds / 2 ? 5: 4);
    }
}

function leftLeds(parentRect) {
    const curveLeds = maxLeds / 6;
    var centerX = parentRect.left + parentRect.width / 2;
    var centerY = parentRect.top + parentRect.height / 2;
    for (let i = 1; i < curveLeds; i++) {
        const coords = findPointOnCircle(centerX, centerY, parentRect.width / 2, Math.PI/curveLeds * i + Math.PI/2);
        createLed(coords.y, coords.x, 6);
    }
}

function rightLeds(parentRect) {
    const curveLeds = maxLeds / 6;
    var centerX = parentRect.left + parentRect.width/2;
    var centerY = parentRect.top + parentRect.height/2;
    for (let i = 1; i < curveLeds; i++) {
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
    img.src = 'img/mtgtableart.png';
    img.style.height = tableCenter.height * 0.8;
    img.style.width = tableCenter.height * 0.8;
    //img.style.top = tableCenter.top + tableCenter.height * .1;
    //img.style.left = tableCenter.left + tableCenter.width / 2 - (tableCenter.height * 0.8 / 2);
    img.style.position = 'absolute';
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
</script>

<main>
    <div bind:this={mtgTable} id="mtgTable">
        <div class="tableOuterCenter">
            <div class="outerLeftCircle">
                <div class="leftCircle" bind:this={mtgTableLeft} id="mtgTableLeft"></div>
            </div>
            <div class="outerRightCircle">
                <div class="rightCircle" bind:this={mtgTableRight} id="mtgTableRight"></div>
            </div>
            <div class="tableCenter" id="mtgTableCenter">
                <div class="mtgLogo"><img src="img/mtgtableart.png" alt="art"/></div>
            </div>
        </div>
    </div>

    <br /><br />
    <button type="button" onClick="nextTurn();">Ring!</button>
</main>

<style>
.tableOuterCenter {
    height: 480px;
    width: 640px;
    background-color: black;
    position: relative;
    left: 600px;
}

.tableCenter {
	height: 360px;
	width: 640px;
	background-color: #CBC3E3;
	position: absolute;
	top: 60px;
}

.outerLeftCircle {
    height: 480px;
    width: 480px;
    background-color: black;
    border-radius: 50%;
    position: absolute;
    left: -240px;
}

.leftCircle {
	height: 360px;
	width: 360px;
	background-color: #CBC3E3;
	border-radius: 50%;
	position: absolute;
	top: 60px;
	left: 60px;
}

.outerRightCircle {
    height: 480px;
    width: 480px;
    background-color: black;
    border-radius: 50%;
    position: absolute;
    left: 400px;
}

.rightCircle {
	height: 360px;
	width: 360px;
	background-color: #CBC3E3;
	border-radius: 50%;
	position: absolute;
	top: 60px;
	left: 60px;
}

.mtgLogo {
    height: 288px;
    width: 288px;
    position: absolute;
    top: 36px;
    left: 176px;
}

.led {
	height: 4px;
	width: 4px;
	background-color: red;
	position: fixed;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
}
</style>