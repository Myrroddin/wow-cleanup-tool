"""Generate bug icon for the bug report button."""

from PIL import Image, ImageDraw
from pathlib import Path


# Create a simple bug icon (16x16 and 24x24 for different scales)
def create_bug_icon(size=16, filename="bug.png"):
    """Create a simple bug icon with outline for visibility."""
    # Create transparent image
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Scale for the given size
    scale = size / 16

    # Use a bright color that contrasts on both light and dark backgrounds
    bug_color = (220, 20, 60, 255)  # Crimson red
    outline_color = (255, 255, 255, 255)  # White outline
    outline_width = max(1, int(0.5 * scale))

    # Draw bug body (circle/oval in center) with outline
    body_x = size // 2 - int(3 * scale)
    body_y = size // 2 - int(4 * scale)
    body_w = int(6 * scale)
    body_h = int(8 * scale)

    # Draw body with white outline first, then fill
    draw.ellipse(
        [
            body_x - outline_width,
            body_y - outline_width,
            body_x + body_w + outline_width,
            body_y + body_h + outline_width,
        ],
        fill=outline_color,
    )
    draw.ellipse([body_x, body_y, body_x + body_w, body_y + body_h], fill=bug_color)

    # Draw head (smaller circle at top) with outline
    head_x = size // 2 - int(2 * scale)
    head_y = size // 2 - int(6 * scale)
    head_w = int(4 * scale)

    draw.ellipse(
        [
            head_x - outline_width,
            head_y - outline_width,
            head_x + head_w + outline_width,
            head_y + head_w + outline_width,
        ],
        fill=outline_color,
    )
    draw.ellipse([head_x, head_y, head_x + head_w, head_y + head_w], fill=bug_color)

    # Draw antennae (two lines) with outline effect
    antenna_width = max(1, int(1.5 * scale))

    # Left antenna
    draw.line(
        [
            (head_x + int(1 * scale), head_y - int(1 * scale)),
            (head_x - int(2 * scale), head_y - int(4 * scale)),
        ],
        fill=outline_color,
        width=antenna_width + outline_width,
    )
    draw.line(
        [
            (head_x + int(1 * scale), head_y - int(1 * scale)),
            (head_x - int(2 * scale), head_y - int(4 * scale)),
        ],
        fill=bug_color,
        width=antenna_width,
    )

    # Right antenna
    draw.line(
        [
            (head_x + int(3 * scale), head_y - int(1 * scale)),
            (head_x + int(6 * scale), head_y - int(4 * scale)),
        ],
        fill=outline_color,
        width=antenna_width + outline_width,
    )
    draw.line(
        [
            (head_x + int(3 * scale), head_y - int(1 * scale)),
            (head_x + int(6 * scale), head_y - int(4 * scale)),
        ],
        fill=bug_color,
        width=antenna_width,
    )

    # Draw legs (3 on each side) with outline effect
    leg_width = max(1, int(1.5 * scale))
    for i in range(3):
        y_offset = int((2 + i * 2) * scale)

        # Left legs
        draw.line(
            [
                (body_x - int(2 * scale), body_y + y_offset),
                (body_x - int(5 * scale), body_y + y_offset),
            ],
            fill=outline_color,
            width=leg_width + outline_width,
        )
        draw.line(
            [
                (body_x - int(2 * scale), body_y + y_offset),
                (body_x - int(5 * scale), body_y + y_offset),
            ],
            fill=bug_color,
            width=leg_width,
        )

        # Right legs
        draw.line(
            [
                (body_x + body_w + int(2 * scale), body_y + y_offset),
                (body_x + body_w + int(5 * scale), body_y + y_offset),
            ],
            fill=outline_color,
            width=leg_width + outline_width,
        )
        draw.line(
            [
                (body_x + body_w + int(2 * scale), body_y + y_offset),
                (body_x + body_w + int(5 * scale), body_y + y_offset),
            ],
            fill=bug_color,
            width=leg_width,
        )

    return img


# Create icons in different sizes
icons_dir = Path(__file__).parent / "assets" / "icons"
icons_dir.mkdir(parents=True, exist_ok=True)

# Create 16px icon
img16 = create_bug_icon(16)
img16.save(icons_dir / "bug_16.png")

# Create 24px icon
img24 = create_bug_icon(24)
img24.save(icons_dir / "bug_24.png")

print(f"Bug icons created in {icons_dir}")
