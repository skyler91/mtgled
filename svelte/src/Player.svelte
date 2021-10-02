<script>
    import { createEventDispatcher } from 'svelte';
    import ColorPicker from './ColorPicker.svelte';
    import { gameInProgress } from './stores.js';

    export let player;
    let colorPickerVisible = false;

    const dispatch = createEventDispatcher();
    let location;
    $: {
        switch(parseInt(player.number)) {
            case 1:
                location = {
                    x: '-5px',
                    y: '-25px'
                }
                break;
            case 2:
                location = {
                    x: '335px',
                    y: '-25px'
                }
                break;
            case 3:
                location = {
                    x: '675px',
                    y: '120px'
                }
                break;
            case 4:
                location = {
                    x: '335px',
                    y: '240px'
                }
                break;
            case 5:
                location = {
                    x: '-5px',
                    y: '240px'
                }
                break;
            case 6:
                location = {
                    x: '-345px',
                    y: '120px'
                }
                break;
        }
    }

    function addPlayer() {
        dispatch('addPlayer', {
            name: player.name,
            number: player.number,
            color: player.color,
            lightStart: player.lightStart,
            lightEnd: player.lightEnd
        });
    }

    function removePlayer() {
        dispatch('removePlayer', {
            number: player.number
        });
    }

    function toggleColorPickerVisibility() {
        colorPickerVisible = !colorPickerVisible;
    }

    $: inGameStatus = player.inGame ? "YES" : "NO";
    $: opacity = (!$gameInProgress && player.inGame) ? 100 : 0;
</script>

<div class="player" style="left:{location.x}; top: {location.y}; --player-opacity:{opacity}; --light-color:{player.color}">
    <div class="description">Name: {player.name}</div>
    <div>
        <div class="description">Light Color: {player.color}</div>
        <div class="lightColorPreview" on:click={toggleColorPickerVisibility}></div>
    </div>


    {#if colorPickerVisible}
        <ColorPicker bind:colorHex={player.color} />
    {/if}
    <div class="description">In Game? {inGameStatus}</div>
    {#if player.inGame}
        <div>
            <button class="addRemoveButtons" on:click={removePlayer}>Remove</button>
        </div>
    {:else}
        <div>
            <button clas="addRemoveButtons" on:click={addPlayer}>Add</button>
        </div>
    {/if}
</div>

<style>
    .player {
        height: 250px;
        width: 335px;
        background-color: darkblue;
        position: absolute;
        z-index: 1;
        border-color: black;
        border-radius: 1px;
        border-style: solid;
        opacity: var(--player-opacity);
    }

    .player:hover {
        border-color: darkgray;
        opacity: 100;
    }

    .description {
        size: 18pt;
        font-weight: bold;
        color: white;
        display: inline-block;
    }

    .addRemoveButtons {
        display: inline;
        margin: 5px;
    }

    .lightColorPreview {
        width: 40px;
        height: 20px;
        border-color: black;
        border-radius: 1px;
        border-style: solid;
        left: 50px;
        display: inline-block;
        vertical-align: middle;
        background-color: var(--light-color);
    }
</style>