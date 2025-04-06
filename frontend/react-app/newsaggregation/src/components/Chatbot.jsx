"use client"

import { useState, useEffect, useRef } from "react"
import { useLocation, useParams } from "react-router-dom"
import { FaRobot, FaTimes, FaChevronDown, FaPaperPlane, FaSpinner } from "react-icons/fa"
import "./Chatbot.css"
import axios from "axios"

const Chatbot = () => {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState("")
  const [isOpen, setIsOpen] = useState(false)
  const [isMinimized, setIsMinimized] = useState(true)
  const [isTyping, setIsTyping] = useState(false)
  const messagesEndRef = useRef(null)
  const inputRef = useRef(null)
  const location = useLocation()
  const { id: articleId } = useParams()

  // Scroll to bottom of messages
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  // Initialize chatbot with welcome message
  useEffect(() => {
    if (messages.length === 0) {
      setMessages([
        {
          sender: "bot",
          text: "Hello! I'm your news assistant. How can I help you today?",
          timestamp: new Date().toISOString(),
        },
      ])
    }
  }, [messages])

  // Focus input when chat is opened
  useEffect(() => {
    if (isOpen && !isMinimized) {
      inputRef.current?.focus()
    }
  }, [isOpen, isMinimized])

  const toggleMinimize = () => {
    setIsMinimized(!isMinimized)
    if (isMinimized) {
      setIsOpen(true)
    }
  }

  const handleSend = async () => {
    if (!input.trim()) return

    const userMessage = {
      sender: "user",
      text: input,
      timestamp: new Date().toISOString(),
    }

    setMessages((prev) => [...prev, userMessage])
    setInput("")
    setIsTyping(true)

    try {
      const isArticlePage = location.pathname.includes("/article/")
      const articleId = isArticlePage ? location.pathname.split('/').pop() : null;
      console.log("Article ID:", articleId)
      const currentArticleId = isArticlePage ? articleId : null

      const requestData = {
        message: input,
        article_id: currentArticleId,
      }

      // Log the request data
      console.log("Chatbot request:", requestData)

      const response = await axios({
        method: "post",
        url: "/api/chatbot/",
        headers: { "Content-Type": "application/json" },
        data: requestData,
      })

      setTimeout(() => {
        const botMessage = {
          sender: "bot",
          text: response.data.reply || "I'm not sure how to respond to that.",
          timestamp: new Date().toISOString(),
        }
        setMessages((prev) => [...prev, botMessage])
        setIsTyping(false)
      }, 700)
    } catch (error) {
      console.error("Error:", error)
      setTimeout(() => {
        const botMessage = {
          sender: "bot",
          text: "Sorry, I encountered an error. Please try again later.",
          timestamp: new Date().toISOString(),
          isError: true,
        }
        setMessages((prev) => [...prev, botMessage])
        setIsTyping(false)
      }, 700)
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  // Format timestamp
  const formatTime = (timestamp) => {
    const date = new Date(timestamp)
    return date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })
  }

  return (
    <div className={`chatbot-wrapper ${isOpen ? "open" : ""} ${isMinimized ? "minimized" : ""}`}>
      {isMinimized ? (
        <div className="chatbot-button" onClick={toggleMinimize}>
          <FaRobot />
          <span>Chat with AI</span>
        </div>
      ) : (
        <div className="chatbot-container">
          <div className="chatbot-header">
            <div className="chatbot-title">
              <FaRobot />
              <span>News Assistant</span>
            </div>
            <div className="chatbot-controls">
              <button onClick={toggleMinimize} className="minimize-btn">
                <FaChevronDown />
              </button>
              <button onClick={() => setIsOpen(false)} className="close-btn">
                <FaTimes />
              </button>
            </div>
          </div>

          <div className="chatbot-messages">
            {messages.map((msg, index) => (
              <div
                key={index}
                className={`chatbot-message ${msg.sender === "user" ? "user" : "bot"} ${msg.isError ? "error" : ""}`}
              >
                <div className="message-content">{msg.text}</div>
                <div className="message-timestamp">{formatTime(msg.timestamp)}</div>
              </div>
            ))}

            {isTyping && (
              <div className="chatbot-message bot typing">
                <div className="typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <div className="chatbot-input">
            <textarea
              ref={inputRef}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Type your message..."
              rows={1}
            />
            <button onClick={handleSend} disabled={!input.trim() || isTyping} className={isTyping ? "loading" : ""}>
              {isTyping ? <FaSpinner className="spinner" /> : <FaPaperPlane />}
            </button>
          </div>

          {articleId && (
            <div className="chatbot-context">
              <span>Currently viewing article #{articleId}</span>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default Chatbot

