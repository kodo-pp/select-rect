#!/usr/bin/env python
from argparse import ArgumentParser

import pygame as pg


def parse_args():
    ap = ArgumentParser()
    ap.add_argument('image', type=str, help='Image filename')
    return ap.parse_args()


def get_rect(a, b):
    x1, y1 = a
    x2, y2 = b
    left = min(x1, x2)
    top = min(y1, y2)
    right = max(x1, x2)
    bottom = max(y1, y2)
    width = right - left
    height = bottom - top
    return pg.Rect(left, top, width, height)


def print_rect(initial_position, final_position, offset):
    x, y = offset
    rect = get_rect(initial_position, final_position)
    print('[{}, {}, {}, {}]'.format(rect.left - x, rect.top - y, rect.width, rect.height))


def main():
    print('=== Loading, please wait... ===')
    print('Notice: large images may take a while to be processed')
    args = parse_args()

    pg.init()
    image = pg.image.load(args.image)
    image = image.convert(24, pg.HWSURFACE)
    max_width = 1600
    max_height = 800
    image_width, image_height = image.get_size()
    window_size = (min(image_width, max_width), min(image_height, max_height))
    pg.display.set_mode(window_size, pg.DOUBLEBUF | pg.HWSURFACE)
    screen = pg.display.get_surface()

    should_redraw = True
    initial_position = None
    current_position = None
    offset_x = 0
    offset_y = 0
    while True:
        if should_redraw:
            screen.fill((0, 0, 0))
            screen.blit(image, pg.Rect(offset_x, offset_y, image_width, image_height))
            if initial_position is not None:
                rect = get_rect(current_position, initial_position)
                pg.draw.rect(screen, (255, 255, 255), rect, 2)
                pg.draw.rect(screen, (0, 0, 0), rect, 1)
            pg.display.flip()
        should_redraw = False
        event = pg.event.wait()
        if event.type == pg.QUIT:
            break
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            initial_position = event.pos
            current_position = event.pos
            should_redraw = True
        elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
            final_position = event.pos
            print_rect(initial_position, final_position, (offset_x, offset_y))
            break
        elif event.type == pg.MOUSEMOTION:
            if initial_position is not None:
                current_position = event.pos
                should_redraw = True
        elif event.type == pg.KEYDOWN:
            should_redraw = True
            if event.key == pg.K_UP:
                offset_y += 40
            if event.key == pg.K_DOWN:
                offset_y -= 40
            if event.key == pg.K_LEFT:
                offset_x += 40
            if event.key == pg.K_RIGHT:
                offset_x -= 40


if __name__ == '__main__':
    main()
