import { writable } from 'svelte/store';

export const statusEnum = {
    CONNECTED: {
        text: "Connected",
        color: 'green'
    },
    DISCONNECTED: {
        text: "Disconnected",
        color: 'red'
    }
}

export const connectionStatus = writable(statusEnum.DISCONNECTED);