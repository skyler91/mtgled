<script>
    import { createEventDispatcher } from 'svelte';
    import { fade } from 'svelte/transition';
    import ColorPicker from './ColorPicker.svelte';
    import { gameInProgress } from './stores.js';

    export let player;
    let colorPickerVisible = false;
    let editName = false;
    let visible = false;

    const dispatch = createEventDispatcher();
    let location;
    let tmpPlayer;

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
        colorPickerVisible = false;
        editName = false;
        dispatch('removePlayer', {
            number: player.number
        });
    }

    function toggleColorPickerVisibility() {
        if (!$gameInProgress) {
            colorPickerVisible = !colorPickerVisible;
        }
    }

    function onEditName() {
        if (!$gameInProgress) {
            editName = true;
        }
    }

    function updatePlayer() {
        tmpPlayer = { ...player }
    }

    function commitPlayer() {
        player.name = tmpPlayer.name;
        editName = false;
    }

    function mouseEnter() {
        if (!visible && (!$gameInProgress || ($gameInProgress && player.inGame))) {
            visible = true;
        }
    }

    function mouseLeave() {
        if (visible && ($gameInProgress || (!$gameInProgress && !player.inGame))) {
            visible = false;
        }
    }

    $: player, updatePlayer();
    $: inGameStatus = player.inGame ? "YES" : "NO";
    $: visible = (!$gameInProgress && player.inGame) ? true : false;
    $: playerBorderColor = player.inGame ? 'green' : 'black';
    $: colorPickerVisible = colorPickerVisible && !$gameInProgress;
    $: editName = editName && !$gameInProgress;
</script>

<div class="container" on:mouseenter={mouseEnter} on:mouseleave={mouseLeave} style="left: {location.x}; top: {location.y};">
    {#if visible}
        <div class="player" style="--light-color:{player.color}; --player-border-color: {playerBorderColor};" transition:fade>
            {#if editName && !$gameInProgress}
                <div class="description">Name: </div>
                <input type="text" class="nameInput" bind:value={tmpPlayer.name}>
                <button type="submit" class="updateButton" on:click={commitPlayer}>Update</button>
            {:else}
                <div class="description" on:click={onEditName}>Name: {player.name}</div>
            {/if}

            <div>
                <div class="description">Light Color: {player.color}</div>
                <div class="lightColorPreview" on:click={toggleColorPickerVisibility}></div>
            </div>

            {#if colorPickerVisible && !$gameInProgress}
                <ColorPicker bind:colorHex={player.color} />
            {/if}

            <div class="description">In Game? {inGameStatus}</div>

            {#if !$gameInProgress}
                {#if player.inGame}
                    <div>
                        <button class="addRemoveButtons" on:click={removePlayer}>Remove</button>
                    </div>
                {:else}
                    <div>
                        <button class="addRemoveButtons" disabled={editName} on:click={addPlayer}>Add</button>
                    </div>
                {/if}
            {/if}
        </div>
    {/if}
</div>

<style>
    .container {
        height: 250px;
        width: 335px;
        position: absolute;
        z-index: 2;
    }

    .player {
        height: 250px;
        width: 335px;
        background-color: darkblue;
        z-index: 1;
        border-color: var(--player-border-color);
        border-radius: 1px;
        border-style: solid;
        opacity: 0.9;
    }

    .player:hover {
        border-color: yellow;
    }

    .description {
        size: 18pt;
        font-weight: bold;
        color: white;
        display: inline-block;
    }

    .nameInput {
        height: 25px;
        width: 100px;
        margin: 5px;
    }

    .updateButton {
        height: 25px;
        margin-top: -3px;
        margin-bottom: 2px;
        margin-left: 3px;
        margin-right: 3px;
        padding-top: 0px;
        padding-bottom: 0px;
        padding-left: 2px;
        padding-right: 2px;
        vertical-align: middle;
        text-align: center;
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