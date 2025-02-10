import os
import json
import subprocess
import streamlit as st
from get_data import load_data, get_unique_subheaders
from text_generated import get_response_text, get_response_category
from video_generated import add_text
from video_generated import initialize_video
from video_generated import release_resources

# Load config.json
with open("config.json") as config_file:
    config = json.load(config_file)

# Access the API key
api_key = config["api_key"]

def hex_to_bgr(hex_color):
    """
    Convert a hex color code (e.g., #FFFFFF) to a BGR tuple for OpenCV.
    :param hex_color: Hex color code as a string.
    :return: Tuple (B, G, R)
    """
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (4, 2, 0))  # Convert RGB to BGR

# Convert video to compatible format using ffmpeg
def convert_video_to_mp4(input_path, output_path):
    try:
        subprocess.run([
            "ffmpeg", "-y", "-i", input_path, "-vcodec", "libx264", "-acodec", "aac", output_path
        ], check=True)
        return True
    except Exception as e:
        st.error(f"Failed to convert video: {e}")
        return False

# Check video resolution using ffmpeg
def get_video_resolution(video_path):
    try:
        result = subprocess.run([
            "ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
            "stream=width,height", "-of", "csv=p=0", video_path
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        width, height = map(int, result.stdout.decode().strip().split(","))
        return width, height
    except Exception as e:
        st.error(f"Failed to get video resolution: {e}")
        return None, None

# Set up Streamlit UI
st.title("📹 Personalized Video Creator")
st.sidebar.title("⚙️ Configuration")

# Upload Excel File
# st.sidebar.subheader("Step 1: 📄 Upload Excel File")
uploaded_file = './data/data.xlsx'
# api_key = st.sidebar.text_input("🔑 Groq API Key", type="password")

# Step 2: CIF Input as a Number
st.sidebar.subheader("Step 1: 🔢 Enter CIF")
cif_input = st.sidebar.number_input(
    "Enter CIF", min_value=1, step=1, format="%d", help="CIF must be a positive integer"
)

# Step 3: Video Settings
st.sidebar.subheader("Step 2: 🎥 Video Settings")
font_choices = ["Arial", "Times New Roman", "Courier New", "Verdana", "Tahoma"]
selected_font = st.sidebar.selectbox("Select Font", font_choices, index=0)
font_scale = st.sidebar.slider("Font Scale", min_value=0.5, max_value=3.0, value=1.0, step=0.1)
text_color_hex = st.sidebar.color_picker("Text Color", value="#FFFFFF")
font_thickness = st.sidebar.slider("Font Thickness", min_value=1, max_value=5, value=2)
shadow_color_hex = st.sidebar.color_picker("Shadow Color", value="#000000")
shadow_offset_x = st.sidebar.slider("Shadow Offset X", min_value=-10, max_value=10, value=2)
shadow_offset_y = st.sidebar.slider("Shadow Offset Y", min_value=-10, max_value=10, value=2)
text_duration = st.sidebar.slider("Text Duration (seconds)", min_value=1, max_value=30, value=10)


if st.sidebar.button("Generate Video"):
    if not (uploaded_file and api_key and cif_input): 
        st.error("Please provide all required inputs!")
    else:
        try:
            # Convert hex colors to BGR
            text_color = hex_to_bgr(text_color_hex)
            shadow_color = hex_to_bgr(shadow_color_hex)

            # Step 1: Process Excel Data
            st.markdown(
                """
                <div style="padding: 10px; background-color: #f9f9f9; border-radius: 5px; border: 1px solid #ddd;">
                    <strong>Processing Excel data...</strong>
                </div>
                """,
                unsafe_allow_html=True
            )
            data_processor = load_data(uploaded_file)
            subheader_values = get_unique_subheaders(data_processor, cif_input)  # Convert CIF to string if needed
            if not subheader_values:
                st.error("No matching data found for the given CIF.")
                st.stop()

            st.markdown(
                f"""
                <div style="padding: 10px; background-color: #f9f9f9; border-radius: 5px; border: 1px solid #ddd;">
                    <strong>Found {len(subheader_values)} transaction patterns.</strong>
                </div>
                """,
                unsafe_allow_html=True
            )

            # Step 2: Generate Text with Groq
            st.markdown(
                """
                <div style="padding: 10px; background-color: #f9f9f9; border-radius: 5px; border: 1px solid #ddd;">
                    <strong>Generating text with Groq...</strong>
                </div>
                """,
                unsafe_allow_html=True
            )
            generated_text = get_response_text(subheader_values)

            category = get_response_category(generated_text)
            st.write('Category:', category)

            if category == 'makanan & minuman':
                video_path = './tamplate_video/video_template_mnm.mp4'
            elif category == 'belanja':
                video_path = './tamplate_video/video_template_belanja.mp4'
            elif category == 'hiburan':
                video_path = './tamplate_video/video_template_hiburan.mp4'
            else:
                video_path = './tamplate_video/video_template_hiburan.mp4'

            # Display generated text in a styled bubble
            st.markdown(
                f"""
                <div style="padding: 10px; background-color: #f0f8ff; border-radius: 10px; border: 1px solid #cce7ff;">
                    <h4 style="color: #007acc;">Generated Text:</h4>
                    <p style="font-size: 16px; font-family: {selected_font}; color: #333;">{generated_text}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

            # Step 3: Check Video Resolution
            st.markdown(
                """
                <div style="padding: 10px; background-color: #f9f9f9; border-radius: 5px; border: 1px solid #ddd;">
                    <strong>Checking video resolution...</strong>
                </div>
                """,
                unsafe_allow_html=True
            )
            width, height = get_video_resolution(video_path)
            if width and height:
                st.markdown(
                    f"""
                    <div style="padding: 10px; background-color: #f9f9f9; border-radius: 5px; border: 1px solid #ddd;">
                        <strong>Video resolution: {width}x{height}</strong>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                if width < height:
                    st.warning("The video is vertical. Adjusting text position for vertical layout.")

            # Step 4: Create Video with Text
            st.markdown(
                """
                <div style="padding: 10px; background-color: #f9f9f9; border-radius: 5px; border: 1px solid #ddd;">
                    <strong>Creating video with overlay text...</strong>
                </div>
                """,
                unsafe_allow_html=True
            )
            output_path = f"./output_video_{cif_input}.mp4"  # Use CIF to name the output file
            st.write(f"Output path: {os.path.abspath(output_path)}")
            position = (width // 2, height // 4) if width and height and width < height else (100, 100)
            
            cap, out, logo, fps, frame_width, frame_height = initialize_video(video_path, output_path)

            # Now call add_text with the correct parameters
            add_text(
                cap=cap, 
                out=out, 
                text=generated_text, 
                fps=fps, 
                frame_width=frame_width, 
                frame_height=frame_height, 
                font_scale=font_scale, 
                text_color=text_color, 
                font_thickness=font_thickness, 
                shadow_color=shadow_color, 
                shadow_offset=(shadow_offset_x, shadow_offset_y), 
                duration=text_duration
            )

            # After the video generation, release resources
            release_resources(cap, out)

            # Save video and verify
            if os.path.exists(output_path):
                file_size = os.path.getsize(output_path)
                st.markdown(
                    f"""
                    <div style="padding: 10px; background-color: #dff0d8; border-radius: 5px; border: 1px solid #d6e9c6;">
                        <strong>Video file created successfully. File size: {file_size / (1024 * 1024):.2f} MB</strong>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                # Convert video if necessary, it's really necessary fr
                converted_path = f"./converted_video_{cif_input}.mp4"
                if convert_video_to_mp4(output_path, converted_path):
                    st.video(data=converted_path, format="video/mp4", start_time=0)

                    # Provide download link
                    with open(converted_path, "rb") as video_file:
                        st.download_button(
                            label="📥 Download Video",
                            data=video_file,
                            file_name=f"converted_video_{cif_input}.mp4",
                            mime="video/mp4",
                            help="Click to download your video."
                        )
                else:
                    st.error("Failed to convert video to a compatible format.")
            else:
                st.error("The video file was not found after saving. Please check the video generation logic.")

        except Exception as e:
            st.error(f"An error occurred: {e}")