"use client";

import { useEffect, useRef } from "react";
import { motion } from "framer-motion";
import { ArrowRight, BrainCircuit, Network, Zap, GitCommit, Database, Activity, Target } from "lucide-react";
import Link from "next/link";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import Lenis from "lenis";
import { ReactFlow, Background, Controls } from "@xyflow/react";
import "@xyflow/react/dist/style.css";

gsap.registerPlugin(ScrollTrigger);

export default function LandingPage() {
  const containerRef = useRef<HTMLDivElement>(null);
  const morphTextRef = useRef<HTMLDivElement>(null);
  const graphContainerRef = useRef<HTMLDivElement>(null);
  const tutorDemoRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // Initialize Lenis Smooth Scroll
    const lenis = new Lenis({
      duration: 1.2,
      easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
      orientation: "vertical",
      gestureOrientation: "vertical",
      smoothWheel: true,
      wheelMultiplier: 1,
      touchMultiplier: 2,
    });

    function raf(time: number) {
      lenis.raf(time);
      requestAnimationFrame(raf);
    }
    requestAnimationFrame(raf);

    // GSAP Pinned Morphing Text (Section 2)
    const morphWords = ["DOCUMENTS", "UNDERSTANDING", "REASONING", "MASTERY"];
    const tl = gsap.timeline({
      scrollTrigger: {
        trigger: "#pinned-section",
        start: "top top",
        end: "+=3000",
        scrub: 1,
        pin: true,
      }
    });

    // Animate morphing text
    morphWords.forEach((word, i) => {
      if (i > 0) {
        tl.to("#morph-text", {
          opacity: 0,
          y: -50,
          duration: 1,
          ease: "power2.inOut",
        }).set("#morph-text", {
          innerHTML: word,
          y: 50,
        }).to("#morph-text", {
          opacity: 1,
          y: 0,
          duration: 1,
          ease: "power2.inOut",
        });
      }
    });

    // GSAP Knowledge Graph Reveal (Section 3)
    gsap.fromTo(
      graphContainerRef.current,
      { opacity: 0, scale: 0.8, filter: "blur(20px)" },
      {
        opacity: 1,
        scale: 1,
        filter: "blur(0px)",
        ease: "power3.out",
        scrollTrigger: {
          trigger: "#graph-section",
          start: "top 60%",
          end: "top 20%",
          scrub: 1,
        }
      }
    );

    // Cleanup
    return () => {
      lenis.destroy();
      ScrollTrigger.getAll().forEach(t => t.kill());
    };
  }, []);

  return (
    <div ref={containerRef} className="bg-background text-foreground overflow-x-hidden selection:bg-white/20">
      
      {/* Navbar */}
      <nav className="fixed top-0 w-full z-50 border-b border-border-subtle bg-background/50 backdrop-blur-md select-none">
        <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
          <Link href="/" className="flex items-center gap-2 font-mono font-bold text-lg tracking-tighter hover:text-white/80 transition-colors">
            <div className="w-4 h-4 rounded-full bg-white shadow-[0_0_10px_rgba(255,255,255,0.5)]" />
            STRATA
          </Link>
          <div className="flex items-center gap-6 text-sm text-foreground-muted">
            <Link href="/workspace" className="text-white font-medium hover:opacity-80 transition-opacity flex items-center gap-1">
              Enter Workspace <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
        </div>
      </nav>

      {/* SECTION 1: Fullscreen Hero */}
      <section className="relative h-screen flex flex-col items-center justify-center text-center px-6 noise-bg select-none">
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[80vw] h-[80vw] max-w-[800px] max-h-[800px] rounded-full bg-white/5 blur-[150px] pointer-events-none" />
        
        <motion.div 
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 1.5, ease: [0.16, 1, 0.3, 1] }}
          className="relative z-10"
        >
          <h1 className="text-7xl md:text-9xl font-bold tracking-tighter leading-[0.9] mb-6">
            STRATA <span className="text-foreground-muted">OS</span>
          </h1>
          <h2 className="text-3xl md:text-5xl font-medium tracking-tight mb-8 text-gradient">
            Your Second Brain.
          </h2>
          <p className="text-xl md:text-2xl text-foreground-muted max-w-2xl mx-auto font-light">
            Learn at the speed of thought.
          </p>
        </motion.div>
        
        {/* Animated Scroll Indicator */}
        <motion.div 
          animate={{ y: [0, 10, 0] }}
          transition={{ repeat: Infinity, duration: 2, ease: "easeInOut" }}
          className="absolute bottom-10 left-1/2 -translate-x-1/2 flex flex-col items-center gap-2 text-foreground-muted/50 text-xs tracking-widest uppercase"
        >
          <div className="w-px h-12 bg-gradient-to-b from-transparent via-white/50 to-transparent" />
          Scroll
        </motion.div>
      </section>

      {/* SECTION 2: Pinned Morphing Text */}
      <section id="pinned-section" className="h-screen w-full flex items-center justify-center bg-surface select-none relative overflow-hidden">
        <div className="absolute inset-0 noise-bg opacity-50" />
        <div className="z-10 text-center flex flex-col items-center justify-center h-full w-full">
          <p className="text-sm font-mono text-foreground-muted uppercase tracking-[0.3em] mb-8">The Learning Pipeline</p>
          <div className="h-[120px] md:h-[200px] flex items-center justify-center overflow-hidden w-full">
            <h2 id="morph-text" className="text-6xl md:text-[8rem] font-bold tracking-tighter text-white">
              DOCUMENTS
            </h2>
          </div>
        </div>
      </section>

      {/* SECTION 3: Knowledge Graph Reveal */}
      <section id="graph-section" className="min-h-screen py-32 px-6 flex flex-col items-center select-none bg-background relative border-t border-border-subtle">
        <div className="max-w-4xl mx-auto text-center mb-16">
          <h2 className="text-4xl md:text-6xl font-bold tracking-tight mb-6">Semantic Explosion.</h2>
          <p className="text-xl text-foreground-muted">Watch flat documents transform into a living, multi-dimensional neural web.</p>
        </div>
        
        <div ref={graphContainerRef} className="w-full max-w-6xl h-[600px] glass rounded-3xl overflow-hidden border border-border-subtle shadow-[0_0_100px_rgba(255,255,255,0.05)] relative">
          <div className="absolute top-4 left-4 z-10 flex items-center gap-2 px-3 py-1.5 rounded-full bg-white/10 text-xs font-medium border border-white/10 backdrop-blur-md">
            <Network className="w-3 h-3" /> Live Graph Demo
          </div>
          <ReactFlow 
            nodes={[
              { id: '1', position: { x: 250, y: 100 }, data: { label: 'Quantum Field Theory' }, style: { background: '#050505', color: '#fff', border: '1px solid rgba(255,255,255,0.2)', padding: 15, borderRadius: 8 } },
              { id: '2', position: { x: 100, y: 250 }, data: { label: 'Schrodinger Equation' }, style: { background: '#050505', color: '#fff', border: '1px solid rgba(255,255,255,0.2)', padding: 15, borderRadius: 8 } },
              { id: '3', position: { x: 400, y: 250 }, data: { label: 'Wave Function' }, style: { background: '#050505', color: '#fff', border: '1px solid rgba(255,255,255,0.2)', padding: 15, borderRadius: 8 } },
              { id: '4', position: { x: 250, y: 400 }, data: { label: 'Probability Density' }, style: { background: '#050505', color: '#fff', border: '1px solid #10B981', padding: 15, borderRadius: 8 } },
            ]}
            edges={[
              { id: 'e1-2', source: '1', target: '2', animated: true, style: { stroke: 'rgba(255,255,255,0.5)' } },
              { id: 'e1-3', source: '1', target: '3', animated: true, style: { stroke: 'rgba(255,255,255,0.5)' } },
              { id: 'e2-4', source: '2', target: '4', animated: true, style: { stroke: '#10B981' } },
              { id: 'e3-4', source: '3', target: '4', animated: true, style: { stroke: '#10B981' } },
            ]}
            fitView
            proOptions={{ hideAttribution: true }}
            panOnScroll={false}
            zoomOnScroll={false}
          >
            <Background color="rgba(255,255,255,0.05)" />
          </ReactFlow>
        </div>
      </section>

      {/* SECTION 4 & 5: Agentic System & AI Tutor */}
      <section className="py-32 px-6 bg-surface border-t border-border-subtle noise-bg select-none">
        <div className="max-w-7xl mx-auto">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-24 items-center">
            
            <div>
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-border-subtle bg-white/5 mb-6 text-sm font-mono">
                <Database className="w-4 h-4 text-success" /> Multi-Agent Architecture
              </div>
              <h2 className="text-4xl md:text-5xl font-bold tracking-tight mb-6">An Operating System,<br/>Not a Chatbot.</h2>
              <p className="text-lg text-foreground-muted mb-8">
                StrataAI utilizes a swarm of specialized autonomous agents. While you read, the Memory Agent indexes concepts, the Evaluation Agent tracks your weaknesses, and the Tutor Agent generates adaptive quizzes.
              </p>
              
              <div className="space-y-4">
                {['Planner Agent', 'Research Agent', 'Evaluation Agent'].map((agent, i) => (
                  <div key={i} className="flex items-center gap-4 p-4 rounded-xl border border-border-subtle glass hover:glass-hover transition-all">
                    <div className="w-10 h-10 rounded-lg bg-white/10 flex items-center justify-center">
                      <BrainCircuit className="w-5 h-5 text-white" />
                    </div>
                    <div className="font-medium">{agent}</div>
                    <div className="ml-auto w-2 h-2 rounded-full bg-success shadow-[0_0_8px_#10B981]" />
                  </div>
                ))}
              </div>
            </div>

            <div className="relative h-[600px] w-full glass rounded-3xl border border-border-subtle shadow-2xl p-6 flex flex-col">
              <div className="flex items-center gap-2 mb-6 border-b border-border-subtle pb-4">
                <div className="w-3 h-3 rounded-full bg-red-500/50" />
                <div className="w-3 h-3 rounded-full bg-yellow-500/50" />
                <div className="w-3 h-3 rounded-full bg-green-500/50" />
              </div>
              
              <div className="flex-1 space-y-6">
                <div className="flex gap-4">
                  <div className="w-8 h-8 rounded-full bg-white/10 flex-shrink-0" />
                  <div className="p-4 rounded-2xl bg-white/5 border border-white/10 text-sm">
                    Can you explain backpropagation as if I were a 5 year old?
                  </div>
                </div>
                
                <div className="flex gap-4">
                  <div className="w-8 h-8 rounded-full bg-white flex items-center justify-center flex-shrink-0">
                    <div className="w-4 h-4 rounded-full bg-black" />
                  </div>
                  <div className="flex-1">
                    <div className="flex items-center gap-2 text-xs text-foreground-muted mb-2 font-mono">
                      <GitCommit className="w-3 h-3 animate-spin" /> Retrieving Neural Network contexts...
                    </div>
                    <div className="p-4 rounded-2xl bg-white text-black text-sm font-medium">
                      Imagine you are trying to throw a ball into a bucket...
                    </div>
                  </div>
                </div>
              </div>
            </div>

          </div>
        </div>
      </section>

      {/* SECTION 6: Cognitive Profile */}
      <section className="py-32 px-6 border-t border-border-subtle select-none">
        <div className="max-w-7xl mx-auto text-center">
          <h2 className="text-4xl md:text-6xl font-bold tracking-tight mb-16">Metrics that matter.</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="glass p-10 rounded-3xl border border-border-subtle flex flex-col items-center justify-center hover:scale-[1.02] transition-transform duration-500">
              <Activity className="w-8 h-8 text-white mb-6 opacity-50" />
              <div className="text-6xl font-bold mb-2">94<span className="text-3xl text-foreground-muted">%</span></div>
              <div className="text-sm font-mono text-success tracking-widest uppercase">Retention Rate</div>
            </div>
            
            <div className="glass p-10 rounded-3xl border border-border-subtle flex flex-col items-center justify-center hover:scale-[1.02] transition-transform duration-500">
              <Zap className="w-8 h-8 text-white mb-6 opacity-50" />
              <div className="text-6xl font-bold mb-2">12.4<span className="text-3xl text-foreground-muted">x</span></div>
              <div className="text-sm font-mono text-success tracking-widest uppercase">Learning Velocity</div>
            </div>

            <div className="glass p-10 rounded-3xl border border-border-subtle flex flex-col items-center justify-center hover:scale-[1.02] transition-transform duration-500">
              <Target className="w-8 h-8 text-white mb-6 opacity-50" />
              <div className="text-6xl font-bold mb-2">850</div>
              <div className="text-sm font-mono text-success tracking-widest uppercase">Concepts Mastered</div>
            </div>
          </div>
        </div>
      </section>

      {/* SECTION 7: Final CTA */}
      <section className="min-h-screen flex flex-col items-center justify-center text-center px-6 relative bg-surface noise-bg border-t border-border-subtle select-none">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,rgba(255,255,255,0.05),transparent_50%)]" />
        
        <h2 className="text-6xl md:text-8xl font-bold tracking-tighter mb-12 relative z-10 text-gradient">
          Build Your Second Brain.
        </h2>
        
        <Link 
          href="/workspace" 
          className="relative z-10 group flex items-center justify-center gap-3 px-10 py-5 bg-white text-black font-semibold rounded-full overflow-hidden transition-transform hover:scale-[1.02] active:scale-[0.98] text-lg"
        >
          <span className="relative z-10 flex items-center gap-2">
            Start Learning Smarter <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
          </span>
        </Link>
      </section>

    </div>
  );
}

