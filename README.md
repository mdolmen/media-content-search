# Media Content Search

Search in the content of video. It uses machine learning to generate the
transcript in which you can then do a simple text search.

You can run the transcritpion on locally on your machine or remotely using
[Replicate](https://replicate.com/)'s hardware. It requires an API key.

## How to run

Install ffmpeg:

MacOS:
```
brew install ffmpeg
```

Fedora:
```
sudo dnf install -y ffmpeg
```

Setup a python environment for `pyo3`:
```
python3 -m venv venv
source venv/bin/activate
cd backend
pip install -r requirements
deactivate
cd ..
```

Run:
```
cd app

# It will install the binary. Only tested on macos.
cargo tauri build

# Alternatively for dev
cargo tauri dev
```

## TODO

- [ ] Add a config file (for API key)
- [ ] (ux) Improve feedback on progression
- [ ] (ux) Display user Replicate account info (estimate billing)
- [ ] (feature) Upload file on personal cloud storage to handle large files (for
remote exec)
- [ ] (feature) Interact with an LLM about the content
- [ ] (feature) List keywords, the idea is to get a general idea about the
content (names, places, etc.)
- [ ] Packaging (including python interpreter for `pyo3`)
