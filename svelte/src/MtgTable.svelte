<script>
import { onMount } from 'svelte';
import { element } from 'svelte/internal';
import LED from './LED.svelte';

let statusMsg = 'Connecting...';

function connectWebSocket() {
    const socket = new WebSocket("ws://127.0.0.1:8756");
    socket.addEventListener('open', function(event) {
        console.info('Connected to WebSocket')
        statusMsg = '';
    });

    socket.addEventListener('close', function(event) {
        statusMsg = 'Connecting...'
        setTimeout(function() {
            connectWebSocket();
        }, 1000);
    })

    socket.addEventListener('message', function(event) {
        const data = event.data;
        const json_data = JSON.parse(data)
        console.info(`data: ${JSON.stringify(json_data)}`)
        json_data.forEach((element, index) => {
            leds[index].color = `rgb(${element.r},${element.g},${element.b})`
        });
        leds = leds
    });
}

connectWebSocket();

let mtgTable, mtgTableCenter, mtgTableLeft, mtgTableRight;

const maxLeds = 148;
const maxPlayers = 6;
let currentPlayers = [1,2,3,4,5,6];
let leds = [];
let currPlayer = 0;

onMount(() => {
    addLeds();
});

function addLeds() {
    topLeds();
    rightLeds();
    bottomLeds();
    leftLeds();

    leds = leds;
}

function newGame(players) {
    resetLeds();
    currentPlayers = players;
}

function topLeds() {
    const sideLeds = maxLeds / 3;
    const tableRect = mtgTableCenter.getBoundingClientRect();
    for (let i = 0; i < sideLeds; i++) {
        createLed(0, tableRect.width / sideLeds * i, i <= sideLeds / 2 ? 1 : 2);
    }
}

function bottomLeds() {
    const sideLeds = maxLeds / 3;
    const tableRect = mtgTableCenter.getBoundingClientRect();
    for (let i = sideLeds; i >= 0; i--) {
        createLed(tableRect.height, tableRect.width / sideLeds * i, i <= sideLeds / 2 ? 5: 4);
    }
}

function leftLeds() {
    const curveLeds = maxLeds / 6;
    const leftRect = mtgTableLeft.getBoundingClientRect();
    var centerX = leftRect.width / 2;
    var centerY = leftRect.height / 2;
    for (let i = 1; i < curveLeds; i++) {
        const coords = findPointOnCircle(centerX, centerY, leftRect.width / 2, Math.PI/curveLeds * i + Math.PI/2);
        createLed(coords.y, coords.x, 6);
    }
}

function rightLeds() {
    const curveLeds = maxLeds / 6;
    const rightRect = mtgTableRight.getBoundingClientRect();
    var centerX = rightRect.width/2;
    var centerY = rightRect.height/2;
    for (let i = 1; i < curveLeds; i++) {
        const coords = findPointOnCircle(centerX, centerY, rightRect.width / 2, Math.PI/curveLeds * i - Math.PI/2);
        createLed(coords.y, coords.x, 3);
    }
}

function findPointOnCircle(centerX, centerY, radius, angleRadians) {
    var newX = radius * Math.cos(angleRadians) + centerX;
    var newY = radius * Math.sin(angleRadians) + centerY;

    return {'x': newX, 'y': newY};
}

function createLed(top, left, player_id, color="red", size=4) {
    const led = {
        coords: {
            x: left,
            y: top
        },
        player_id: player_id,
        color: color,
        size: size,
        visible: true
    };
    leds = [...leds, led];
}

function nextTurn() {
    resetLeds();

    do {
        currPlayer = currPlayer == maxPlayers ? 1 : currPlayer + 1;
    } while (!currentPlayers.includes(currPlayer));

    console.info(`Player ${currPlayer}'s turn!`);
    leds.forEach(l => {
        if (l.player_id === currPlayer)
        {
            l.color = 'red';
            l.visible = true;
        }
    });
    leds = leds;
}

function randomColor() {
    return `#${Math.floor(Math.random() * 16777215).toString(16)}`
}

// reset all LEDs to red
function resetLeds() {
    leds.forEach(l => l.visible = false);
}
</script>

<main>
    <h1>{statusMsg}</h1>
    <div bind:this={mtgTable} id="mtgTable">
        <div class="tableOuterCenter">
            <div class="outerLeftCircle">
                <div class="leftCircle" bind:this={mtgTableLeft} id="mtgTableLeft">
                    {#each leds.filter(l => l.player_id === 6) as led}
                        <LED coords={led.coords} color={led.color} visible={led.visible} />
                    {/each}
                </div>
            </div>
            <div class="outerRightCircle">
                <div class="rightCircle" bind:this={mtgTableRight} id="mtgTableRight">
                    {#each leds.filter(l => l.player_id === 3) as led}
                        <LED coords={led.coords} color={led.color} visible={led.visible} />
                    {/each}
                </div>
            </div>
            <div class="tableCenter" bind:this={mtgTableCenter} id="mtgTableCenter">
                <div class="mtgLogo"><img src="img/mtgtableart.png" alt="art"/></div>
                {#each leds.filter(l => [1,2,4,5].includes(l.player_id)) as led}
                <LED coords={led.coords} color={led.color} visible={led.visible} />
                {/each}
            </div>
        </div>
    </div>

    <br /><br />
    <button type="button" on:click="{nextTurn}">Next Turn</button>
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
</style>