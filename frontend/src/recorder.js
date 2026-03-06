let mediaRecorder = null
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
