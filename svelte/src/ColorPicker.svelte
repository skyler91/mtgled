<script>
    import iro from '@jaames/iro';
    import { onMount } from 'svelte';

    export let colorHex = '#f00';
    let colorPickerElem;
    let colorPicker;


    onMount(() => {
        colorPicker = new iro.ColorPicker(colorPickerElem, {
            width: 100,
            color: colorHex,
            layout: [
                {
                    component: iro.ui.Wheel,
                    options: {
                        margin: 3
                    }
                },
                {
                    component: iro.ui.Slider,
                    options: {
                        margin: 3
                    }
                }
            ]
        })

        colorPicker.on('color:change', function(newColor) {
            colorHex = newColor.hexString
        });
    });


</script>

<div bind:this={colorPickerElem} class='colorPicker'></div>

<style>
    .colorPicker {
        margin: auto;
        width: 100px;
    }
</style>