export const audioStore = {}
let msgCount = 0

export function addMessage(role, text, audioChunks) {
  document.getElementById("emptyState").style.display = "none"
  const id = "msg" + (++msgCount)
  if (audioChunks && audioChunks.length > 0) { audioStore[id] = audioChunks }
  const playBtn = (role === "ai" && audioChunks && audioChunks.length > 0)
    ? "<button class=\"play-btn\" onclick=\"window.replayAudio('" + id + "')\">Play again</button>"
    : ""
  const el = document.createElement("div")
  el.className = "message"
  const avatarClass = role === "ai" ? "ai" : "user"
  const avatarText = role === "ai" ? "V" : "U"
  const bubbleClass = role === "ai" ? "ai" : "user"
  el.innerHTML = "<div class=\"msg-row " + role + "\">"
    + "<div class=\"avatar " + avatarClass + "\">" + avatarText + "</div>"
    + "<div class=\"bubble " + bubbleClass + "\">" + escapeHtml(text) + playBtn + "</div>"
    + "</div>"
  document.getElementById("messages").appendChild(el)
  scrollToBottom()
  return id
}

export function addTyping() {
  const el = document.createElement("div")
  el.className = "message"
  el.innerHTML = "<div class=\"msg-row ai\"><div class=\"avatar ai\">V</div><div class=\"bubble ai\"><div class=\"typing\"><span></span><span></span><span></span></div></div></div>"
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
  return text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/\n/g, "<br>")
}
