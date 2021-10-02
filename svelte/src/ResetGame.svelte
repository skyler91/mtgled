<script>
    import { allPlayers } from './stores.js';
    import { playersDefault } from './players.js';

    function resetGame() {
        $allPlayers = JSON.parse(JSON.stringify(playersDefault));
    }
</script>

<div>
    <button on:click={resetGame}>Reset Game</button>
</div>