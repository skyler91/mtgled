<script>
import { onMount } from 'svelte';
import LED from './LED.svelte';
import NextTurn from './NextTurn.svelte';
import StartGame from './StartGame.svelte';
import Player from './Player.svelte';
import EndGame from './EndGame.svelte';
import ResetGame from './ResetGame.svelte';
import { statusEnum, connectionStatus, allPlayers, gameInProgress } from './stores.js';

let mtgTable, mtgTableCenter, mtgTableLeft, mtgTableRight;
const maxLeds = 148;
let leds = [];
$: gameStatus = $connectionStatus == statusEnum.CONNECTED
    ? $gameInProgress
        ? "Game in Progress"
        : "Start a new game"
    : "";

onMount(() => {
    addLeds();
    connectWebSocket();
});

function connectWebSocket() {
    const socketAddr = PYLIGHTS_ADDRESS || '127.0.0.1:8756';
    const socket = new WebSocket(`ws://${socketAddr}/lightsocket`);
    socket.addEventListener('open', function(event) {
        console.info('Connected to WebSocket');
        $connectionStatus = statusEnum.CONNECTED;
    });

    socket.addEventListener('close', function(event) {
        $connectionStatus = statusEnum.DISCONNECTED;

        hideAllLeds();
        setTimeout(function() {
            connectWebSocket();
        }, 1000);
    })

    socket.addEventListener('message', function(event) {
        const data = event.data;
        const json_data = JSON.parse(data)
        console.info(JSON.stringify(event))
        $gameInProgress = json_data.status
        json_data.lights.forEach((element, index) => {
            leds[index].color = element;
            leds[index].visible = true;
        });
        if (json_data.players) {
            console.info(`Updating players from backend: ${JSON.stringify(json_data.players)}`);
            json_data.players.forEach((p) => {
                const matchIdx = $allPlayers.findIndex(m => m.number == p.number);
                if(matchIdx >= 0 && !$allPlayers[matchIdx].inGame) {
                    $allPlayers[matchIdx] = p;
                    $allPlayers[matchIdx].inGame = true;
                    $allPlayers = $allPlayers;
                }
            });
        }
        leds = leds
    });
}

function handleAddPlayer(event) {
    const playerObj = event.detail;
    if (!playerObj.name || !playerObj.number || !playerObj.color
        || playerObj.lightStart == undefined || playerObj.lightEnd == undefined) {
        console.error(`Failed to add player (missing info): ${JSON.stringify(playerObj)}`);
        return;
    }

    const matching = $allPlayers.find(p => p.number == playerObj.number);
    if (matching == null) {
        console.error(`Could not find player ${JSON.stringify(playerObj)}`);
        return;
    }

    if (matching.inGame) {
        console.warn(`Player ${playerObj.number} is already in the game`);
        return;
    }

    matching.inGame = true;
    $allPlayers = $allPlayers;
}

function handleRemovePlayer(event) {
    const matchingPlayer = $allPlayers.find(p => p.number == event.detail.number);
    if (matchingPlayer == null) {
        console.error(`Cannot find player to remove: ${JSON.stringify(event.detail)}`);
        return;
    }
    console.info(`removing ${JSON.stringify(matchingPlayer)}`);
    matchingPlayer.inGame = false;
    $allPlayers = $allPlayers;
}

function addLeds() {
    topLeds();
    rightLeds();
    bottomLeds();
    leftLeds();

    leds = leds;
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
        visible: false
    };
    leds = [...leds, led];
}

function hideAllLeds() {
    leds.forEach(led => led.visible = false)
    leds = leds;
}
</script>

<main>
    <h1 class="gameStatus">{gameStatus}</h1>
    <div>Players: {JSON.stringify($allPlayers.filter(p => p.inGame))}</div>
    <div bind:this={mtgTable} id="mtgTable">
        <div class="tableOuterCenter">
        {#each $allPlayers as p}
            {#if ($gameInProgress && p.inGame) || !$gameInProgress}
                <Player on:addPlayer={handleAddPlayer} on:removePlayer={handleRemovePlayer} player={p} />
            {/if}
        {/each}
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
    {#if $gameInProgress}
        <NextTurn />
        <EndGame />
    {:else}
        <StartGame players={$allPlayers.filter(p => p.inGame)} />
        <ResetGame />
    {/if}
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

.gameStatus {
    height: 50px;
    width: 100%;
    text-align: center;
    visibility: visible;
}
</style>