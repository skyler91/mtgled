<script>
    export let color = red;
    export let coords;
    export let visible;
</script>

<style>
    .led {
	height: 4px;
	width: 4px;
	position: absolute;
    transform: translate(-50%, -50%);
}
</style>

{#if visible}
<div class="led" style="top:{coords.y}px; left:{coords.x}px; background-color:{color};"></div>
{/if}