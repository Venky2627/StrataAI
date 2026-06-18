"use client";

import { motion } from "framer-motion";
import { ArrowUp, BookOpen, BrainCircuit, FileText, Settings, LayoutDashboard, Target, Zap, LayoutGrid, CheckCircle, Network, Database } from "lucide-react";
import Link from "next/link";
import { useState, useRef, useEffect } from "react";
import { sendChatMessage, ChatMessage } from "@/lib/api";

export default function WorkspacePage() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const handleSubmit = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage = input.trim();
    setInput("");
    
    // Add user message immediately
    const newHistory: ChatMessage[] = [...messages, { role: "user", content: userMessage }];
    setMessages(newHistory);
    setIsLoading(true);

    try {
      // Send to backend
      const res = await sendChatMessage(userMessage, messages);
      setMessages([...newHistory, { role: "assistant", content: res.response }]);
    } catch (error) {
      console.error(error);
      setMessages([...newHistory, { role: "assistant", content: "⚠️ Connection error. Make sure the FastAPI backend is running on port 8000." }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex h-screen bg-background overflow-hidden text-foreground">
      
      {/* 1. LEFT COLUMN - Knowledge Navigator */}
      <aside className="w-64 border-r border-border-subtle bg-surface/30 backdrop-blur-md flex flex-col hidden lg:flex select-none flex-shrink-0 z-20">
        <Link href="/" className="p-4 border-b border-border-subtle flex items-center gap-2 font-mono font-bold text-sm tracking-tighter hover:text-white/80 transition-colors cursor-pointer">
          <div className="w-3 h-3 rounded-full bg-white shadow-[0_0_8px_rgba(255,255,255,0.4)]" />
          STRATA OS
        </Link>
        
        <div className="p-4 flex-1 overflow-y-auto space-y-8">
          
          <div>
            <div className="text-xs font-semibold text-foreground-muted mb-3 tracking-widest uppercase flex items-center gap-2"><LayoutGrid className="w-3 h-3"/> Core Systems</div>
            <nav className="space-y-1">
              <Link href="/workspace" className="flex items-center gap-2 px-2 py-1.5 rounded-md bg-white/10 text-sm font-medium border border-white/5">
                <BrainCircuit className="w-4 h-4" /> Reasoning Engine
              </Link>
              <Link href="/profile" className="flex items-center gap-2 px-2 py-1.5 rounded-md text-foreground-muted hover:text-white hover:bg-white/5 transition-colors text-sm font-medium">
                <Target className="w-4 h-4" /> Cognitive Profile
              </Link>
              <Link href="/graph" className="flex items-center gap-2 px-2 py-1.5 rounded-md text-foreground-muted hover:text-white hover:bg-white/5 transition-colors text-sm font-medium">
                <Network className="w-4 h-4" /> Neural Graph
              </Link>
            </nav>
          </div>

          <div>
            <div className="text-xs font-semibold text-foreground-muted mb-3 tracking-widest uppercase flex items-center gap-2"><Database className="w-3 h-3"/> Active Context</div>
            <div className="space-y-1">
              <div className="flex items-center gap-2 px-2 py-1.5 rounded-md text-sm text-foreground-muted hover:text-white hover:bg-white/5 cursor-pointer transition-colors group">
                <FileText className="w-3.5 h-3.5 text-white/40 group-hover:text-white transition-colors" /> quantum_mechanics.pdf
              </div>
              <div className="flex items-center gap-2 px-2 py-1.5 rounded-md text-sm text-foreground-muted hover:text-white hover:bg-white/5 cursor-pointer transition-colors group">
                <FileText className="w-3.5 h-3.5 text-white/40 group-hover:text-white transition-colors" /> neuro_bio_ch4.docx
              </div>
            </div>
            <button className="mt-4 w-full py-2 border border-dashed border-border-subtle rounded-md text-xs font-medium text-foreground-muted hover:text-white hover:border-white/20 transition-all bg-white/5 hover:bg-white/10">
              + Ingest Document
            </button>
          </div>

        </div>
      </aside>

      {/* 2. CENTER COLUMN - Main AI Workspace */}
      <main className="flex-1 flex flex-col relative bg-background noise-bg z-10 min-w-0">
        
        {/* Chat History Area */}
        <div className="flex-1 overflow-y-auto p-6 flex flex-col pt-12 pb-40">
          <div className="max-w-3xl w-full mx-auto space-y-8">
            
            {messages.length === 0 ? (
              <motion.div 
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
                className="mt-32 flex flex-col items-center text-center select-none"
              >
                <div className="w-16 h-16 rounded-2xl glass flex items-center justify-center mb-6 shadow-[0_0_30px_rgba(255,255,255,0.05)] border border-border-subtle">
                  <BrainCircuit className="w-8 h-8 text-white/80" />
                </div>
                <h2 className="text-2xl font-semibold mb-2 tracking-tight">System initialized.</h2>
                <p className="text-foreground-muted text-sm font-light">
                  Upload a source document or ask a question to begin building semantic memory.
                </p>
              </motion.div>
            ) : (
              messages.map((msg, idx) => (
                <motion.div 
                  key={idx}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div className={`max-w-[85%] rounded-2xl p-4 text-[15px] leading-relaxed ${
                    msg.role === 'user' 
                      ? 'bg-white text-black' 
                      : 'bg-transparent text-white border-l-2 border-white/20 pl-6 rounded-none whitespace-pre-wrap'
                  }`}>
                    {msg.role === 'assistant' && (
                      <div className="flex items-center gap-2 mb-2 select-none">
                        <div className="relative w-5 h-5 flex items-center justify-center">
                          <motion.div 
                            animate={{ rotate: 360 }} 
                            transition={{ duration: 4, repeat: Infinity, ease: "linear" }} 
                            className="absolute inset-0 rounded-[4px] border border-white/20 border-t-white/80" 
                          />
                          <motion.div 
                            animate={{ scale: [0.8, 1.2, 0.8], opacity: [0.5, 1, 0.5] }} 
                            transition={{ duration: 2, repeat: Infinity, ease: "easeInOut" }}
                            className="w-1.5 h-1.5 rounded-full bg-white shadow-[0_0_8px_rgba(255,255,255,0.8)]" 
                          />
                        </div>
                        <span className="font-semibold text-xs uppercase tracking-widest text-foreground-muted">Tutor Agent</span>
                      </div>
                    )}
                    {msg.content}
                  </div>
                </motion.div>
              ))
            )}

            {isLoading && (
              <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="flex justify-start">
                <div className="bg-transparent text-white border-l-2 border-white/20 pl-6 py-2">
                  <div className="flex items-center gap-2">
                    <div className="w-1.5 h-1.5 rounded-full bg-white/50 animate-bounce" style={{ animationDelay: '0ms' }} />
                    <div className="w-1.5 h-1.5 rounded-full bg-white/50 animate-bounce" style={{ animationDelay: '150ms' }} />
                    <div className="w-1.5 h-1.5 rounded-full bg-white/50 animate-bounce" style={{ animationDelay: '300ms' }} />
                  </div>
                </div>
              </motion.div>
            )}
            
            <div ref={messagesEndRef} />
          </div>
        </div>

        {/* Floating Input Area */}
        <div className="p-6 w-full max-w-3xl mx-auto absolute bottom-0 left-1/2 -translate-x-1/2 select-none z-20 bg-gradient-to-t from-background via-background to-transparent pt-10">
          <div className="relative glass rounded-2xl p-2 shadow-[0_20px_50px_rgba(0,0,0,0.5)] focus-within:ring-1 focus-within:ring-white/20 transition-all border border-border-focus">
            <textarea 
              className="w-full bg-transparent resize-none text-white placeholder-foreground-muted outline-none px-3 py-3 text-[15px] min-h-[60px] max-h-[200px] select-text"
              placeholder="Ask anything or use '/' for commands..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault();
                  handleSubmit();
                }
              }}
            />
            
            <div className="flex items-center justify-between px-2 pt-2 border-t border-border-subtle/50 mt-1">
              <div className="flex items-center gap-3 text-xs font-medium text-foreground-muted">
                <span className="flex items-center gap-1 cursor-pointer hover:text-white transition-colors bg-white/5 px-2 py-1 rounded"><FileText className="w-3 h-3"/> Attach</span>
                <span className="flex items-center gap-1 cursor-pointer hover:text-white transition-colors bg-white/5 px-2 py-1 rounded"><Settings className="w-3 h-3"/> Model: Omni</span>
              </div>
              <button 
                onClick={handleSubmit}
                disabled={isLoading || !input.trim()}
                className={`w-8 h-8 rounded-full flex items-center justify-center transition-all ${input.trim().length > 0 ? 'bg-white text-black scale-100 hover:scale-105' : 'bg-white/10 text-white/40 scale-95'} ${isLoading ? 'opacity-50 cursor-not-allowed' : ''}`}
              >
                <ArrowUp className="w-4 h-4" />
              </button>
            </div>
          </div>
          <div className="text-center mt-3 text-[10px] text-foreground-muted/40 uppercase tracking-widest font-mono pb-2">
            StrataAI • Encrypted Telemetry Active
          </div>
        </div>
      </main>

      {/* 3. RIGHT COLUMN - AI Studio */}
      <aside className="w-72 border-l border-border-subtle bg-surface/30 backdrop-blur-md flex flex-col hidden xl:flex select-none flex-shrink-0 z-20">
        <div className="p-4 border-b border-border-subtle flex items-center gap-2 text-sm font-semibold tracking-tight">
          <Zap className="w-4 h-4 text-success" /> AI Studio
        </div>
        
        <div className="p-4 flex-1 overflow-y-auto space-y-6">
          
          <div>
            <div className="text-xs font-semibold text-foreground-muted mb-3 tracking-widest uppercase">Generators</div>
            <div className="grid grid-cols-2 gap-2">
              <button className="glass flex flex-col items-center justify-center p-4 rounded-xl hover:glass-hover transition-all text-xs font-medium text-foreground-muted hover:text-white gap-2 group">
                <CheckCircle className="w-5 h-5 text-white/50 group-hover:text-white transition-colors" /> Generate Quiz
              </button>
              <button className="glass flex flex-col items-center justify-center p-4 rounded-xl hover:glass-hover transition-all text-xs font-medium text-foreground-muted hover:text-white gap-2 group">
                <BookOpen className="w-5 h-5 text-white/50 group-hover:text-white transition-colors" /> Flashcards
              </button>
              <button className="glass flex flex-col items-center justify-center p-4 rounded-xl hover:glass-hover transition-all text-xs font-medium text-foreground-muted hover:text-white gap-2 group">
                <Target className="w-5 h-5 text-white/50 group-hover:text-white transition-colors" /> Study Plan
              </button>
              <button className="glass flex flex-col items-center justify-center p-4 rounded-xl hover:glass-hover transition-all text-xs font-medium text-foreground-muted hover:text-white gap-2 group">
                <BrainCircuit className="w-5 h-5 text-white/50 group-hover:text-white transition-colors" /> Analysis
              </button>
            </div>
          </div>

          <div>
            <div className="text-xs font-semibold text-foreground-muted mb-3 tracking-widest uppercase">System Status</div>
            <div className="space-y-2 text-xs">
              <div className="flex justify-between items-center bg-white/5 px-3 py-2 rounded-lg border border-border-subtle">
                <span className="text-foreground-muted">Memory Agent</span>
                <span className="text-success flex items-center gap-1.5"><span className="w-1.5 h-1.5 rounded-full bg-success animate-pulse" /> Active</span>
              </div>
              <div className="flex justify-between items-center bg-white/5 px-3 py-2 rounded-lg border border-border-subtle">
                <span className="text-foreground-muted">Tutor Agent</span>
                <span className="text-success flex items-center gap-1.5"><span className="w-1.5 h-1.5 rounded-full bg-success animate-pulse" /> Active</span>
              </div>
              <div className="flex justify-between items-center bg-white/5 px-3 py-2 rounded-lg border border-border-subtle">
                <span className="text-foreground-muted">Context Window</span>
                <span className="font-mono text-white/80">32% Used</span>
              </div>
            </div>
          </div>

        </div>
      </aside>

    </div>
  );
}

