<script>
async function nextTurn() {
    const resp = await fetch('http://127.0.0.1:8756/api/nextturn');
}
</script>

<div>
    <button on:click={nextTurn}>Next Turn</button>
</div>