<script>
    import { connectionStatus } from './stores.js';

    // let text = $status.text;
    // let color = $status.color;

    // $: {
    //     text = $status.text;
    //     color = $status.color;
    // };

</script>

<div class='container'>
    <div class='statusLight' style='background-color:{$connectionStatus.color}'></div>
    <div class='text'>{$connectionStatus.text}</div>
</div>

<style>
    .container {
        text-align: left
    }

    .statusLight {
        height: 8px;
        width: 8px;
        border-radius: 50%;
        background-color: 'red';
        display: inline-block;
    }

    .text {
        display: inline-block;
    }
</style>