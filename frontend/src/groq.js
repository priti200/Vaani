export async function askGroq(question, pdfText, languageCode) {
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
