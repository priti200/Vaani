import os

os.makedirs("frontend/src", exist_ok=True)

# ── index.html ───────────────────────────────────────────────
with open("frontend/index.html", "w", encoding="utf-8") as f:
    f.write("""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Vaani</title>
  <link rel="icon" href="data:,">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      background: #212121;
      color: #ececec;
      height: 100vh;
      display: flex;
      flex-direction: column;
    }
    .topbar {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 14px 24px;
      border-bottom: 1px solid #2a2a2a;
      flex-shrink: 0;
    }
    .logo {
      font-size: 18px;
      font-weight: 600;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .logo-dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: #10a37f;
    }
    .lang-row { display: flex; gap: 4px; }
    .lang-btn {
      padding: 5px 12px;
      border-radius: 6px;
      border: 1px solid #333;
      background: transparent;
      color: #888;
      font-size: 12px;
      font-weight: 600;
      cursor: pointer;
      font-family: inherit;
      transition: all 0.15s;
    }
    .lang-btn.active { background: #10a37f; border-color: #10a37f; color: white; }
    .messages {
      flex: 1;
      overflow-y: auto;
      padding: 24px 0;
    }
    .messages::-webkit-scrollbar { width: 4px; }
    .messages::-webkit-scrollbar-thumb { background: #333; border-radius: 4px; }
    .empty {
      height: 100%;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      gap: 10px;
      color: #555;
    }
    .empty h2 { font-size: 20px; color: #ececec; font-weight: 600; }
    .empty p { font-size: 13px; text-align: center; line-height: 1.6; }
    .message { max-width: 700px; margin: 0 auto; padding: 4px 24px; }
    .msg-row { display: flex; gap: 10px; align-items: flex-start; }
    .msg-row.user { flex-direction: row-reverse; }
    .avatar {
      width: 28px; height: 28px;
      border-radius: 50%;
      display: flex; align-items: center; justify-content: center;
      font-size: 12px; font-weight: 700;
      flex-shrink: 0; margin-top: 2px;
    }
    .avatar.ai { background: #10a37f; color: white; }
    .avatar.user { background: #444; color: white; }
    .bubble { max-width: calc(100% - 44px); font-size: 14px; line-height: 1.6; color: #ececec; }
    .bubble.user { background: #2f2f2f; padding: 9px 14px; border-radius: 14px; }
    .bubble.ai { padding: 4px 0; }
    .play-btn {
      display: inline-flex; align-items: center; gap: 5px;
      background: #2a2a2a; border: 1px solid #333;
      border-radius: 6px; color: #888;
      padding: 4px 10px; font-size: 11px;
      cursor: pointer; font-family: inherit;
      margin-top: 8px; transition: all 0.15s;
    }
    .play-btn:hover { border-color: #555; color: #ececec; }
    .typing { display: flex; gap: 4px; align-items: center; padding: 6px 0; }
    .typing span {
      width: 6px; height: 6px;
      background: #555; border-radius: 50%;
      animation: bounce 1.1s infinite;
    }
    .typing span:nth-child(2) { animation-delay: 0.18s; }
    .typing span:nth-child(3) { animation-delay: 0.36s; }
    @keyframes bounce {
      0%, 60%, 100% { transform: translateY(0); }
      30% { transform: translateY(-5px); }
    }
    .bottom {
      flex-shrink: 0;
      padding: 12px 24px 20px;
      border-top: 1px solid #2a2a2a;
    }
    .input-wrap {
      max-width: 700px;
      margin: 0 auto;
      display: flex;
      flex-direction: column;
      gap: 10px;
    }
    .pdf-btn {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 7px 14px;
      border-radius: 8px;
      border: 1px dashed #3a3a3a;
      background: transparent;
      color: #666;
      font-size: 12px;
      cursor: pointer;
      font-family: inherit;
      transition: all 0.15s;
      width: fit-content;
    }
    .pdf-btn:hover { border-color: #555; color: #ececec; }
    .pdf-btn.loaded { border-style: solid; border-color: #10a37f; color: #10a37f; }
    .input-box {
      display: flex;
      align-items: flex-end;
      gap: 10px;
      background: #2f2f2f;
      border: 1px solid #3a3a3a;
      border-radius: 14px;
      padding: 10px 12px;
      transition: border-color 0.15s;
    }
    .input-box:focus-within { border-color: #555; }
    textarea {
      flex: 1;
      background: transparent;
      border: none;
      outline: none;
      color: #ececec;
      font-size: 14px;
      font-family: inherit;
      resize: none;
      max-height: 140px;
      line-height: 1.5;
      padding: 2px 0;
    }
    textarea::placeholder { color: #555; }
    .mic-btn {
      width: 36px; height: 36px;
      border-radius: 8px;
      border: none;
      background: #2a2a2a;
      color: #888;
      font-size: 16px;
      cursor: pointer;
      display: flex; align-items: center; justify-content: center;
      flex-shrink: 0;
      transition: all 0.2s;
    }
    .mic-btn:hover { background: #383838; color: #ececec; }
    .mic-btn.recording { background: #ef4444; color: white; animation: pulse 1.2s infinite; }
    .mic-btn:disabled { opacity: 0.35; cursor: not-allowed; }
    @keyframes pulse {
      0%, 100% { box-shadow: 0 0 0 0 rgba(239,68,68,0.4); }
      50% { box-shadow: 0 0 0 8px rgba(239,68,68,0); }
    }
    .send-btn {
      width: 36px; height: 36px;
      border-radius: 8px;
      border: none;
      background: #10a37f;
      color: white;
      font-size: 18px;
      cursor: pointer;
      display: flex; align-items: center; justify-content: center;
      flex-shrink: 0;
      transition: all 0.15s;
    }
    .send-btn:hover { background: #0d8f6e; }
    .send-btn:disabled { background: #2a2a2a; color: #444; cursor: not-allowed; }
    .status {
      display: flex;
      align-items: center;
      gap: 6px;
      font-size: 11px;
      color: #555;
    }
    .status-dot { width: 5px; height: 5px; border-radius: 50%; background: #333; flex-shrink: 0; }
    .status-dot.ready { background: #10a37f; }
    .status-dot.busy { background: #f59e0b; animation: blink 0.8s infinite; }
    .status-dot.error { background: #ef4444; }
    @keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0.2; } }
  </style>
</head>
<body>
  <div class="topbar">
    <div class="logo">
      <div class="logo-dot"></div>
      Vaani
    </div>
    <div class="lang-row">
      <button class="lang-btn active" data-lang="en-IN">EN</button>
      <button class="lang-btn" data-lang="hi-IN">HI</button>
      <button class="lang-btn" data-lang="bn-IN">BN</button>
    </div>
  </div>
  <div class="messages" id="messagesWrap">
    <div class="empty" id="emptyState">
      <h2>Vaani</h2>
      <p>Upload a research paper then type or speak your question.</p>
    </div>
    <div id="messages"></div>
  </div>
  <div class="bottom">
    <div class="input-wrap">
      <button class="pdf-btn" id="uploadBtn" onclick="document.getElementById('pdfInput').click()">
        <span>PDF</span>
        <span id="uploadLabel">Upload PDF</span>
      </button>
      <input type="file" id="pdfInput" accept=".pdf" style="display:none">
      <div class="input-box">
        <textarea id="textInput" placeholder="Type a question or use the mic..." rows="1"></textarea>
        <button class="mic-btn" id="micBtn">MIC</button>
        <button class="send-btn" id="sendBtn">&#8593;</button>
      </div>
      <div class="status">
        <div class="status-dot" id="statusDot"></div>
        <span id="statusText">Upload a PDF to begin</span>
      </div>
    </div>
  </div>
  <script type="module" src="src/main.js"></script>
</body>
</html>
""")

# ── recorder.js ──────────────────────────────────────────────
with open("frontend/src/recorder.js", "w", encoding="utf-8") as f:
    f.write("""let mediaRecorder = null
let audioChunks = []

export async function startRecording() {
  const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
  mediaRecorder = new MediaRecorder(stream, { mimeType: "audio/webm" })
  audioChunks = []
  mediaRecorder.ondataavailable = function(e) { audioChunks.push(e.data) }
  return new Promise(function(resolve) {
    mediaRecorder.onstop = async function() {
      stream.getTracks().forEach(function(t) { t.stop() })
      const webmBlob = new Blob(audioChunks, { type: "audio/webm" })
      const wavBlob = await convertToWav(webmBlob)
      resolve(wavBlob)
    }
    mediaRecorder.start()
  })
}

export function stopRecording() {
  if (mediaRecorder && mediaRecorder.state !== "inactive") {
    mediaRecorder.stop()
  }
}

async function convertToWav(webmBlob) {
  const arrayBuffer = await webmBlob.arrayBuffer()
  const audioContext = new OfflineAudioContext(1, 44100 * 10, 44100)
  const decoded = await audioContext.decodeAudioData(arrayBuffer)
  const samples = decoded.getChannelData(0)
  const sampleRate = decoded.sampleRate
  const numSamples = samples.length
  const buffer = new ArrayBuffer(44 + numSamples * 2)
  const view = new DataView(buffer)
  writeString(view, 0, "RIFF")
  view.setUint32(4, 36 + numSamples * 2, true)
  writeString(view, 8, "WAVE")
  writeString(view, 12, "fmt ")
  view.setUint32(16, 16, true)
  view.setUint16(20, 1, true)
  view.setUint16(22, 1, true)
  view.setUint32(24, sampleRate, true)
  view.setUint32(28, sampleRate * 2, true)
  view.setUint16(32, 2, true)
  view.setUint16(34, 16, true)
  writeString(view, 36, "data")
  view.setUint32(40, numSamples * 2, true)
  for (let i = 0; i < numSamples; i++) {
    const s = Math.max(-1, Math.min(1, samples[i]))
    view.setInt16(44 + i * 2, s < 0 ? s * 0x8000 : s * 0x7fff, true)
  }
  return new Blob([buffer], { type: "audio/wav" })
}

function writeString(view, offset, string) {
  for (let i = 0; i < string.length; i++) {
    view.setUint8(offset + i, string.charCodeAt(i))
  }
}
""")

# ── pdf.js ───────────────────────────────────────────────────
with open("frontend/src/pdf.js", "w", encoding="utf-8") as f:
    f.write("""export async function extractPDF(file) {
  if (!window.pdfjsLib) {
    await loadScript("https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js")
    window.pdfjsLib.GlobalWorkerOptions.workerSrc = "https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js"
  }
  const arrayBuffer = await file.arrayBuffer()
  const pdf = await pdfjsLib.getDocument({ data: arrayBuffer }).promise
  let fullText = ""
  for (let i = 1; i <= Math.min(pdf.numPages, 40); i++) {
    const page = await pdf.getPage(i)
    const content = await page.getTextContent()
    const pageText = content.items.map(function(item) { return item.str }).join(" ")
    fullText += pageText + "\\n"
  }
  return fullText.slice(0, 30000)
}

function loadScript(src) {
  return new Promise(function(resolve, reject) {
    const script = document.createElement("script")
    script.src = src
    script.onload = resolve
    script.onerror = reject
    document.head.appendChild(script)
  })
}
""")

# ── sarvam.js ────────────────────────────────────────────────
with open("frontend/src/sarvam.js", "w", encoding="utf-8") as f:
    f.write("""export async function speechToText(wavBlob, languageCode) {
  const formData = new FormData()
  formData.append("file", wavBlob, "audio.wav")
  formData.append("language_code", languageCode)
  const response = await fetch("/api/stt", { method: "POST", body: formData })
  if (!response.ok) { throw new Error("STT failed: " + response.status) }
  const data = await response.json()
  return data.transcript || ""
}

export async function textToSpeech(text, languageCode) {
  const response = await fetch("/api/tts", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text: text, language_code: languageCode })
  })
  if (!response.ok) { throw new Error("TTS failed: " + response.status) }
  const data = await response.json()
  return data.audio
}

export function playAudio(base64Audio) {
  return new Promise(function(resolve) {
    const audio = new Audio("data:audio/wav;base64," + base64Audio)
    audio.onended = resolve
    audio.onerror = resolve
    audio.play()
  })
}
""")

# ── groq.js ──────────────────────────────────────────────────
with open("frontend/src/groq.js", "w", encoding="utf-8") as f:
    f.write("""export async function askGroq(question, pdfText, languageCode) {
  const response = await fetch("/api/llm", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      question: question,
      pdfText: pdfText,
      language_code: languageCode
    })
  })
  if (!response.ok) { throw new Error("LLM failed: " + response.status) }
  const data = await response.json()
  return data.answer
}
""")

# ── ui.js ────────────────────────────────────────────────────
with open("frontend/src/ui.js", "w", encoding="utf-8") as f:
    f.write("""export const audioStore = {}
let msgCount = 0

export function addMessage(role, text, audioB64) {
  document.getElementById("emptyState").style.display = "none"
  const id = "msg" + (++msgCount)
  if (audioB64) { audioStore[id] = audioB64 }
  const playBtn = (role === "ai" && audioB64)
    ? "<button class=\\"play-btn\\" onclick=\\"window.replayAudio('" + id + "')\\">Play again</button>"
    : ""
  const el = document.createElement("div")
  el.className = "message"
  const avatarClass = role === "ai" ? "ai" : "user"
  const avatarText = role === "ai" ? "V" : "U"
  const bubbleClass = role === "ai" ? "ai" : "user"
  el.innerHTML = "<div class=\\"msg-row " + role + "\\">"
    + "<div class=\\"avatar " + avatarClass + "\\">" + avatarText + "</div>"
    + "<div class=\\"bubble " + bubbleClass + "\\">" + escapeHtml(text) + playBtn + "</div>"
    + "</div>"
  document.getElementById("messages").appendChild(el)
  scrollToBottom()
  return id
}

export function addTyping() {
  const el = document.createElement("div")
  el.className = "message"
  el.innerHTML = "<div class=\\"msg-row ai\\"><div class=\\"avatar ai\\">V</div><div class=\\"bubble ai\\"><div class=\\"typing\\"><span></span><span></span><span></span></div></div></div>"
  document.getElementById("messages").appendChild(el)
  scrollToBottom()
  return el
}

export function setStatus(type, message) {
  document.getElementById("statusDot").className = "status-dot " + type
  document.getElementById("statusText").textContent = message
}

export function setTranscript(text) {
  const textarea = document.getElementById("textInput")
  textarea.value = text
  autoResize(textarea)
}

export function clearTextarea() {
  const textarea = document.getElementById("textInput")
  textarea.value = ""
  textarea.style.height = "auto"
}

export function autoResize(textarea) {
  textarea.style.height = "auto"
  textarea.style.height = Math.min(textarea.scrollHeight, 140) + "px"
}

function scrollToBottom() {
  const wrap = document.getElementById("messagesWrap")
  wrap.scrollTop = wrap.scrollHeight
}

function escapeHtml(text) {
  return text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/\\n/g, "<br>")
}
""")

# ── main.js ──────────────────────────────────────────────────
with open("frontend/src/main.js", "w", encoding="utf-8") as f:
    f.write("""import { startRecording, stopRecording } from "./recorder.js"
import { speechToText, textToSpeech, playAudio } from "./sarvam.js"
import { askGroq } from "./groq.js"
import { extractPDF } from "./pdf.js"
import { addMessage, addTyping, setStatus, setTranscript, clearTextarea, autoResize, audioStore } from "./ui.js"

var pdfText = ""
var currentLang = "en-IN"
var isRecording = false
var isBusy = false

window.replayAudio = function(id) {
  if (audioStore[id]) { playAudio(audioStore[id]) }
}

document.getElementById("pdfInput").addEventListener("change", async function(e) {
  const file = e.target.files[0]
  if (!file) return
  setStatus("busy", "Reading PDF...")
  pdfText = await extractPDF(file)
  document.getElementById("uploadBtn").classList.add("loaded")
  document.getElementById("uploadLabel").textContent = "Done: " + file.name.slice(0, 24)
  setStatus("ready", "PDF ready, type or speak your question")
})

document.querySelectorAll(".lang-btn").forEach(function(btn) {
  btn.addEventListener("click", function() {
    document.querySelectorAll(".lang-btn").forEach(function(b) { b.classList.remove("active") })
    btn.classList.add("active")
    currentLang = btn.dataset.lang
  })
})

document.getElementById("textInput").addEventListener("input", function(e) {
  autoResize(e.target)
})

document.getElementById("sendBtn").addEventListener("click", function() {
  const text = document.getElementById("textInput").value.trim()
  if (!text || isBusy) return
  clearTextarea()
  runPipeline(text)
})

document.getElementById("textInput").addEventListener("keydown", function(e) {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault()
    const text = document.getElementById("textInput").value.trim()
    if (!text || isBusy) return
    clearTextarea()
    runPipeline(text)
  }
})

document.getElementById("micBtn").addEventListener("click", async function() {
  if (isBusy) return
  if (!pdfText) { setStatus("error", "Upload a PDF first"); return }
  if (!isRecording) {
    isRecording = true
    document.getElementById("micBtn").classList.add("recording")
    document.getElementById("micBtn").textContent = "STOP"
    setStatus("busy", "Listening... tap to stop")
    const wavBlob = await startRecording()
    await runVoicePipeline(wavBlob)
  } else {
    isRecording = false
    document.getElementById("micBtn").classList.remove("recording")
    document.getElementById("micBtn").textContent = "MIC"
    stopRecording()
  }
})

async function runVoicePipeline(wavBlob) {
  setBusy(true)
  setStatus("busy", "Transcribing your voice...")
  var question = ""
  try {
    question = await speechToText(wavBlob, currentLang)
  } catch(e) {
    setStatus("error", "Could not transcribe, try again")
    setBusy(false)
    return
  }
  if (!question) {
    setStatus("ready", "Nothing heard, try again")
    setBusy(false)
    return
  }
  setTranscript(question)
  await runPipeline(question)
}

async function runPipeline(question) {
  if (!pdfText) { setStatus("error", "Upload a PDF first"); return }
  setBusy(true)
  addMessage("user", question)
  clearTextarea()
  const typing = addTyping()
  setStatus("busy", "Thinking...")
  var answer = ""
  try {
    answer = await askGroq(question, pdfText, currentLang)
  } catch(e) {
    typing.remove()
    setStatus("error", "Could not get answer, try again")
    setBusy(false)
    return
  }
  setStatus("busy", "Generating voice...")
  var audioB64 = null
  try {
    audioB64 = await textToSpeech(answer, currentLang)
  } catch(e) {
    console.warn("TTS failed:", e.message)
  }
  typing.remove()
  addMessage("ai", answer, audioB64)
  if (audioB64) {
    setStatus("busy", "Speaking...")
    await playAudio(audioB64)
  }
  setStatus("ready", "Ask another question")
  setBusy(false)
}

function setBusy(busy) {
  isBusy = busy
  document.getElementById("micBtn").disabled = busy
  document.getElementById("sendBtn").disabled = busy
}
""")

print("All files written successfully!")