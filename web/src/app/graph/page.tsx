"use client";

import { motion } from "framer-motion";
import { ArrowLeft, Network, Settings, ZoomIn, ZoomOut, Database } from "lucide-react";
import Link from "next/link";
import { useCallback } from "react";
import {
  ReactFlow,
  MiniMap,
  Controls,
  Background,
  useNodesState,
  useEdgesState,
  addEdge,
  BackgroundVariant,
} from "@xyflow/react";
import "@xyflow/react/dist/style.css";

const initialNodes = [
  { id: "1", position: { x: 250, y: 50 }, data: { label: "Artificial Intelligence" }, style: { background: "#0A0A0A", color: "#fff", border: "1px solid rgba(255,255,255,0.2)", borderRadius: "8px", padding: "10px 20px" } },
  { id: "2", position: { x: 100, y: 150 }, data: { label: "Machine Learning" }, style: { background: "#0A0A0A", color: "#fff", border: "1px solid rgba(255,255,255,0.2)", borderRadius: "8px", padding: "10px 20px" } },
  { id: "3", position: { x: 400, y: 150 }, data: { label: "Neural Networks" }, style: { background: "#0A0A0A", color: "#fff", border: "1px solid rgba(255,255,255,0.2)", borderRadius: "8px", padding: "10px 20px" } },
  { id: "4", position: { x: 400, y: 250 }, data: { label: "Deep Learning" }, style: { background: "#0A0A0A", color: "#fff", border: "1px solid rgba(16, 185, 129, 0.5)", borderRadius: "8px", padding: "10px 20px" } },
];

const initialEdges = [
  { id: "e1-2", source: "1", target: "2", animated: true, style: { stroke: "rgba(255,255,255,0.4)" } },
  { id: "e1-3", source: "1", target: "3", animated: true, style: { stroke: "rgba(255,255,255,0.4)" } },
  { id: "e3-4", source: "3", target: "4", animated: true, style: { stroke: "rgba(16, 185, 129, 0.8)", strokeWidth: 2 } },
];

export default function KnowledgeGraphPage() {
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);

  const onConnect = useCallback(
    (params: any) => setEdges((eds) => addEdge({ ...params, animated: true, style: { stroke: "rgba(255,255,255,0.4)" } }, eds)),
    [setEdges],
  );

  return (
    <div className="h-screen w-screen bg-background overflow-hidden text-foreground flex flex-col selection:bg-white/20">
      
      {/* Top Navbar */}
      <nav className="w-full border-b border-border-subtle bg-background/50 backdrop-blur-md absolute top-0 z-50">
        <div className="px-6 h-14 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Link href="/workspace" className="p-1.5 rounded-md hover:bg-white/10 transition-colors text-foreground-muted hover:text-white">
              <ArrowLeft className="w-4 h-4" />
            </Link>
            <div className="font-mono font-bold text-sm tracking-tighter flex items-center gap-2">
              <div className="w-2.5 h-2.5 rounded-full bg-white shadow-[0_0_8px_rgba(255,255,255,0.4)]" />
              KNOWLEDGE GRAPH
            </div>
          </div>
          <div className="flex items-center gap-3">
            <button className="flex items-center gap-1.5 text-xs font-medium text-foreground-muted hover:text-white transition-colors bg-white/5 px-3 py-1.5 rounded border border-border-subtle">
              <Database className="w-3.5 h-3.5" /> Re-index Graph
            </button>
            <button className="flex items-center gap-1.5 text-xs font-medium text-foreground-muted hover:text-white transition-colors bg-white/5 px-3 py-1.5 rounded border border-border-subtle">
              <Settings className="w-3.5 h-3.5" /> View Options
            </button>
          </div>
        </div>
      </nav>

      {/* Full Screen React Flow Canvas */}
      <main className="flex-1 w-full relative pt-14">
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          onConnect={onConnect}
          fitView
          className="bg-background"
          proOptions={{ hideAttribution: true }}
        >
          {/* Custom controls hidden via CSS, using built-in for simplicity initially */}
          <Controls className="!bg-surface !border-border-subtle !fill-white" />
          <Background variant={BackgroundVariant.Dots} gap={24} size={1} color="rgba(255,255,255,0.05)" />
        </ReactFlow>

        {/* Floating Info Card */}
        <motion.div 
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          className="absolute bottom-6 left-6 glass p-4 rounded-xl border border-border-subtle w-72 select-none"
        >
          <h3 className="text-sm font-semibold mb-1 flex items-center gap-2">
            <Network className="w-4 h-4" /> Semantic Mapping
          </h3>
          <p className="text-xs text-foreground-muted leading-relaxed">
            This graph dynamically maps relationships between concepts in your active documents using vector embeddings.
          </p>
        </motion.div>
      </main>
    </div>
  );
}
