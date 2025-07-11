
# 🧩 ChatOverlayLint

**ChatOverlayLint** is a desktop application that displays YouTube Live Chat as a transparent overlay on your screen.  
Unlike other chat tools, this version works **without requiring any YouTube API key** — made possible by `pytchat`, which uses YouTube's publicly available data.
---

## 🎯 Features

- ✅ Live chat overlay for any YouTube Live stream
- 🪟 Transparent, draggable overlay window
- 🎨 Auto-highlights messages by role:
  - Owner
  - Moderator
  - Sponsor (Member)
  - SuperChat
- 📝 Built-in viewer for all collected messages
- 🔌 No YouTube API key required

---

## 📦 Installation

### From source

Install dependencies with pip:

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install pytchat appdirs
```

Run the program:

```bash
python main.py
```

---

### From Releases

You can download pre-built Windows executables (`.exe`) directly from the [Releases](https://github.com/TineTheUnc/ChatOverlayLint/releases) page.  
No installation or Python required — just run the executable.

---

## 🚀 Usage

1. Run the app
2. Paste the **Live ID** from a YouTube livestream URL (`v=...`)
3. Click **Start** to begin capturing the chat.
4. A transparent overlay will appear on your screen, showing incoming messages.
5. Click **Read Chat** to view the full chat log from the session.