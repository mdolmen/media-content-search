// Prevents additional console window on Windows in release, DO NOT REMOVE!!
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use std::env;
use std::process::Command;

use whisper_rs::{FullParams, SamplingStrategy, WhisperContext, WhisperContextParameters};

use pyo3::prelude::*;

// Maximum amplitude for a 16-bit audio sample
const MAX_AMPLITUDE: f32 = 32768.0;

// Sample rate required by whisper
const SAMPLE_RATE: &str = "16000";

#[pyclass]
struct LoggingStdout;

#[pymethods]
impl LoggingStdout {
    fn write(&self, data: &str) {
        println!("[python] {:?}", data);
    }

    fn flush(&self) {
    }
}

#[tauri::command]
async fn mcs_get_transcript(link: String) -> Vec<(i64, String)> {
    let audio_file = py_dl_audio(&link)
        .expect("failed to get the path to the audio file");

    let transcript = transcribe(audio_file.as_str());

    transcript
}

fn py_dl_audio(link: &String) -> PyResult<String> {
    let code = include_str!("../../../backend/src/media.py");

    Python::with_gil(|py| {
        let sys = py.import("sys")?;
        let path = sys.getattr("path")?;

        // Python's output to stdout
        sys.setattr("stdout", LoggingStdout.into_py(py))?;

        // Append venv to path
        // The workdir from python is 'app/src-tauri', not 'app/src-tauri/src' as above to
        // include_str the code file
        path.call_method1("append", ("../../venv/lib/python3.12/site-packages",))?;

        let _yt_dlp = PyModule::import(py, "yt_dlp")?;
        let media = PyModule::from_code(py, code, "media.py", "media")?;

        let audio_file: String = media.getattr("ytdl_and_extract_audio")?.call1((link.as_str(),))?.extract()?;

        Ok(audio_file)
    })
}

///
/// Based on: https://github.com/openai/whisper:whisper/whisper/audio.py.
///
fn load_audio(file: &str) -> Vec<f32> {
    // This launches a subprocess to decode audio while down-mixing
    // and resampling as necessary.  Requires the ffmpeg CLI in PATH.
    let ffmpeg = Command::new("ffmpeg")
        .args(["-nostdin", "-threads", "0", "-i", file, "-f", "s16le",
            "-ac", "1", "-acodec", "pcm_s16le", "-ar", SAMPLE_RATE, "-"
        ])
        .output()
        .expect("failed to execute process ffmpeg");

    // Normalize the values to the range [-1.0, 1.0]
    let audio: Vec<f32> = ffmpeg.stdout
        .chunks_exact(2)
        .map(|chunk| i16::from_le_bytes([chunk[0], chunk[1]]) as f32 / MAX_AMPLITUDE)
        .collect();
    println!("{:?}", audio.len());

    audio.to_vec()
}

fn transcribe(audio_file: &str) -> Vec<(i64, String)> {
    // TODO: get path to model from config
    let path_to_model = "/Users/mat/Workspace/media-content-search/models/ggml-base.en.bin";

    // Load a context and model.
    let ctx = WhisperContext::new_with_params(
        path_to_model,
        WhisperContextParameters::default(),
    )
    .expect("failed to load model");
    // Create a state
    let mut state = ctx.create_state().expect("failed to create key");

    // Create a params object for running the model.
    // The number of past samples to consider defaults to 0.
    let mut params = FullParams::new(SamplingStrategy::Greedy { best_of: 0 });

    // Edit params as needed.
    // Set the number of threads to use to 1.
    params.set_n_threads(1);
    // Enable translation.
    params.set_translate(false);
    // Disable anything that prints to stdout.
    params.set_print_special(false);
    params.set_print_progress(false);
    params.set_print_realtime(false);
    params.set_print_timestamps(false);

    println!("[+] loading audio...");
    let audio = load_audio(audio_file);

    // Run the model.
    println!("[+] running model...");
    state.full(params, &audio[..]).expect("failed to run model");
    println!("[+] done");

    let mut transcript = Vec::new();

    // Iterate through the segments of the transcript.
    let num_segments = state
        .full_n_segments()
        .expect("failed to get number of segments");
    for i in 0..num_segments {
        // Get the transcribed text and timestamps for the current segment.
        let segment = state
            .full_get_segment_text(i)
            .expect("failed to get segment");
        // Format is seconds.ms without separators. E.g. 5.35 sec -> 535
        let start = state
            .full_get_segment_t0(i)
            .expect("failed to get start timestamp");

        // Print the segment to stdout.
        //println!("[{} - {}]: {}", start_timestamp, end_timestamp, segment);

        // Format the segment information as a string.
        //let line = format!("[{} - {}]: {}\n", start_timestamp, end_timestamp, segment);
        transcript.push((start, segment));

        // Write the segment information to the file.
        //file.write_all(line.as_bytes())
        //    .expect("failed to write to file");
    }

    transcript
}

fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![mcs_get_transcript])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
