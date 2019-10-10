import pygame


class LineFontChunk:
    def __init__(self, text, font):
        self.text = text
        self.font = font

    def __repr__(self):
        return "[" + str(self.text) + ", " + str(self.font) + "]"


def lerp(a, b, c):
    return (c * b) + ((1.0 - c) * a)


def render_adventure_text(screen, adventure_output, entered_keys, font, bold_font,
                          italic_font, header_font, active_scene, player, time_delta):
    text_printing_finished = False
    text_lines = adventure_output.split('\n')
    line_num = 0
    current_screen_y_pos = 40

    text_colour = pygame.Color("#000000")
    text_colour.r = active_scene.text_colour.r
    text_colour.g = active_scene.text_colour.g
    text_colour.b = active_scene.text_colour.b

    if active_scene.is_first_visit:
        if active_scene.type_print_per_letter_timer_acc < active_scene.type_print_per_letter_time:
            active_scene.type_print_per_letter_timer_acc += time_delta
        else:
            active_scene.type_print_per_letter_timer_acc = 0.0
            active_scene.type_letter_progress += 1
    else:
        if active_scene.fade_timer_acc < active_scene.fade_time:
            active_scene.fade_timer_acc += time_delta
            fade_value = active_scene.fade_timer_acc / active_scene.fade_time
            if fade_value > 1.0:
                fade_value = 1.0

            text_colour.r = int(lerp(float(active_scene.background_colour.r),
                                     float(active_scene.text_colour.r), fade_value))
            text_colour.g = int(lerp(float(active_scene.background_colour.g),
                                     float(active_scene.text_colour.g), fade_value))
            text_colour.b = int(lerp(float(active_scene.background_colour.b),
                                     float(active_scene.text_colour.b), fade_value))

        else:
            text_colour = active_scene.text_colour
            active_scene.type_letter_progress = len(active_scene.get_description(player))

    line_len_acc = 0
    # current_bold_state = False
    while not text_printing_finished:
        current_screen_y_pos = 40 + line_num * 22
        text_line = text_lines[line_num]

        if font.size(text_line)[0] >= 500:
            line_words = text_line.split(' ')
            line_length = 0
            word_num = 0
            found_word_wrap_point = False
            for word in line_words:
                line_length += font.size(word)[0]
                if line_length >= 500 and not found_word_wrap_point:
                    found_word_wrap_point = True
                    text_line = ""
                    for wordIndex in range(0, word_num):
                        text_line += line_words[wordIndex] + " "

                    next_text_line = ""
                    for new_line_word_index in range(word_num, len(line_words)):
                        next_text_line += line_words[new_line_word_index] + " "
                    text_lines.insert(line_num+1, next_text_line)
                word_num += 1

        line_end = 0
        # these are chunks of text per line where we switch between fonts
        # e.g. if we are rendering bold text
        line_font_chunks = [LineFontChunk(text_line, font)]

        # process line into chunks
        for chunk in line_font_chunks:
            bold_start_index = chunk.text.find("[b]")
            if bold_start_index != -1:
                line_font_chunks.append(LineFontChunk(chunk.text[:bold_start_index], font))
                line_font_chunks.append(LineFontChunk(chunk.text[bold_start_index+3:], bold_font))
                line_font_chunks.remove(chunk)

        for chunk in line_font_chunks:
            bold_end_index = chunk.text.find("[/b]")
            if bold_end_index != -1:
                line_font_chunks.append(LineFontChunk(chunk.text[:bold_end_index], bold_font))
                line_font_chunks.append(LineFontChunk(chunk.text[bold_end_index+4:], font))
                line_font_chunks.remove(chunk)

        for chunk in line_font_chunks:
            header_start_index = chunk.text.find("[h]")
            if header_start_index != -1:
                line_font_chunks.append(LineFontChunk(chunk.text[:header_start_index], font))
                line_font_chunks.append(LineFontChunk(chunk.text[header_start_index+3:], header_font))
                line_font_chunks.remove(chunk)

        for chunk in line_font_chunks:
            header_end_index = chunk.text.find("[/h]")
            if header_end_index != -1:
                line_font_chunks.append(LineFontChunk(chunk.text[:header_end_index], header_font))
                line_font_chunks.append(LineFontChunk(chunk.text[header_end_index+4:], font))
                line_font_chunks.remove(chunk)

        for chunk in line_font_chunks:
            italic_start_index = chunk.text.find("[i]")
            if italic_start_index != -1:
                line_font_chunks.append(LineFontChunk(chunk.text[:italic_start_index], font))
                line_font_chunks.append(LineFontChunk(chunk.text[italic_start_index+3:], italic_font))
                line_font_chunks.remove(chunk)

        for chunk in line_font_chunks:
            italic_end_index = chunk.text.find("[/i]")
            if italic_end_index != -1:
                line_font_chunks.append(LineFontChunk(chunk.text[:italic_end_index], italic_font))
                line_font_chunks.append(LineFontChunk(chunk.text[italic_end_index+4:], font))
                line_font_chunks.remove(chunk)

        # draw chunks
        chunk_x_pos = 40
        chunk_line_pos = 0
        for chunk in line_font_chunks:
            if active_scene.is_first_visit:
                if active_scene.type_letter_progress >= line_len_acc:
                    line_end = active_scene.type_letter_progress - line_len_acc - chunk_line_pos
                    if line_end > len(chunk.text):
                        line_end = len(chunk.text)
                    if line_end < 0:
                        line_end = 0

                adventure_output_text_render = chunk.font.render(chunk.text[:line_end], True, text_colour)
                adventure_output_text_rect = adventure_output_text_render.get_rect(x=chunk_x_pos,
                                                                                   y=current_screen_y_pos)
                screen.blit(adventure_output_text_render, adventure_output_text_rect)
                chunk_x_pos += chunk.font.size(chunk.text[:line_end])[0]
            else:
                if active_scene.type_letter_progress < len(adventure_output):
                    if active_scene.type_letter_progress >= line_len_acc:
                        line_end = active_scene.type_letter_progress - line_len_acc
                        if line_end > len(chunk.text):
                            line_end = len(chunk.text)

                        length = font.size(text_line[:line_end])[0]
                        adventure_output_text_render = chunk.font.render(chunk.text[:line_end],
                                                                         True, active_scene.text_colour)
                        adventure_output_text_rect = adventure_output_text_render.get_rect(x=chunk_x_pos,
                                                                                           y=current_screen_y_pos)

                        adventure_output2_text_render = chunk.font.render(chunk.text[line_end:], True, text_colour)
                        adventure_output2_text_rect = adventure_output2_text_render.get_rect(x=chunk_x_pos + length,
                                                                                             y=current_screen_y_pos)

                        screen.blit(adventure_output_text_render, adventure_output_text_rect)
                        screen.blit(adventure_output2_text_render, adventure_output2_text_rect)

                    chunk_x_pos += chunk.font.size(chunk.text)[0]
                else:
                    adventure_output_text_render = chunk.font.render(chunk.text, True, text_colour)
                    adventure_output_text_rect = adventure_output_text_render.get_rect(x=chunk_x_pos,
                                                                                       y=current_screen_y_pos)
                    screen.blit(adventure_output_text_render, adventure_output_text_rect)
                    chunk_x_pos += chunk.font.size(chunk.text)[0]
            chunk_line_pos += len(chunk.text)

        line_num += 1
        line_len_acc += len(text_line)
        if line_num == len(text_lines):
            text_printing_finished = True

    current_screen_y_pos += 20
    
    player_input = "> " + entered_keys
    adventure_output_text_render = bold_font.render(player_input, True, active_scene.player_text_colour)
    adventure_output_text_rect = adventure_output_text_render.get_rect(x=40, y=current_screen_y_pos)
    screen.blit(adventure_output_text_render, adventure_output_text_rect)
