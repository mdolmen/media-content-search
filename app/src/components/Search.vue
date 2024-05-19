<script setup lang="ts">
import { ref, watch } from 'vue';
import axios from 'axios';

// Issue '..not a constructor' when importing this module as the others
//     https://github.com/nextapps-de/flexsearch/issues/341#issuecomment-1296011307
// Using the following from the project's README
//import Index from "../../node_modules/flexsearch/dist/module/index";
//import Document from "../../node_modules/flexsearch/dist/module/document";
import Document from "flexsearch/dist/module/document";

import { invoke } from '@tauri-apps/api';
import { QuestionMarkCircleIcon } from '@heroicons/vue/24/solid'

let transcript = ref();
let isYoutube = ref(false);
let videoUrl = ref("");
let videoEmbedUrl = ref("");
let index = new Document({
  id: "id",
  index: [{
    field: "content",
    tokenize: "full"
  }]
});
let inputSearch = ref("");
let status = ref("idle");
let debug = ref("nothing");
declare var YT: any; // because YouTube API loaded asynchronously
let player: any = null;
let ytAPIReady = false;
let remoteEnabled = ref(false);

function videoSeek(time: number) {
    player.seekTo(time, true);
    player.playVideo();
}

function getTranscriptForDev() {
    transcript.value = [
  ["0.0", " See, a statically typed procedural programming language famous for making the world go around."],
  ["5.52", " It's the language behind many tools we take for granted, like the Windows, Linux, and Mac operating"],
  ["10.48", " system kernels, databases like MySQL, interpreters for languages like Python, tools like VIM and Git,"],
  ["17.12", " and countless others. It was created in 1972 by Dennis Richie at Bell Labs, where it would be used to"],
  ["22.96", " develop the Unix operating system. It would go on to become the mother of all languages,"],
  ["27.04", " inspiring the syntax of C++, C sharp, Java, JavaScript, Terrel, and PHP just to name a few."],
  ["33.36", " It compiles directly to machine code and requires minimal runtime support, but is platform"],
  ["37.84", " dependent, meaning the executable is designed to run on a specific operating system. It's a high"],
  ["43.12", " level language designed for humans, yet provides low-level control over memory and hardware."],
  ["47.68", " There's no garbage collector. Instead, your code needs to manage its own memory. When you create a"],
  ["51.92", " variable, it's assigned an address and memory. You can store that address in another variable"],
  ["56.4", " called a pointer. When the variable is no longer needed, you'll need to free it to avoid memory"],
  ["60.8", " leaks. To get started, install AC compiler. A popular choice is the GNU-C compiler or GCC."],
  ["66.96", " Create a file, ending in .c, include any libraries you plan to use, then add a main function to it."],
  ["72.24", " This is where your program will start executing. There's no function keyword, and notice how it"],
  ["76.32", " returns an integer type. A return value of 0 means success, while a return value of 1 means"],
  ["81.52", " failure. There are only a few basic types in C, create a variable by starting with a type,"],
  ["86.16", " followed by a name and value. Use print to print the value to the standard output, or put an"],
  ["91.52", " ampersand in front of it to reference its address and memory. There's no string type, but instead"],
  ["96.24", " char, which represents a 1 by character stored as an integer. A string can be created within a"],
  ["101.44", " ray of characters. Each letter will have its own memory address and be terminated by a null"],
  ["105.84", " character. Another approach is to start with a pointer by adding a star character in front of the"],
  ["111.2", " type, then we can allocate 4 bytes to it. Now assign a character to each index, ending with a"],
  ["116.0", " null character to create a string. When you no longer need that memory allocated to your program,"],
  ["120.24", " use free to release it back to the computer's RAM. The language is procedural, and does not support"],
  ["125.6", " object-oriented features, although you can create your own complex data types using structs."],
  ["130.16", " Now compile your code to machine instructions for your operating system using the C compiler."],
  ["134.8", " This has been the C programming language in 100 seconds. Hit the like button and subscribe if"],
  ["139.36", " you want to see more short videos like this. Thanks for watching, and I will see you in the next one."]
    ];
}

function setupRealTimeSearch() {
    for (let i = 0; i < transcript.value.length; i++) {
        var line = transcript.value[i];
        index.add({
            id: i,
            time: line[0],
            content: line[1]
        });
    }

    console.log(index);
}

/*
 * Search the 'input' text into the index and return an array of entries
 * containing 'input'.
 */
function realTimeSearch() {
    let resultIndex = index.search(inputSearch.value);
    let result = [];

    if (resultIndex.length <= 0) {
        return result;
    }

    let ids = (resultIndex[0] as any)["result"];
    for (let i = 0; i < ids.length; i++) {
        let id = ids[i];
        // push([time, text])
        result.push([transcript.value[id][0], transcript.value[id][1]]);
    }

    return result;
}

/*
 * Source: https://stackoverflow.com/questions/3452546/how-do-i-get-the-youtube-video-id-from-a-url
 *
 * Supported formats:
 *    http://www.youtube.com/watch?v=0zM3nApSvMg&feature=feedrec_grec_index
 *    http://www.youtube.com/user/IngridMichaelsonVEVO#p/a/u/1/QdK8U-VIH_o
 *    http://www.youtube.com/v/0zM3nApSvMg?fs=1&amp;hl=en_US&amp;rel=0
 *    http://www.youtube.com/watch?v=0zM3nApSvMg#t=0m10s
 *    http://www.youtube.com/embed/0zM3nApSvMg?rel=0
 *    http://www.youtube.com/watch?v=0zM3nApSvMg
 *    http://youtu.be/0zM3nApSvMg
 */
function youtubeParser(url: string){
    var regExp = /^.*((youtu.be\/)|(v\/)|(\/u\/\w\/)|(embed\/)|(watch\?))\??v?=?([^#&?]*).*/;
    var match = url.match(regExp);
    return (match&&match[7].length==11)? match[7] : false;
}

async function updateTranscript() {
    const videoId = youtubeParser(videoUrl.value);
    videoEmbedUrl = ref("https://www.youtube.com/embed/"+videoId);
    transcript.value = {}
    status.value = "extracting transcript...";

    console.log("video id = ", videoId);
    console.log("getting transcript");

    // Load video
    if (player === null) {
        player = new YT.Player('player', {
            videoId: videoId,
            playerVars: {
                'playsinline': 1
            },
            events: {
                'onReady': onPlayerReady
            }
        });
    }
    else {
        player.loadVideoById(videoId);
    }

    // Extract transcript
    try {
        // invoke tauri command, async
        invoke('mcs_get_transcript', { link: videoEmbedUrl.value, remote: remoteEnabled.value }).then(
          message => {
            debug.value = message[0];
            transcript.value = message;
            status.value = "transcript loaded";
            console.log("done");
            setupRealTimeSearch();
          }
        );
    } catch (error) {
        console.log(error);
    }
}

//
// YouTube player
// Source: https://developers.google.com/youtube/iframe_api_reference#Loading_a_Video_Player
//

// 2. This code loads the IFrame Player API code asynchronously.
function loadYoutubeAPI() {
    console.log("loading youtube api");
    var tag = document.createElement('script');

    tag.src = "https://www.youtube.com/iframe_api";
    var firstScriptTag = document.getElementsByTagName('script')[0];
    if (firstScriptTag.parentNode) {
        firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
    } else {
        console.log("loadYoutubeAPI: failed to load API");
    }

    // To make the callback accessible to the API
    (window as any).onYouTubeIframeAPIReady = onYouTubeIframeAPIReady;
}

// 3. This function creates an <iframe> (and YouTube player)
//    after the API code downloads.
function onYouTubeIframeAPIReady() {
    console.log("onYouTubeIframeAPIReady");
    ytAPIReady = true;
}

// 4. The API will call this function when the video player is ready.
function onPlayerReady(event: any) {
    console.log("onPlayerReady");
    event.target.playVideo();
}

// Convert milliseconds to time format (00:00:00).
function secondsToTime(seconds) {
    let secs = Math.floor(seconds % 60);
    let minutes = Math.floor(seconds / 60);
    let hours = Math.floor(minutes / 60);

    hours = (hours < 10) ? "0" + hours : hours;
    minutes = (minutes < 10) ? "0" + minutes : minutes;
    secs = (secs < 10) ? "0" + secs : secs;

    return hours + ":" + minutes + ":" + secs;
}

loadYoutubeAPI()
</script>

<template>
    <div class="flex flex-row mb-4">
        <div class="basis-5/6 mr-4">
            <label class="input input-bordered flex items-center gap-2">
                <input type="text" class="grow" placeholder="Video URL" v-model="videoUrl" @keyup.enter="isYoutube = true; updateTranscript()">
                <svg class="w-6 h-6 text-gray-800 dark:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 16 18" @click="isYoutube = true; updateTranscript()">
                    <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 1v11m0 0 4-4m-4 4L4 8m11 4v3a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2v-3"/>
                </svg>
            </label>
        </div>
        <div class="w-full basis-1/6 flex flex-row items-center">
            <input type="checkbox" id="enableRemote" class="toggle mr-2" v-model="remoteEnabled" />
            <p>Remote</p>
            <div class="tooltip ml-1" data-tip="Enable to execute the transcription using Replicate. Config required in conf.yaml.">
                <QuestionMarkCircleIcon class="size-4 text-blue-500"/>
            </div>
        </div>
    </div>


    <div class="columns-2 gap-4 flex flex-row">
        <div class="w-full flex flex-col">
            <!-- Hack to align the player with the table... -->
            <div class="">
                <a role="tab" class="tab"></a>
            </div>

            <div id="player-wrapper" class="w-full aspect-video mt-2">
                <!-- 1. The <iframe> (and video player) will replace this <div> tag. -->
                <div id="player"></div>
            </div>
        </div>

        <div id="result" class="w-full">
            <div role="tablist" class="tabs tabs-bordered">
                <a role="tab" class="tab tab-active">Search</a>
                <a role="tab" class="tab">ChatGPT</a>
                <a role="tab" class="tab">Keywords</a>
            </div>

            <div id="transcript-table" class="overflow-auto mt-2 mb-2">
                <table class="table-zebra overflow-auto">
                    <tbody>
                        <tr v-for="line in inputSearch ? realTimeSearch() : transcript" :key="line[0]"
                            class="overflow-auto"
                            @click="videoSeek(line[0])"
                        >
                            <th>[{{ secondsToTime(line[0]) }}]</th>
                            <th class="transcript-line ml-2">{{ line[1] }}</th>
                        </tr>
                    </tbody>
                </table>
            </div>

            <div class="">
              <input type="text" class="input input-bordered w-full" placeholder="Search" v-model="inputSearch">
            </div>
        </div>
    </div>

    <div id="status-bar" class="flex flex-row mt-10 mb-5">
        <label>Status: {{ status }}</label>
        <label for="enableRemote" class="ml-3">Remote: {{ remoteEnabled }}</label>
        <label class="bg-gray-300 ml-3" @click="isYoutube = false; getTranscriptForDev()">Load transcript for dev</label>
        <!--
        <p>Debug: {{ debug }}</p>
        -->
    </div>

</template>

<style>
#player {
    border-radius: var(--rounded-btn, 0.5rem);
}

.transcript {
    border-style: solid;
    border-width: 1px;
    min-height: 63vh;
    overflow: scroll;
}

.transcript-line {
    white-space: nowrap !important;
    text-align: left;
}

#transcript-table {
    min-height: 50vh;
    max-height: 60vh;
    border-style: solid;
    border-width: 1px;
    border-radius: var(--rounded-btn, 0.5rem);
}

#result {
    max-width: 50%;
}

#status-bar {
    position: fixed;
    bottom: 0;
}

#replicate-api {
    border-style: solid;
    border-width: 1px;
    border-radius: var(--rounded-btn, 0.5rem);
}

.search-bar {
    margin: auto;
    margin-top: 8px;
}

iframe {
    height: 50vh !important;
    width: 100% !important;
}
</style>
