export async function speechToText(wavBlob, languageCode) {
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
  return data.audios || []
}

export async function playAudio(audiosArray) {
  if (!Array.isArray(audiosArray)) {
    audiosArray = [audiosArray]
  }
  for (const base64Audio of audiosArray) {
    if (!base64Audio) continue;
    await new Promise(function(resolve) {
      const audio = new Audio("data:audio/wav;base64," + base64Audio)
      audio.onended = resolve
      audio.onerror = resolve
      audio.play().catch(resolve)
    })
  }
}
