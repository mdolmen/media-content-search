// Prevents additional console window on Windows in release, DO NOT REMOVE!!
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use pyo3::prelude::*;
use pyo3::types::IntoPyDict;

#[tauri::command]
fn py_get_version() -> String {
    let version = test_calling_python().unwrap();

    version
}

fn test_calling_python() -> PyResult<String> {
    Python::with_gil(|py| {
        let sys = py.import_bound("sys")?;
        let version: String = sys.getattr("version")?.extract()?;

        let locals = [("os", py.import_bound("os")?)].into_py_dict_bound(py);
        let code = "os.getenv('USER') or os.getenv('USERNAME') or 'Unknown'";
        let user: String = py.eval_bound(code, None, Some(&locals))?.extract()?;

        Ok(format!("Hello {}, I'm Python {}", user, version))
    })
}

fn main() {
  tauri::Builder::default()
    .invoke_handler(tauri::generate_handler![py_get_version])
    .run(tauri::generate_context!())
    .expect("error while running tauri application");
}
