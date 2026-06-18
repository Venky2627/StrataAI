"use client";

import { motion } from "framer-motion";
import { ArrowLeft, BrainCircuit, Activity, Target, Zap, Clock, TrendingUp } from "lucide-react";
import Link from "next/link";

export default function CognitiveProfilePage() {
  return (
    <div className="min-h-screen bg-background overflow-hidden text-foreground selection:bg-white/20">
      
      {/* Top Navbar */}
      <nav className="w-full border-b border-border-subtle bg-background/50 backdrop-blur-md sticky top-0 z-50">
        <div className="px-6 h-14 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Link href="/workspace" className="p-1.5 rounded-md hover:bg-white/10 transition-colors text-foreground-muted hover:text-white">
              <ArrowLeft className="w-4 h-4" />
            </Link>
            <div className="font-mono font-bold text-sm tracking-tighter flex items-center gap-2">
              <div className="w-2.5 h-2.5 rounded-full bg-white shadow-[0_0_8px_rgba(255,255,255,0.4)]" />
              COGNITIVE PROFILE
            </div>
          </div>
          <div className="text-xs font-mono text-success flex items-center gap-2">
            <span className="w-1.5 h-1.5 rounded-full bg-success animate-pulse" />
            Syncing Telemetry
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-6xl mx-auto px-6 py-12">
        
        {/* Header Section */}
        <div className="mb-10">
          <motion.h1 
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-3xl font-semibold tracking-tight mb-2 select-none"
          >
            Learning Analytics
          </motion.h1>
          <motion.p 
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="text-foreground-muted select-none"
          >
            Real-time telemetry on your knowledge retention and study patterns.
          </motion.p>
        </div>

        {/* Metrics Grid */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
          {[
            { title: "Learning Velocity", value: "85%", icon: Zap, trend: "+12%" },
            { title: "Mastery Index", value: "4.2", icon: Target, trend: "+0.4" },
            { title: "Active Concepts", value: "142", icon: BrainCircuit, trend: "+24" },
            { title: "Deep Work Hours", value: "18.5h", icon: Clock, trend: "-2.1h" },
          ].map((metric, i) => (
            <motion.div 
              key={i}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 + (i * 0.05) }}
              className="glass p-5 rounded-xl border border-border-subtle flex flex-col justify-between hover:border-border-focus transition-colors cursor-default select-none"
            >
              <div className="flex items-center justify-between mb-4 text-foreground-muted">
                <span className="text-xs font-medium uppercase tracking-wider">{metric.title}</span>
                <metric.icon className="w-4 h-4" />
              </div>
              <div className="flex items-baseline gap-2">
                <span className="text-3xl font-semibold">{metric.value}</span>
                <span className={`text-xs font-medium ${metric.trend.startsWith('+') ? 'text-success' : 'text-red-400'}`}>
                  {metric.trend}
                </span>
              </div>
            </motion.div>
          ))}
        </div>

        {/* Detailed Charts Area (Placeholders for Vercel/Linear style graph) */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
            className="md:col-span-2 glass rounded-xl border border-border-subtle p-6 h-[400px] flex flex-col select-none"
          >
            <div className="flex items-center justify-between mb-6">
              <h3 className="font-semibold flex items-center gap-2"><Activity className="w-4 h-4" /> Retention Curve</h3>
              <select className="bg-transparent border border-border-subtle rounded-md text-xs px-2 py-1 outline-none text-foreground-muted">
                <option>Last 30 Days</option>
                <option>Last 7 Days</option>
              </select>
            </div>
            {/* Fake Graph Area */}
            <div className="flex-1 w-full relative flex items-end justify-between px-2 pb-6 border-b border-border-subtle/30">
              {/* Grid lines */}
              <div className="absolute inset-0 flex flex-col justify-between pointer-events-none">
                <div className="w-full h-px bg-border-subtle/20" />
                <div className="w-full h-px bg-border-subtle/20" />
                <div className="w-full h-px bg-border-subtle/20" />
                <div className="w-full h-px bg-border-subtle/20" />
              </div>
              
              {/* Bars */}
              {[40, 55, 30, 70, 90, 65, 80, 95, 85, 100].map((height, i) => (
                <div key={i} className="w-[8%] bg-white/20 hover:bg-white/40 transition-colors rounded-t-sm relative group" style={{ height: `${height}%` }}>
                  {/* Tooltip */}
                  <div className="absolute -top-8 left-1/2 -translate-x-1/2 opacity-0 group-hover:opacity-100 transition-opacity bg-surface px-2 py-1 rounded text-[10px] whitespace-nowrap border border-border-subtle">
                    Score: {height}%
                  </div>
                </div>
              ))}
            </div>
          </motion.div>

          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5 }}
            className="glass rounded-xl border border-border-subtle p-6 flex flex-col select-none"
          >
            <h3 className="font-semibold flex items-center gap-2 mb-6"><TrendingUp className="w-4 h-4" /> Concept Mastery</h3>
            <div className="flex-1 space-y-4">
              
              {/* Mastery Items */}
              {[
                { name: "Quantum Entanglement", val: 95 },
                { name: "Backpropagation", val: 82 },
                { name: "Cellular Respiration", val: 64 },
                { name: "Market Equilibrium", val: 45 },
              ].map((item, i) => (
                <div key={i}>
                  <div className="flex justify-between text-xs mb-1.5">
                    <span className="text-foreground-muted">{item.name}</span>
                    <span>{item.val}%</span>
                  </div>
                  <div className="w-full h-1.5 bg-white/10 rounded-full overflow-hidden">
                    <div className={`h-full rounded-full ${item.val > 80 ? 'bg-success' : item.val > 60 ? 'bg-white' : 'bg-white/30'}`} style={{ width: `${item.val}%` }} />
                  </div>
                </div>
              ))}

            </div>
          </motion.div>

        </div>

      </main>
    </div>
  );
}
