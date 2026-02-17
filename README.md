# ZeroTraceGPT Image Creator

A web interface for AI image generation (Gradio).

![](screenshot.png)

## How to run (Windows)

1. **Unzip** the file.
2. **Install [Python 3.10.6](https://www.python.org/downloads/release/python-3106/)** — check **"Add Python to PATH"**. (Newer Python versions do not support torch.)
3. **Run `webui-user.bat`** from Windows Explorer as a normal (non-administrator) user.

The script will create the environment and launch the Web UI.

---

## Run without a GPU (Google Colab)

1. Open [colab_notebook.ipynb](colab_notebook.ipynb) in Colab (**File → Upload notebook**).
2. **Runtime → Change runtime type** → set **Hardware accelerator** to **T4 GPU** → Save.
3. **Runtime → Run all**. Use the public Gradio link printed in the last cell to open the Web UI.

---

## Credits

Licenses: see **Settings → Licenses** in the app, or `html/licenses.html`. Based on [AUTOMATIC1111/stable-diffusion-webui](https://github.com/AUTOMATIC1111/stable-diffusion-webui).
