<script>
    export let players = [];

    async function startGame() {
        console.info(`Starting a new game with players: ${JSON.stringify(players)}`);
        const resp = await fetch('http://127.0.0.1:8756/api/startgame', {
            method: 'POST',
            body: JSON.stringify(players.sort())
        });
        const resp_json = await resp.json()
        if (resp_json.error) {
            console.error(`Got error when starting new game: ${resp_json.error}`);
        }
    }
</script>

<div>
    <button on:click={startGame}>Start Game</button>
</div>