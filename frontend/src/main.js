import { startRecording, stopRecording } from "./recorder.js"
// import { speechToText, textToSpeech, playAudio } from "./sarvam.js"
import { speechToText, textToSpeech, playAudio } from "./elevenlabs.js"
import { askGroq } from "./groq.js"
import { extractPDF } from "./pdf.js"
import { addMessage, addTyping, setStatus, setTranscript, clearTextarea, autoResize, audioStore } from "./ui.js"

var pdfText = ""
var currentLang = "en-IN"
var isRecording = false
var isBusy = false

window.replayAudio = function (id) {
  if (audioStore[id]) { playAudio(audioStore[id]) }
}

document.getElementById("pdfInput").addEventListener("change", async function (e) {
  const file = e.target.files[0]
  if (!file) return
  setStatus("busy", "Reading PDF...")
  pdfText = await extractPDF(file)
  document.getElementById("uploadBtn").classList.add("loaded")
  document.getElementById("uploadLabel").textContent = "Done: " + file.name.slice(0, 24)
  setStatus("ready", "PDF ready, type or speak your question")
})

document.querySelectorAll(".lang-btn").forEach(function (btn) {
  btn.addEventListener("click", function () {
    document.querySelectorAll(".lang-btn").forEach(function (b) { b.classList.remove("active") })
    btn.classList.add("active")
    currentLang = btn.dataset.lang
  })
})

document.getElementById("textInput").addEventListener("input", function (e) {
  autoResize(e.target)
})

document.getElementById("sendBtn").addEventListener("click", function () {
  const text = document.getElementById("textInput").value.trim()
  if (!text || isBusy) return
  clearTextarea()
  runPipeline(text)
})

document.getElementById("textInput").addEventListener("keydown", function (e) {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault()
    const text = document.getElementById("textInput").value.trim()
    if (!text || isBusy) return
    clearTextarea()
    runPipeline(text)
  }
})

document.getElementById("micBtn").addEventListener("click", async function () {
  if (isBusy) return
  if (!pdfText) { setStatus("error", "Upload a PDF first"); return }
  if (!isRecording) {
    isRecording = true
    document.getElementById("micBtn").classList.add("recording")
    setStatus("busy", "Listening... tap to stop")
    const wavBlob = await startRecording()
    await runVoicePipeline(wavBlob)
  } else {
    isRecording = false
    document.getElementById("micBtn").classList.remove("recording")
    stopRecording()
  }
})

async function runVoicePipeline(wavBlob) {
  setBusy(true)
  setStatus("busy", "Transcribing your voice...")
  var question = ""
  try {
    question = await speechToText(wavBlob, currentLang)
  } catch (e) {
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
  } catch (e) {
    typing.remove()
    setStatus("error", "Could not get answer, try again")
    setBusy(false)
    return
  }
  setStatus("busy", "Generating voice...")
  var audioChunks = null
  try {
    audioChunks = await textToSpeech(answer, currentLang)
  } catch (e) {
    console.warn("TTS failed:", e.message)
  }
  typing.remove()
  addMessage("ai", answer, audioChunks)
  if (audioChunks && audioChunks.length > 0) {
    setStatus("busy", "Speaking...")
    await playAudio(audioChunks)
  }
  setStatus("ready", "Ask another question")
  setBusy(false)
}

function setBusy(busy) {
  isBusy = busy
  document.getElementById("micBtn").disabled = busy
  document.getElementById("sendBtn").disabled = busy
}
