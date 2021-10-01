<script>
    export let players = [];

    async function startGame() {
        const resp = await fetch('http://127.0.0.1:8756/api/startgame', {
            method: 'POST',
            body: JSON.stringify(players.sort())
        });
    }
</script>

<div>
    <button on:click={startGame}>Start Game</button>
</div>