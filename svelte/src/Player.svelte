<script>
    import { createEventDispatcher } from 'svelte';
    import ColorPicker from './ColorPicker.svelte';

    export let player;

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

</script>

<div class="player" style="left:{location.x}; top: {location.y}; background-color: {player.color};">
    <div class="description">Name: {player.name}</div>
    <div class="description">Light Color: {player.color}</div>
    <ColorPicker bind:colorHex={player.color} />
    <button on:click={addPlayer}>Add</button>
</div>

<style>
    .player {
        height: 250px;
        width: 335px;
        background-color: yellow;
        position: absolute;
        z-index: 1;
        border-color: transparent;
        border-radius: 1px;
        border-style: solid;
        opacity: 0;
    }

    .player:hover {
        border-color: black;
        opacity: 100;
    }

    .description {
        size: 18pt;
        font-weight: bold;
        color: white;
    }
</style>