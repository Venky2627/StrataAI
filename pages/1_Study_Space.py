import streamlit as st
import json
from config.settings import APP_TITLE
from src.ui.theme import get_base_css

st.set_page_config(page_title=f"Study Space - {APP_TITLE}", layout="wide")
st.markdown(get_base_css(), unsafe_allow_html=True)

# --- CUSTOM CSS FOR COMMAND CENTER ---
st.markdown("""
<style>
    .cmd-card {
        background: rgba(30, 30, 36, 0.6);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    .cmd-title {
        color: #f0f0f0;
        font-size: 1.2rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- MAIN LAYOUT ---
col_chat, col_cmd = st.columns([7, 3])

# --- STUDIO (RIGHT COLUMN) ---
with col_cmd:
    st.markdown("<h3 style='margin-bottom: 0.2rem; font-weight: 600;'>Studio</h3>", unsafe_allow_html=True)
    
    active_docs = list(st.session_state.get("documents", {}).keys())
    if active_docs:
        st.markdown(f"<div style='color: #4CAF50; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 1.5rem;'>{len(active_docs)} document(s) active</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div style='color: #A0A0A0; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 1.5rem;'>No documents loaded</div>", unsafe_allow_html=True)
        
    from src.explanations.personas import get_all_personas
    st.markdown("<div style='font-size: 0.9rem; color: #f0f0f0; margin-bottom: 0.5rem;'>Tutor Persona</div>", unsafe_allow_html=True)
    personas_list = get_all_personas()
    selected_persona = st.selectbox("Tutor Persona", personas_list, index=0, label_visibility="collapsed")
    st.session_state.current_persona = selected_persona
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div style='font-size: 0.9rem; color: #f0f0f0; margin-bottom: 0.5rem;'>Generation Tools</div>", unsafe_allow_html=True)
    
    # NotebookLM Style Grid (1-Click Generation)
    grid_col1, grid_col2 = st.columns(2)
    
    with grid_col1:
        if st.button("Generate Quiz", use_container_width=True):
            st.session_state.pending_command = ("quiz", "Multiple Choice")
            st.rerun()
            
        if st.button("Study Planner", use_container_width=True):
            st.session_state.pending_command = ("planner", (7, 2, "Deep Comprehension"))
            st.rerun()
            
    with grid_col2:
        if st.button("Flashcard Deck", use_container_width=True):
            st.session_state.pending_command = ("flashcards", 15)
            st.rerun()
            
        if st.button("Progress Stats", use_container_width=True):
            # This could just jump to the Progress Tracker or spawn a summary
            pass


# --- PROCESS PENDING COMMANDS ---
if "pending_command" in st.session_state and st.session_state.pending_command:
    cmd, args = st.session_state.pending_command
    st.session_state.pending_command = None
    
    if not active_docs:
        st.error("You must upload a document first!")
    else:
        combined_text = ""
        for doc_name in active_docs:
            combined_text += f"\n--- Document: {doc_name} ---\n"
            combined_text += st.session_state.documents[doc_name].get("text", "")
            
        if cmd == "quiz":
            from src.quiz.generator import generate_quiz
            q_type = "mcq" if args == "Multiple Choice" else "short_answer"
            with st.spinner("AI is generating your quiz..."):
                try:
                    chunks = []
                    for doc_name in active_docs:
                        chunks.extend(st.session_state.documents[doc_name].get("chunks", []))
                    quiz_data = generate_quiz(chunks[:20], num_questions=5, quiz_type=q_type)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": f"[QUIZ_JSON]\n{json.dumps(quiz_data)}\n[/QUIZ_JSON]"
                    })
                except Exception as e:
                    st.error(f"Quiz failed: {e}")
                    
        elif cmd == "flashcards":
            from src.quiz.flashcards import generate_flashcards
            with st.spinner("AI is crafting your flashcards..."):
                try:
                    deck = generate_flashcards(combined_text, args)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": f"[FLASHCARD_JSON]\n{json.dumps(deck)}\n[/FLASHCARD_JSON]"
                    })
                except Exception as e:
                    st.error(f"Flashcards failed: {e}")
                    
        elif cmd == "planner":
            from src.study.planner import generate_study_plan
            days, hours, goal = args
            with st.spinner("AI is scheduling your timeline..."):
                try:
                    schedule = generate_study_plan(combined_text, days, hours, goal)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": f"[STUDY_PLAN_JSON]\n{json.dumps(schedule)}\n[/STUDY_PLAN_JSON]"
                    })
                except Exception as e:
                    st.error(f"Planner failed: {e}")


# --- CHAT FEED (LEFT COLUMN) ---
with col_chat:
    st.markdown("""
    <div class="study-header">
        <div class="ai-status">● AI Core Online</div>
        <div class="study-title">Knowledge Interface</div>
        <div class="study-subtitle">A unified space for documents, chats, quizzes, and plans.</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Render messages
    for idx, message in enumerate(st.session_state.messages):
        if message["role"] == "user":
            st.markdown(f"""
            <div style="display: flex; justify-content: flex-end; width: 100%; margin-bottom: 0.5rem;">
                <div style="background: #1e1e24; padding: 12px 22px; border-radius: 24px; color: #f0f0f0; max-width: 75%; font-family: inherit; font-size: 1rem; line-height: 1.5;">
                    {message["content"]}
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            content = message["content"]
            
            # 1. QUIZ RENDERER
            if "[QUIZ_JSON]" in content:
                try:
                    json_str = content.split("[QUIZ_JSON]")[1].split("[/QUIZ_JSON]")[0].strip()
                    quiz = json.loads(json_str)
                    st.markdown("### Interactive Quiz")
                    quiz_state_key = f"inline_quiz_{idx}"
                    if quiz_state_key not in st.session_state:
                        st.session_state[quiz_state_key] = {"answers": {}, "submitted": False, "evaluations": {}}
                    q_state = st.session_state[quiz_state_key]
                    
                    for i, q in enumerate(quiz):
                        q_type = q.get('type', 'mcq')
                        st.markdown(f"**Q{i+1}: {q['question']}**")
                        if q_type == "mcq":
                            selected = st.radio("Select an answer", options=q.get('options', []), key=f"{quiz_state_key}_q_{i}", label_visibility="collapsed", disabled=q_state["submitted"])
                            q_state["answers"][i] = selected
                            if q_state["submitted"]:
                                if selected == q.get('correct_answer'): st.success("Correct!")
                                else: st.error(f"Incorrect. Correct answer: **{q.get('correct_answer')}**")
                                st.info(f"**Explanation:** {q.get('explanation')}")
                        elif q_type == "short_answer":
                            selected = st.text_area("Your Answer", key=f"{quiz_state_key}_q_{i}", label_visibility="collapsed", disabled=q_state["submitted"])
                            q_state["answers"][i] = selected
                            if q_state["submitted"]:
                                score = q_state["evaluations"].get(i, {}).get('score', 0)
                                feedback = q_state["evaluations"].get(i, {}).get('feedback', 'No feedback.')
                                if score >= 8: st.success(f"**Score: {score}/10** - Excellent!")
                                elif score >= 5: st.warning(f"**Score: {score}/10** - Good, but needs work.")
                                else: st.error(f"**Score: {score}/10** - Needs review.")
                                st.info(f"**AI Feedback:** {feedback}")
                                
                    if not q_state["submitted"]:
                        if st.button("Submit Answers", key=f"{quiz_state_key}_btn"):
                            has_short_answer = any(q.get("type") == "short_answer" for q in quiz)
                            if has_short_answer:
                                with st.spinner("AI is grading your answers..."):
                                    from src.quiz.evaluator import evaluate_answer
                                    for i, q in enumerate(quiz):
                                        if q.get("type") == "short_answer":
                                            ans = q_state["answers"].get(i, "").strip()
                                            q_state["evaluations"][i] = evaluate_answer(active_docs, q["question"], ans)
                            try:
                                from src.db.database import log_quiz_result
                                total_mcq = sum([1 for q in quiz if q.get('type', 'mcq') == 'mcq'])
                                mcq_score = sum([1 for i, q in enumerate(quiz) if q.get('type', 'mcq') == 'mcq' and q_state["answers"].get(i) == q.get('correct_answer')])
                                total_sa = sum([1 for q in quiz if q.get('type') == 'short_answer'])
                                sa_score = sum([q_state["evaluations"].get(i, {}).get('score', 0) for i, q in enumerate(quiz) if q.get('type') == 'short_answer'])
                                docs_str = ", ".join(active_docs)
                                if total_mcq > 0: log_quiz_result(docs_str, "Inline MCQ", mcq_score, total_mcq)
                                if total_sa > 0: log_quiz_result(docs_str, "Inline SA", sa_score, total_sa * 10)
                            except Exception as e:
                                pass
                            q_state["submitted"] = True
                            st.rerun()
                except Exception as e:
                    st.error(f"Quiz render failed: {e}")
            
            # 2. FLASHCARD RENDERER
            elif "[FLASHCARD_JSON]" in content:
                try:
                    json_str = content.split("[FLASHCARD_JSON]")[1].split("[/FLASHCARD_JSON]")[0].strip()
                    deck = json.loads(json_str)
                    
                    fc_key = f"fc_{idx}"
                    if fc_key not in st.session_state:
                        st.session_state[fc_key] = {"deck": deck, "mastered": 0, "flipped": False}
                    state = st.session_state[fc_key]
                    
                    st.markdown("### Flashcard Session")
                    if len(state["deck"]) == 0:
                        st.success(f"Session Complete! You mastered {state['mastered']} concepts.")
                    else:
                        st.progress(state["mastered"] / (state["mastered"] + len(state["deck"])))
                        current_card = state["deck"][0]
                        
                        card_bg = "#2a2a35" if not state["flipped"] else "rgba(132, 94, 194, 0.2)"
                        label = "Question" if not state["flipped"] else "Answer"
                        text = current_card.get('front', '') if not state["flipped"] else current_card.get('back', '')
                        
                        st.markdown(f"""
                        <div style="background: {card_bg}; padding: 2rem; border-radius: 12px; text-align: center; border: 1px solid #444; margin: 1rem 0;">
                            <div style="color: #845EC2; font-size: 0.8rem; text-transform: uppercase; margin-bottom: 1rem;">{label}</div>
                            <div style="font-size: 1.4rem; color: white;">{text}</div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        if not state["flipped"]:
                            if st.button("Flip Card", key=f"flip_{idx}"):
                                state["flipped"] = True
                                st.rerun()
                        else:
                            cA, cB = st.columns(2)
                            with cA:
                                if st.button("Review Later", key=f"rev_{idx}", use_container_width=True):
                                    state["deck"].append(state["deck"].pop(0))
                                    state["flipped"] = False
                                    st.rerun()
                            with cB:
                                if st.button("Got It", key=f"got_{idx}", use_container_width=True):
                                    state["deck"].pop(0)
                                    state["mastered"] += 1
                                    state["flipped"] = False
                                    st.rerun()
                except Exception as e:
                    st.error(f"Flashcard render failed: {e}")
                    
            # 3. STUDY PLAN RENDERER
            elif "[STUDY_PLAN_JSON]" in content:
                try:
                    json_str = content.split("[STUDY_PLAN_JSON]")[1].split("[/STUDY_PLAN_JSON]")[0].strip()
                    schedule = json.loads(json_str)
                    
                    st.markdown("### Your Study Timeline")
                    for day_plan in schedule:
                        day_num = day_plan.get("day", "?")
                        title = day_plan.get("title", "Session")
                        time_alloc = day_plan.get("time_allocation", "")
                        topics = "".join([f'<span style="background: rgba(132, 94, 194, 0.2); color: #D6CAEA; padding: 4px 12px; border-radius: 20px; font-size: 0.85rem; margin-right: 8px;">{t}</span>' for t in day_plan.get("topics", [])])
                        actions = "".join([f'<li>{a}</li>' for a in day_plan.get("action_items", [])])
                        tips = day_plan.get("tips", "")
                        
                        card_html = f"""
                        <div style="background: rgba(30,30,36,0.6); border-left: 4px solid #845EC2; padding: 1.5rem; margin-bottom: 1rem; border-radius: 8px;">
                            <div style="color: #FF9671; font-size: 0.9rem; font-weight: bold;">Day {day_num} • {time_alloc}</div>
                            <div style="color: white; font-size: 1.2rem; font-weight: bold; margin-bottom: 0.5rem;">{title}</div>
                            <div style="margin-bottom: 1rem;">{topics}</div>
                            <ul style="color: #ccc;">{actions}</ul>
                        """
                        if tips:
                            card_html += f"<div style='background: rgba(255,107,107,0.1); padding: 8px; border-radius: 4px; color: #FFC7C7; font-style: italic;'>{tips}</div>"
                        card_html += "</div>"
                        st.markdown(card_html, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Planner render failed: {e}")
                    
            # 4. NORMAL CHAT MESSAGE
            else:
                st.markdown(content)
                if "sources" in message and message["sources"]:
                    with st.expander("View Source Documents"):
                        for s_idx, chunk in enumerate(message["sources"]):
                            st.info(f"**Chunk {s_idx+1}:**\n\n{chunk}")


# --- UNIFIED CHAT INPUT + FILE UPLOAD ---
if prompt := st.chat_input("Ask a question, request a quiz, or upload a document...", accept_file="multiple"):
    
    if prompt.files:
        with st.spinner("Extracting text and running AI OCR on images..."):
            from src.document.extractor import extract_text_from_file
            from src.rag.chunker import chunk_text
            from src.embeddings.generator import generate_embeddings
            from src.rag.vectorstore import store_documents
            
            for file in prompt.files:
                try:
                    text = extract_text_from_file(file.read(), file.name)
                    chunks = chunk_text(text)
                    embeddings = generate_embeddings(chunks)
                    store_documents(file.name, chunks, embeddings)
                    
                    if "documents" not in st.session_state:
                        st.session_state.documents = {}
                    st.session_state.documents[file.name] = {"text": text, "chunks": chunks, "embeddings": embeddings}
                except Exception as e:
                    st.error(f"Failed to process {file.name}: {e}")
            st.rerun()

    if prompt.text:
        st.session_state.messages.append({"role": "user", "content": prompt.text})
        with st.spinner("Thinking..."):
            try:
                from src.rag.chain import answer_question
                current_persona = st.session_state.get("current_persona", "Standard Tutor")
                ai_answer, sources = answer_question(prompt.text, active_documents=active_docs, persona_name=current_persona)
                st.session_state.messages.append({"role": "assistant", "content": ai_answer, "sources": sources})
                st.rerun()
            except Exception as e:
                st.error(f"Error communicating with AI: {e}")
