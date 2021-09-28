<script>
    async function startGame() {
        const resp = await fetch('http://127.0.0.1:8756/api/startgame', {
            method: 'POST',
            body: JSON.stringify([1,2,4,5])
        });
    }
</script>

<div>
    <button on:click={startGame}>Start Game</button>
</div>