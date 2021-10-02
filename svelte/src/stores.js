import { writable } from 'svelte/store';
import { playersDefault } from './players.js';

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
export const allPlayers = writable(JSON.parse(JSON.stringify(playersDefault)));
export const gameInProgress = writable(false);