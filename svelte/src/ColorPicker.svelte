<script>
    import iro from '@jaames/iro';
    import { onMount } from 'svelte';

    export let colorHex = '#f00';
    let colorPickerElem;
    let colorPicker;


    onMount(() => {
        colorPicker = new iro.ColorPicker(colorPickerElem, {
            width: 100,
            color: colorHex
        })

        colorPicker.on('color:change', function(newColor) {
            colorHex = newColor.hexString
            console.log(`color: ${JSON.stringify(colorHex)}`);
        });
    });


</script>

<div bind:this={colorPickerElem} class='colorPicker'></div>

<style>
    .colorPicker {
        margin: auto;
        width: 100px;
        padding: 5px;
    }
</style>