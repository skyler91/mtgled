<script>
	import MtgTable from "./MtgTable.svelte";
	import ConnectionStatus from './ConnectionStatus.svelte';
</script>

<main>
	<ConnectionStatus />
	<MtgTable />
</main>

<style>
	main {
		text-align: center;
		padding: 1em;
		max-width: 240px;
		margin: 0 auto;
	}

	@media (min-width: 640px) {
		main {
			max-width: none;
		}
	}
</style>