import React, { useState, useEffect, useRef } from 'react'
import { Plus, Wifi, WifiOff, RefreshCcw, Share2, Check } from 'lucide-react'

const API_BASE = 'http://localhost:8000/api/v1/game'
const WS_BASE = 'ws://localhost:8000/api/v1/ws'

type Player = 'X' | 'O' | null
type GameStatus = 'KEEP_PLAYING' | 'X_WINS' | 'O_WINS' | 'DRAW'

interface GameState {
  board: { root: Player[] }[]
  turn: 'X' | 'O'
  status: GameStatus
}

function App() {
  const [gameId, setGameId] = useState<string | null>(null)
  const [gameState, setGameState] = useState<GameState | null>(null)
  const [player, setPlayer] = useState<'X' | 'O'>('X')
  const [error, setError] = useState<string | null>(null)
  const [connected, setConnected] = useState(false)
  const [isCopied, setIsCopied] = useState(false)
  const [isJoined, setIsJoined] = useState(false)
  const socketRef = useRef<WebSocket | null>(null)

  const createGame = async () => {
    try {
      const resp = await fetch(`${API_BASE}/new_game`, { method: 'POST' })
      const data = await resp.json()
      setGameId(data.game_id)
      window.location.hash = data.game_id
      setIsJoined(true)
      setError(null)
    } catch (err) {
      setError('Could not connect to server')
    }
  }

  useEffect(() => {
    const hash = window.location.hash.replace('#', '')
    if (hash && hash.length > 10) {
      setGameId(hash)
      // We don't auto-join anymore, user must click 'Join Game'
    }

    const handleHashChange = () => {
      const newHash = window.location.hash.replace('#', '')
      if (newHash && newHash.length > 10) {
        setGameId(newHash)
      } else if (!newHash) {
        setGameId(null)
        setIsJoined(false)
      }
    }

    window.addEventListener('hashchange', handleHashChange)
    return () => window.removeEventListener('hashchange', handleHashChange)
  }, [])

  useEffect(() => {
    if (!gameId || !isJoined) return

    const socket = new WebSocket(`${WS_BASE}/${gameId}/${player}`)
    socketRef.current = socket

    socket.onopen = () => setConnected(true)
    socket.onclose = () => setConnected(false)
    socket.onerror = () => setError('WebSocket error')

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data)
      if (data.error) {
        setError(data.error)
      } else {
        setGameState(data)
        setError(null)
      }
    }

    return () => {
      socket.close()
    }
  }, [gameId, isJoined, player])

  const makeMove = (row: number, col: number) => {
    if (socketRef.current?.readyState === WebSocket.OPEN) {
      socketRef.current.send(JSON.stringify({ row, col }))
    }
  }

  const reset = () => {
    setGameId(null)
    setGameState(null)
    setIsJoined(false)
    setError(null)
    window.location.hash = ''
  }

  const copyInviteLink = () => {
    const url = window.location.href
    navigator.clipboard.writeText(url)
    setIsCopied(true)
    setTimeout(() => setIsCopied(false), 2000)
  }

  if (!isJoined) {
    return (
      <div className="animate-in">
        <h1>Tic-Tac-Toe</h1>
        <p className="subtitle">{gameId ? `Joining Game ${gameId.slice(0, 4)}` : 'Real-time LAN Gaming'}</p>

        <div className="card">
          <div style={{ marginBottom: '1.5rem' }}>
            <label style={{ fontSize: '0.875rem', color: 'var(--text-secondary)', display: 'block', marginBottom: '0.5rem' }}>
              Choose your side
            </label>
            <div style={{ display: 'flex', gap: '0.5rem' }}>
              <button
                className={`btn ${player === 'X' ? 'btn-primary' : 'btn-outline'}`}
                onClick={() => setPlayer('X')}
              >
                Play as X
              </button>
              <button
                className={`btn ${player === 'O' ? 'btn-primary' : 'btn-outline'}`}
                onClick={() => setPlayer('O')}
              >
                Play as O
              </button>
            </div>
          </div>

          {gameId ? (
            <button className="btn btn-primary" onClick={() => setIsJoined(true)}>
              Join Game
            </button>
          ) : (
            <button className="btn btn-primary" onClick={createGame}>
              <Plus size={18} style={{ marginRight: '0.5rem' }} />
              New Game
            </button>
          )}

          {error && <p style={{ color: 'var(--error)', fontSize: '0.875rem', marginTop: '1rem', textAlign: 'center' }}>{error}</p>}
        </div>
      </div >
    )
  }

  return (
    <div className="animate-in">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
        <div>
          <h1>Game: {gameId.slice(0, 4)}</h1>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.75rem', color: 'var(--text-secondary)' }}>
            {connected ? <Wifi size={12} color="var(--success)" /> : <WifiOff size={12} color="var(--error)" />}
            {connected ? 'Connected' : 'Disconnected'}
            <span style={{ margin: '0 0.25rem' }}>•</span>
            Playing as {player}
          </div>
        </div>
        <div style={{ display: 'flex', gap: '0.5rem' }}>
          <button
            className="btn btn-outline"
            style={{ width: 'auto', padding: '0.5rem' }}
            onClick={copyInviteLink}
            title="Copy Invite Link"
          >
            {isCopied ? <Check size={18} color="var(--success)" /> : <Share2 size={18} />}
          </button>
          <button className="btn btn-outline" style={{ width: 'auto', padding: '0.5rem' }} onClick={reset}>
            <RefreshCcw size={18} />
          </button>
        </div>
      </div>

      <div className="game-board">
        {gameState?.board.map((row, rIdx) =>
          row.root.map((cell, cIdx) => (
            <button
              key={`${rIdx}-${cIdx}`}
              className={`cell ${cell?.toLowerCase() || ''}`}
              disabled={!!cell || gameState.status !== 'KEEP_PLAYING' || gameState.turn !== player}
              onClick={() => makeMove(rIdx, cIdx)}
            >
              {cell}
            </button>
          ))
        )}
      </div>

      <div className="status-bar">
        <div>
          <span style={{ color: 'var(--text-secondary)', fontSize: '0.875rem' }}>
            {gameState?.status === 'KEEP_PLAYING'
              ? (gameState.turn === player ? "Your turn" : "Waiting for opponent...")
              : "Game Over"
            }
          </span>
        </div>
        <div className="badge badge-blue">
          {gameState?.status === 'KEEP_PLAYING'
            ? `Turn: ${gameState.turn}`
            : gameState?.status.replace('_', ' ')
          }
        </div>
      </div>

      {error && (
        <div style={{ marginTop: '1rem', padding: '0.75rem', borderRadius: '0.5rem', backgroundColor: 'rgba(239, 68, 68, 0.1)', color: 'var(--error)', fontSize: '0.875rem' }}>
          {error}
        </div>
      )}
    </div>
  )
}

export default App
