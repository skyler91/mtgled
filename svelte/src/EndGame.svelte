<script>
    async function endGame() {
        console.info(`Ending game`);
        const resp = await fetch('http://127.0.0.1:8756/api/resetgame');
        const resp_json = await resp.json()
        if (resp_json.error) {
            console.error(`Got error when starting new game: ${resp_json.error}`);
        }
    }
</script>

<div>
    <button on:click={endGame}>End Game</button>
</div>