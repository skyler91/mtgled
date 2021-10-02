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
        cursor: default;
        border-style: solid;
        border-width: 1px;
        border-color: black;
        float: left;
        padding: 5px;
    }

    .statusLight {
        height: 8px;
        width: 8px;
        border-radius: 50%;
        background-color: 'red';
        display: inline-block;
        vertical-align: center;
    }

    .text {
        display: inline-block;
    }
</style>