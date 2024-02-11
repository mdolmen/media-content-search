<script setup lang="ts">
import { ref } from 'vue';
import axios from 'axios';

// Issue '..not a constructor' when importing this module as the others
//     https://github.com/nextapps-de/flexsearch/issues/341#issuecomment-1296011307
// Using the following from the project's README
import Index from "../../node_modules/flexsearch/dist/module/index";
import Document from "../../node_modules/flexsearch/dist/module/document";

const backend_url = 'http://localhost:8000'

async function getTranscript() {
    try {
        const response = await axios.get(backend_url+'/transcript');
        const data = response.data;
        console.log('Transcript:\n', data);

        // Update the div with the fetched data
        const resultDiv = document.getElementById('result');
        if (resultDiv) {
            resultDiv.innerHTML = `Data from FastAPI: ${JSON.stringify(data)}`;
        }
    } catch (error) {
        console.log(error);
    }
}

function videoSeek(time: number) {
    const player = document.getElementById('player');
    player.currentTime = time;
    player.play();
}

function getTranscriptForDev() {
    return {
  "0.0": " See, a statically typed procedural programming language famous for making the world go around.",
  "5.52": " It's the language behind many tools we take for granted, like the Windows, Linux, and Mac operating",
  "10.48": " system kernels, databases like MySQL, interpreters for languages like Python, tools like VIM and Git,",
  "17.12": " and countless others. It was created in 1972 by Dennis Richie at Bell Labs, where it would be used to",
  "22.96": " develop the Unix operating system. It would go on to become the mother of all languages,",
  "27.04": " inspiring the syntax of C++, C sharp, Java, JavaScript, Terrel, and PHP just to name a few.",
  "33.36": " It compiles directly to machine code and requires minimal runtime support, but is platform",
  "37.84": " dependent, meaning the executable is designed to run on a specific operating system. It's a high",
  "43.12": " level language designed for humans, yet provides low-level control over memory and hardware.",
  "47.68": " There's no garbage collector. Instead, your code needs to manage its own memory. When you create a",
  "51.92": " variable, it's assigned an address and memory. You can store that address in another variable",
  "56.4": " called a pointer. When the variable is no longer needed, you'll need to free it to avoid memory",
  "60.8": " leaks. To get started, install AC compiler. A popular choice is the GNU-C compiler or GCC.",
  "66.96": " Create a file, ending in .c, include any libraries you plan to use, then add a main function to it.",
  "72.24": " This is where your program will start executing. There's no function keyword, and notice how it",
  "76.32": " returns an integer type. A return value of 0 means success, while a return value of 1 means",
  "81.52": " failure. There are only a few basic types in C, create a variable by starting with a type,",
  "86.16": " followed by a name and value. Use print to print the value to the standard output, or put an",
  "91.52": " ampersand in front of it to reference its address and memory. There's no string type, but instead",
  "96.24": " char, which represents a 1 by character stored as an integer. A string can be created within a",
  "101.44": " ray of characters. Each letter will have its own memory address and be terminated by a null",
  "105.84": " character. Another approach is to start with a pointer by adding a star character in front of the",
  "111.2": " type, then we can allocate 4 bytes to it. Now assign a character to each index, ending with a",
  "116.0": " null character to create a string. When you no longer need that memory allocated to your program,",
  "120.24": " use free to release it back to the computer's RAM. The language is procedural, and does not support",
  "125.6": " object-oriented features, although you can create your own complex data types using structs.",
  "130.16": " Now compile your code to machine instructions for your operating system using the C compiler.",
  "134.8": " This has been the C programming language in 100 seconds. Hit the like button and subscribe if",
  "139.36": " you want to see more short videos like this. Thanks for watching, and I will see you in the next one."
    };
}

const transcript = getTranscriptForDev();
const index = setupRealTimeSearch();
const inputSearch = ref("");

function setupRealTimeSearch() {
    var index = new Document({
        id: "time",
        index: [{
            field: "content",
            tokenize: "full"
        }]
    });
    // TODO: transcript from parameter instead?
    for (let key in transcript) {
        index.add({
            time: key,
            content: transcript[key]
        });
    }

    return index;
}

function realTimeSearch() {
    let resultIndex = index.search(inputSearch.value);
    let result = {};

    if (resultIndex.length <= 0) {
        return result;
    }

    let times = resultIndex[0]["result"];
    for (let i in times) {
        result[times[i]] = transcript[times[i]];
    }

    return result;
}

setupRealTimeSearch();
</script>

<template>
    <h1>Video Content Search</h1>

    <div class="d-grid gap-3">
        <div class="row justify-content-md-center">
            <input type="text" id="video-url" name="video-url" placeholder="Video URL" class="col">
            <button class="col col-1">Load</button>
        </div>
        <div class="row">
            <button class="col">Upload</button>
        </div>

        <div class="row">
            <div class="col col-6">
                <video id="player" controls style="width: 100%">
                    <source src="../assets/c-in-100-seconds.webm" type="video/webm" />
                </video>
            </div>

            <div id="result" class="col col-6">
                <div class="transcript">
                <ul class="list-group">
                    <li v-for="(line, timestamp) in inputSearch ? realTimeSearch() : transcript" :key="timestamp"
                        class="list-group-item list-group-item-action transcript-line"
                        @click="videoSeek(timestamp)"
                    >
                        {{ timestamp }} : {{ line }}
                    </li>
                </ul>
                </div>

                <div class="row search-bar">
                    <input type="text" placeholder="Search" class="col" v-model="inputSearch">
                </div>
            </div>
        </div>
    </div>
</template>

<style>
.transcript {
    border-style: solid;
    min-height: 70vh;
    max-height: 70vh;
    overflow: scroll;
}

.transcript-line {
    white-space: nowrap;
    overflow: scroll;
}

.search-bar {
    margin: auto;
    margin-top: 1rem;
}
</style>
