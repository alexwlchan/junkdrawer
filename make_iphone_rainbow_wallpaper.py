#!/usr/bin/env python

from PIL import Image, ImageDraw


def create_wallpaper(stripes, background_color="#000000"):
    """
    Create a ``PIL.Image`` instance with the data for thsi wallpaper.
    """
    # The dimensions of an iPhone X wallpaper are 1440 x 2560.
    im = Image.new("RGB", size=(1440, 2560), color=background_color)

    draw = ImageDraw.Draw(im)

    # When measuring the stripes on a JPEG of the iPhone X wallpaper:
    #
    #   - Each stripe was 110 pixels high
    #   - The midpoint of the stripes (between orange/red) on the left-hand
    #     side was 1754 pixels down
    #   - The midpoint of the stripes (between orange/red) on the left-hand
    #     side was 1202 pixels down
    #
    stripe_height = 110
    left_hand_midpoint = 1754
    right_hand_midpoint = 1202

    total_stripe_height = stripe_height * len(stripes)
    left_hand_top = 1754 - (total_stripe_height / 2)
    right_hand_top = 1202 - (total_stripe_height / 2)

    # Each stripe is a parallelogram.
    #
    # The points start in the top left-hand corner, and work clockwise
    # around the shape.
    for i, color in enumerate(stripes):
        draw.polygon(
            [
                (0,    left_hand_top  + stripe_height * i),
                (1440, right_hand_top + stripe_height * i),
                (1440, right_hand_top + stripe_height * (i + 1)),
                (0,    left_hand_top  + stripe_height * (i + 1)),
            ],
            fill=color
        )

    return im


if __name__ == '__main__':
    for name, stripes in [
        ("mystery_1", ["#F996B9", "#FFFFFF", "#CA28E3", "#333333", "#5861CD"]),
        ("mystery_2", ["#D90012", "#D90012", "#0033A0", "#0033A0", "#F2A802", "#F2A802"]),
        ("mystery_3", ["#5BBD60", "#BAD897", "#ffffff", "#BABABA", "#333333"]),
        ("mystery_4", ["#fcd827", "#0423d2", "#0423d2", "#0423d2", "#fcd827"])
    ]:
        im = create_wallpaper(stripes=stripes)
        im.save(f"wallpaper_{name}.jpg")

    for name, stripes in [
        ("rainbow", ["#61BB46", "#FCB829", "#F5801E", "#DE393D", "#943B96", "#049CDC"]),
        ("genderfluid", ["#F996B9", "#FFFFFF", "#CA28E3", "#333333", "#5861CD"]),
        ("pan", ["#F53DA2", "#F53DA2", "#F5DA3D", "#F5DA3D", "#3DBEF5", "#3DBEF5"]),
        ("armenia", ["#D90012", "#D90012", "#0033A0", "#0033A0", "#F2A802", "#F2A802"]),
        ("aro", ["#5BBD60", "#BAD897", "#ffffff", "#BABABA", "#333333"]),
        ("delta", ["#fcd827", "#0423d2", "#0423d2", "#0423d2", "#fcd827"])
    ]:
        im = create_wallpaper(stripes=stripes)
        im.save(f"wallpaper_{name}.jpg")
