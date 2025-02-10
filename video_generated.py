import cv2
import textwrap


def initialize_video(video_path, output_path, logo_path=None, logo_scale=1.0):
    """
    Initialize video capture and writer, and optionally load a logo.
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise IOError(f"Unable to open video file: {video_path}")

    # Get video properties
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Create a VideoWriter object
    out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height))

    # Load and scale the logo image
    logo = None
    if logo_path:
        logo = cv2.imread(logo_path, cv2.IMREAD_UNCHANGED)
        if logo is None:
            raise IOError(f"Unable to read logo file: {logo_path}")
        new_width = int(logo.shape[1] * logo_scale)
        new_height = int(logo.shape[0] * logo_scale)
        logo = cv2.resize(logo, (new_width, new_height), interpolation=cv2.INTER_AREA)

    return cap, out, logo, fps, frame_width, frame_height


def release_resources(cap, out):
    """
    Release video resources.
    """
    cap.release()
    out.release()
    cv2.destroyAllWindows()


def wrap_text(text, frame_width, font_scale, font_thickness):
    """
    Wrap text to fit within the frame width.
    """
    char_width = cv2.getTextSize("A", cv2.FONT_HERSHEY_SIMPLEX, font_scale, font_thickness)[0][0]
    max_chars_per_line = frame_width // char_width
    return textwrap.wrap(text, width=max_chars_per_line)


def calculate_text_position(wrapped_text, frame_height, font_scale, font_thickness):
    """
    Calculate the starting Y position for the text.
    """
    text_height = cv2.getTextSize("Test", cv2.FONT_HERSHEY_SIMPLEX, font_scale, font_thickness)[0][1]
    line_spacing = 9
    text_block_height = len(wrapped_text) * (text_height + line_spacing) - line_spacing
    return max(frame_height - text_block_height - 20, 20)


def overlay_logo(frame, logo, frame_width, frame_height, margin_left=10, margin_top=50):
    """
    Overlay the logo on the frame.
    """
    if logo is not None:
        logo_height, logo_width = logo.shape[:2]
        x_start, y_start = margin_left, margin_top
        x_end = min(x_start + logo_width, frame_width)
        y_end = min(y_start + logo_height, frame_height)
        roi_width = x_end - x_start
        roi_height = y_end - y_start

        resized_logo = logo[:roi_height, :roi_width]
        roi = frame[y_start:y_end, x_start:x_end]

        if resized_logo.shape[2] == 4:  # Logo with alpha channel
            logo_bgr = resized_logo[:, :, :3]
            alpha_mask = resized_logo[:, :, 3] / 255.0
            for c in range(3):
                roi[:, :, c] = (1 - alpha_mask) * roi[:, :, c] + alpha_mask * logo_bgr[:, :, c]
        else:
            roi[:, :, :] = resized_logo


def add_text(cap, out, text, fps, frame_width, frame_height, font_scale=1, text_color=(255, 255, 255), font_thickness=2, shadow_color=(0, 0, 0), shadow_offset=(2, 2), duration=10):
    """
    Add text with shadow to the bottom center of the video.
    """
    wrapped_text = wrap_text(text, frame_width, font_scale, font_thickness)
    y_start = calculate_text_position(wrapped_text, frame_height, font_scale, font_thickness)
    text_frames = int(duration * fps)
    frame_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        if frame_count <= text_frames:
            y = y_start
            for line in wrapped_text:
                text_size = cv2.getTextSize(line, cv2.FONT_HERSHEY_SIMPLEX, font_scale, font_thickness)[0]
                x = (frame_width - text_size[0]) // 2

                # Draw shadow
                cv2.putText(frame, line, (x + shadow_offset[0], y + shadow_offset[1]), cv2.FONT_HERSHEY_SIMPLEX, font_scale, shadow_color, font_thickness, cv2.LINE_AA)

                # Draw main text
                cv2.putText(frame, line, (x, y), cv2.FONT_HERSHEY_SIMPLEX, font_scale, text_color, font_thickness, cv2.LINE_AA)
                y += text_size[1] + 9

        out.write(frame)
