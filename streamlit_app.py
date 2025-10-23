import streamlit as st
from mistralai import Mistral
from dotenv import load_dotenv
import random
import os
import time
import math

load_dotenv()
api_key = os.getenv("MISTRAL_API_KEY")

spin_the_wheel = [
    "as a cooking recipe",
    "as a breakup text",
    "as a conspiracy theory",
    "as a haiku",
    "as if you are an 8-year-old explaining",
    "as a Shakespearean monologue",
    "as a love letter"
]

# Colors for each segment
COLORS = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#FFA07A", "#98D8C8", "#F7DC6F", "#BB8FCE"]

def response_to_user(topic, model_response):
    client = Mistral(api_key=api_key)

    prompt = f"""
        You are a fun and engaging AI assistant.
        Your task:
        1. Define the topic **{topic}** briefly in one sentence (about 15% of the total).
        2. Then explain it creatively, humorously, and conversationally (about 75% of the total).
        3. Present the explanation {model_response}.

        Format:
        - Use short paragraphs or playful tone when suitable.
        - Avoid sounding robotic or overly academic.
        - End with a suitable {model_response} closing line.

        Now, define and explain the topic: **{topic}**.
        """

    response = client.chat.complete(
        model="mistral-large-latest",
        messages=[
            {"role": "system", "content": "You are a creative and humorous teacher who makes explanations enjoyable and accessible. Keep it under 300 tokens."},
            {"role": "user", "content": prompt}
        ],max_tokens=500
    )
    return response.choices[0].message.content

def create_wheel_svg(rotation=0, spinning=False, target_rotation=0):
    """Create an SVG wheel with segments"""
    segments = len(spin_the_wheel)
    angle_per_segment = 360 / segments
    
    svg_parts = ['<svg viewBox="0 0 400 400" style="max-width: 400px; margin: auto; display: block;">']
    
    # Add spinning animation style if spinning
    if spinning:
        svg_parts.append(f'''
            <style>
                @keyframes spin {{
                    from {{ transform: rotate(0deg); }}
                    to {{ transform: rotate({target_rotation}deg); }}
                }}
                .wheel-group {{
                    animation: spin 3s cubic-bezier(0.17, 0.67, 0.12, 0.99);
                    transform-origin: center;
                }}
            </style>
        ''')
    
    # Group for wheel (will be rotated)
    svg_parts.append(f'<g class="wheel-group" transform="rotate({rotation} 200 200)">')
    
    # Draw segments
    for i in range(segments):
        start_angle = i * angle_per_segment - 90
        end_angle = (i + 1) * angle_per_segment - 90
        
        # Convert to radians
        start_rad = math.radians(start_angle)
        end_rad = math.radians(end_angle)
        
        # Calculate arc points
        x1 = 200 + 150 * math.cos(start_rad)
        y1 = 200 + 150 * math.sin(start_rad)
        x2 = 200 + 150 * math.cos(end_rad)
        y2 = 200 + 150 * math.sin(end_rad)
        
        # Create path for segment
        path = f'M 200 200 L {x1} {y1} A 150 150 0 0 1 {x2} {y2} Z'
        svg_parts.append(f'<path d="{path}" fill="{COLORS[i]}" stroke="white" stroke-width="2"/>')
        
        # Add text
        text_angle = start_angle + angle_per_segment / 2
        text_rad = math.radians(text_angle)
        text_x = 200 + 100 * math.cos(text_rad)
        text_y = 200 + 100 * math.sin(text_rad)
        
        # Shorter text labels to prevent overflow
        labels = ["🍳", "💔", "🕵️", "🌸", "👶", "🎭", "💌"]
        
        svg_parts.append(f'''
            <text x="{text_x}" y="{text_y}" 
                  text-anchor="middle" 
                  dominant-baseline="middle"
                  fill="white" 
                  font-size="32" 
                  transform="rotate({text_angle + 90} {text_x} {text_y})">
                {labels[i]}
            </text>
        ''')
    
    svg_parts.append('</g>')
    
    # Center circle
    svg_parts.append('<circle cx="200" cy="200" r="30" fill="white" stroke="#333" stroke-width="3"/>')
    svg_parts.append('<circle cx="200" cy="200" r="15" fill="#333"/>')
    
    # Pointer (arrow at top)
    svg_parts.append('''
        <g transform="translate(200, 20)">
            <path d="M 0 0 L -15 -20 L 15 -20 Z" fill="#FF4444" stroke="#CC0000" stroke-width="2"/>
        </g>
    ''')
    
    svg_parts.append('</svg>')
    
    return ''.join(svg_parts)

# Streamlit App
st.set_page_config(page_title="Spin the Wheel Learning", page_icon="🎡")

st.title("🎡 Spin the Wheel Learning!")
st.write("Enter a topic you want to learn about, spin the wheel, and get a creative explanation!")

# Initialize session state
if 'spun' not in st.session_state:
    st.session_state.spun = False
if 'selected_style' not in st.session_state:
    st.session_state.selected_style = None
if 'response' not in st.session_state:
    st.session_state.response = None
if 'spinning' not in st.session_state:
    st.session_state.spinning = False
if 'final_rotation' not in st.session_state:
    st.session_state.final_rotation = 0
if 'visual_rotation' not in st.session_state:
    st.session_state.visual_rotation = 0
if 'show_result' not in st.session_state:
    st.session_state.show_result = False

# Box 1: User Input
st.subheader("📝 Enter Your Topic")
topic = st.text_input("What do you want to learn about?", placeholder="e.g., quantum physics, black holes, AI...")

# Display the wheel
st.markdown("---")
wheel_container = st.container()

with wheel_container:
    if st.session_state.spinning:
        # Show spinning wheel - animate from 0 to target rotation
        st.markdown(create_wheel_svg(0, spinning=True, target_rotation=st.session_state.final_rotation), unsafe_allow_html=True)
    elif st.session_state.show_result:
        # Show static wheel at the SAME position where animation ended (visual_rotation)
        st.markdown(create_wheel_svg(st.session_state.visual_rotation, spinning=False, target_rotation=0), unsafe_allow_html=True)
    else:
        # Show static wheel at starting position
        st.markdown(create_wheel_svg(0, spinning=False, target_rotation=0), unsafe_allow_html=True)

# Spin the Wheel Button
if topic:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🎰 SPIN THE WHEEL!", use_container_width=True, type="primary", disabled=st.session_state.spinning):
            # Decide random selection FIRST (before spinning)
            selected_index = random.randint(0, len(spin_the_wheel) - 1)
            st.session_state.selected_style = spin_the_wheel[selected_index]
            
            # Calculate final rotation to land on selected segment
            # The pointer is at the top (12 o'clock position)
            angle_per_segment = 360 / len(spin_the_wheel)
            
            # Calculate total rotation: 8 full spins + landing position
            full_rotations = 8 * 360  # 8 full rotations
            # Adjust for the pointer being at top and segments starting at -90 degrees
            target_angle = -(selected_index * angle_per_segment + angle_per_segment / 2) + full_rotations
            
            st.session_state.final_rotation = target_angle
            # Store the visual final position (after animation, this is where it should stay)
            st.session_state.visual_rotation = target_angle
            
            # Generate response BEFORE spinning animation
            with st.spinner("✨ Preparing your model..."):
                st.session_state.response = response_to_user(topic, st.session_state.selected_style)
            
            # Start spinning
            st.session_state.spinning = True
            st.session_state.spun = True
            st.rerun()

# Handle spinning animation completion
if st.session_state.spinning:
    time.sleep(3.2)  # Wait for animation to complete
    st.session_state.spinning = False
    st.session_state.show_result = True
    st.rerun()

# Box 2: Display Results
if st.session_state.spun and st.session_state.selected_style and st.session_state.show_result:
    st.markdown("---")
    st.subheader("🎯 The Wheel Has Spoken!")
    
    # Show selected style in a colored box
    st.info(f"**Style:** {st.session_state.selected_style}")
    
    # Show response
    st.subheader("📖 Your Explanation:")
    st.markdown(st.session_state.response)
    
    # Reset button
    if st.button("🔄 Try Another Topic"):
        st.session_state.spun = False
        st.session_state.selected_style = None
        st.session_state.response = None
        st.session_state.final_rotation = 0
        st.session_state.visual_rotation = 0
        st.session_state.show_result = False
        st.rerun()