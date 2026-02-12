import { useMemo, useState } from 'react'

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'
const API_TOKEN = import.meta.env.VITE_API_TOKEN || ''

function getSessionId() {
  const existing = localStorage.getItem('calcifer_session_id')
  if (existing) return existing
  const created = crypto.randomUUID()
  localStorage.setItem('calcifer_session_id', created)
  return created
}

export default function App() {
  const sessionId = useMemo(() => getSessionId(), [])
  const [text, setText] = useState('')
  const [messages, setMessages] = useState([])
  const [approval, setApproval] = useState(null)

  async function callApi(path, body) {
    const res = await fetch(`${API_BASE}${path}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${API_TOKEN}`,
      },
      body: JSON.stringify(body),
    })
    if (!res.ok) throw new Error(await res.text())
    return res.json()
  }

  async function send() {
    if (!text.trim()) return
    const userText = text
    setText('')
    setMessages((prev) => [...prev, { role: 'user', text: userText }])

    try {
      const data = await callApi('/chat', { session_id: sessionId, text: userText })
      if (data.status === 'needs_approval') {
        setApproval(data)
        setMessages((prev) => [...prev, { role: 'assistant', text: 'Approval required before execution.' }])
      } else {
        setMessages((prev) => [...prev, { role: 'assistant', text: data.reply }])
      }
    } catch (err) {
      setMessages((prev) => [...prev, { role: 'assistant', text: `Error: ${err.message}` }])
    }
  }

  async function handleApprove(approve) {
    if (!approval) return
    const approvalId = approval.approval_id
    setApproval(null)
    try {
      const data = await callApi('/approve', { approval_id: approvalId, approve })
      setMessages((prev) => [...prev, { role: 'assistant', text: data.reply }])
    } catch (err) {
      setMessages((prev) => [...prev, { role: 'assistant', text: `Approval error: ${err.message}` }])
    }
  }

  return (
    <main className="app">
      <h1>Calcifer Chat</h1>
      <p className="session">session: {sessionId}</p>
      <section className="chat">
        {messages.map((m, idx) => (
          <div key={`${m.role}-${idx}`} className={`msg ${m.role}`}>
            <strong>{m.role}:</strong> {m.text}
          </div>
        ))}
      </section>

      {approval && (
        <section className="approval">
          <p>Approval required for: {approval.request.tool_name}</p>
          <button onClick={() => handleApprove(true)}>Approve</button>
          <button onClick={() => handleApprove(false)}>Deny</button>
        </section>
      )}

      <section className="composer">
        <input value={text} onChange={(e) => setText(e.target.value)} placeholder="Type your message" />
        <button onClick={send}>Send</button>
      </section>
    </main>
  )
}
