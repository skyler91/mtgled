<script>
    export let top;
    export let left;
    export let player_id, color, size;
</script>

<style>
    .led {
	height: 4px;
	width: 4px;
	position: absolute;
    transform: translate(-50%, -50%);
}
</style>

<div class="led" style="top:{top}px; left:{left}px; background-color:{color};"></div>