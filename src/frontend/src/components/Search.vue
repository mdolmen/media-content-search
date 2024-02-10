<script setup lang="ts">
import axios from 'axios';

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

function getTranscriptForDev() {
    return {
  "00:00:00": " See, a statically typed procedural programming language famous for making the world go around.",
  "00:00:05": " It's the language behind many tools we take for granted, like the Windows, Linux, and Mac operating",
  "00:00:10": " system kernels, databases like MySQL, interpreters for languages like Python, tools like VIM and Git,",
  "00:00:17": " and countless others. It was created in 1972 by Dennis Richie at Bell Labs, where it would be used to",
  "00:00:22": " develop the Unix operating system. It would go on to become the mother of all languages,",
  "00:00:27": " inspiring the syntax of C++, C sharp, Java, JavaScript, Terrel, and PHP just to name a few.",
  "00:00:33": " It compiles directly to machine code and requires minimal runtime support, but is platform",
  "00:00:37": " dependent, meaning the executable is designed to run on a specific operating system. It's a high",
  "00:00:43": " level language designed for humans, yet provides low-level control over memory and hardware.",
  "00:00:47": " There's no garbage collector. Instead, your code needs to manage its own memory. When you create a",
  "00:00:51": " variable, it's assigned an address and memory. You can store that address in another variable",
  "00:00:56": " called a pointer. When the variable is no longer needed, you'll need to free it to avoid memory",
  "00:01:00": " leaks. To get started, install AC compiler. A popular choice is the GNU-C compiler or GCC.",
  "00:01:06": " Create a file, ending in .c, include any libraries you plan to use, then add a main function to it.",
  "00:01:12": " This is where your program will start executing. There's no function keyword, and notice how it",
  "00:01:16": " returns an integer type. A return value of 0 means success, while a return value of 1 means",
  "00:01:21": " failure. There are only a few basic types in C, create a variable by starting with a type,",
  "00:01:26": " followed by a name and value. Use print to print the value to the standard output, or put an",
  "00:01:31": " ampersand in front of it to reference its address and memory. There's no string type, but instead",
  "00:01:36": " char, which represents a 1 by character stored as an integer. A string can be created within a",
  "00:01:41": " ray of characters. Each letter will have its own memory address and be terminated by a null",
  "00:01:45": " character. Another approach is to start with a pointer by adding a star character in front of the",
  "00:01:51": " type, then we can allocate 4 bytes to it. Now assign a character to each index, ending with a",
  "00:01:56": " null character to create a string. When you no longer need that memory allocated to your program,",
  "00:02:00": " use free to release it back to the computer's RAM. The language is procedural, and does not support",
  "00:02:05": " object-oriented features, although you can create your own complex data types using structs.",
  "00:02:10": " Now compile your code to machine instructions for your operating system using the C compiler.",
  "00:02:14": " This has been the C programming language in 100 seconds. Hit the like button and subscribe if",
  "00:02:19": " you want to see more short videos like this. Thanks for watching, and I will see you in the next one."
    };
}

const transcript = getTranscriptForDev();
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
                <video controls style="width: 100%">
                    <source src="../assets/c-in-100-seconds.webm" type="video/webm" />
                </video>
            </div>

            <div id="result" class="col col-6">
                <ul class="list-group">
                    <li v-for="(line, timestamp) in transcript" :key="timestamp" class="list-group-item list-group-item-action">
                        {{ timestamp }} : {{ line }}
                    </li>
                </ul>
            </div>
        </div>
    </div>
</template>
