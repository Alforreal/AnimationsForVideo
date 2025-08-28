import time
from manim import *
import numpy as np

fraction_offset = 0.05
transition_scene_4_5 = VGroup()
SCREEN_HEIGHT = 1080
SCREEN_WIDTH = 1920
MUNIT_WIDTH = 14.22
MUNIT_HEIGHT = 8

def get_len(mobject):
            return (mobject.get_right()[0] - mobject.get_left()[0])

def pixels_to_munits(input):
    return input / SCREEN_HEIGHT * MUNIT_HEIGHT

def get_height(mobject):
            return (mobject.get_top()[1] - mobject.get_bottom()[1])

class Introduction(MovingCameraScene):
    def construct(self):

        circle = Circle(radius=3, stroke_width=3, color=WHITE)
        self.play(Create(circle), run_time=2)
        self.wait(2)

        self.play(self.camera.frame.animate.move_to(circle.point_at_angle(3 * np.pi / 4)).scale(0.01), run_time=2)
        self.wait(2)

class FirstScene(Scene):

    def construct(self):

        #creating box
        plane = NumberPlane(x_range=(0, 5, 1), y_range=(0, 3, 1))
        upper_line = Line(start=plane.c2p(0, 3), end=plane.c2p(5, 3), stroke_width= 2, color=WHITE)
        right_line = Line(start=plane.c2p(5, 3), end=plane.c2p(5,0), stroke_width= 2, color=WHITE)
        box = VGroup(plane, upper_line, right_line)
        box.set_z_index(1)

        #Initial Line

        d1_coord = [0, 0, 0]
        d2_coord = [5, 3, 0]

        d1 = Dot(plane.c2p(d1_coord[0], d1_coord[1]), radius= 0.05, color=GREEN)
        d2 = Dot(plane.c2p(d2_coord[0], d2_coord[1]), radius= 0.05, color=GREEN)

        d1_text = Text("D1", font_size=21).next_to(d1, DOWN)
        d2_text = Text("D2", font_size=21).next_to(d2, UP)

        d1d2_line= Line(start=d1.get_center(), end=d2.get_center(), color=WHITE)
        line_stuff = VGroup(d1, d2, d1_text, d2_text)

        d1d2_line.set_z_index(3)
        line_stuff.set_z_index(5)




        #Calculate arrows (уже не рекурсивно, но все же)

        start = time.perf_counter_ns()
        arrows = self.algorithm(d1_coord, d2_coord, plane)
        end = time.perf_counter_ns()
        print(f"Time taken: {(end - start) / 1e6} ns")
        arrows.set_z_index(4)


        #Animation


        self.play(Create(d1), Create(d2), run_time=2)
        self.play(Write(d1_text), Write(d2_text), run_time=1)
        self.wait(2)
        self.play(Create(d1d2_line), run_time=2)
        self.wait(3)




        self.play(Create(box), run_time=4)
        self.wait(2)

        for arrow in arrows:
            self.play(Create(arrow), run_time=0.5)

        self.wait(3)

        for arrow in reversed(arrows):
            self.play(FadeOut(arrow), run_time=0.3)

        self.play(Uncreate(d1), Uncreate(d2), Uncreate(d1_text), Uncreate(d2_text), Uncreate(d1d2_line), run_time=2)
        self.wait(1)

        self.play(Uncreate(box),  run_time=2)







    def algorithm(self, d1_loc, d2_loc, plane):
        arrows_group = VGroup()
        deltaA = d2_loc[0] - d1_loc[0]
        deltaB = d2_loc[1] - d1_loc[1]
        Nabla = 2*deltaB - deltaA
        arrow_start = d1_loc

        while(arrow_start[0] < d2_loc[0]):

            if(Nabla >= 0):
                arrow_end = [arrow_start[0]+1, arrow_start[1]+1, 0]
                Nabla = Nabla + 2*deltaB - 2*deltaA
            else:
                arrow_end = [arrow_start[0]+1, arrow_start[1], 0]
                Nabla = Nabla + 2*deltaB

            arrows_group += Arrow(start=plane.c2p(*arrow_start), end=plane.c2p(*arrow_end), color=ManimColor('#FF0000'), buff=0.0, stroke_width=2, tip_length = 0.2)
            arrow_start = arrow_end

        return arrows_group



class SecondScene(MovingCameraScene):
        def construct(self):


            #Objects
            # Zoomed Camera
            self.camera.frame.scale(0.4)


            #Box
            plane = NumberPlane(x_range=(0, 5, 1), y_range=(0, 4, 1))
            upper_line = Line(start=plane.c2p(0, 4), end=plane.c2p(5, 4), stroke_width= 2, color=WHITE)
            right_line = Line(start=plane.c2p(5, 4), end=plane.c2p(5,0), stroke_width= 2, color=WHITE)
            box = VGroup(plane, upper_line, right_line)
            box.set_z_index(1)

            #Square
            square = Square(color = BLUE, side_length= 1, stroke_width = 1.7)
            square.move_to(plane.c2p(0.5, 0.5))
            square.set_z_index(1)

            #Dot
            dot = Dot(plane.c2p(0, 0), radius= 0.05, color=GREEN)
            dot.set_z_index(3)

            #Arrows
            arrow_1mm = Arrow(start=plane.c2p(0, 0), end=plane.c2p(1, 0), color=ManimColor("#39E70E"), buff=0.0, stroke_width=2, tip_length = 0.1)
            arrow_2mm = Arrow(start=plane.c2p(0, 0), end=plane.c2p(1, 1), color=ManimColor("#39E70E"), buff=0.0, stroke_width=2, tip_length = 0.1)
            arrow_1mm.set_z_index(2)
            arrow_2mm.set_z_index(2)

            #Text
            text_1mm = Tex("1 mm", font_size=15)
            text_2mm = Tex(r"$\sqrt{2}$ mm", font_size=15)
            text_1mm.move_to(arrow_1mm.get_bottom() + UP * 0.15)
            text_2mm.move_to(arrow_2mm.get_center() + UP * 0.14 + LEFT * 0.13)
            text_2mm.rotate(PI/4)
            text_2mm_approx = Tex(r"$\approx$ 1.41 mm", font_size=17)
            text_2mm_approx.move_to(arrow_2mm.get_center() + UP * 0.14 + LEFT * 0.13)
            text_2mm_approx.rotate(PI/4)

            all_text_in_sqare = VGroup(text_1mm, text_2mm, text_2mm_approx)
            all_text_in_sqare.set_z_index(2)

            all_arrows_in_square = VGroup(arrow_1mm, arrow_2mm)
            all_arrows_in_square.set_z_index(2)


            #Move Camera
            self.camera.frame.move_to(square)
            self.wait(2)

            #D1D2
            d1_coord = [0, 0, 0]
            d2_coord = [5, 4, 0]
            d1 = Dot(plane.c2p(d1_coord[0], d1_coord[1]), radius= 0.05, color=GREEN) #По сути лишний код, у нас уже есть эта точка, но в коде выглядит логичнее так

            d2 = Dot(plane.c2p(d2_coord[0], d2_coord[1]), radius= 0.05, color=GREEN)
            d2_after_traverse = d2.copy()
            d1_name = Tex(r"$\boldsymbol{D_1}$", font_size=21).next_to(d1, DOWN * 0.7)
            d2_name = Tex(r"$\boldsymbol{D_2}$", font_size=21).next_to(d2, UP * 0.5)

            x1y1_text = Tex(r"$\boldsymbol{(x_1, y_1)}$", font_size=21)
            x2y2_text = Tex(r"$\boldsymbol{(x_2, y_2)}$", font_size=21)


            d1d2_line = always_redraw(lambda:
                Line(d1.get_center(), d2_after_traverse.get_center(), color=WHITE)
            )

            d1d2_dots = VGroup(d1, d2, d2_after_traverse)
            d1d2_names = VGroup(d1_name, d2_name)

            xy_group = VGroup(x1y1_text, x2y2_text)

            d1d2_line.set_z_index(3)
            d1d2_dots.set_z_index(4)
            d1d2_names.set_z_index(3)

            xy_group.set_z_index(3)

            #Arrows_on_sides
            arrow_b = Arrow(start = plane.c2p(0, 2.2), end = plane.c2p(0, 2.7), color=ManimColor("#00A2FF"), buff=0.0, stroke_width=1, tip_length = 0.1)
            b_name = Text("b", font_size=14).next_to(arrow_b, LEFT * 0.1)

            b_group = VGroup(arrow_b, b_name)
            b_group.set_z_index(2)
            b_group.shift(LEFT * 0.2).set_opacity(0.8)

            arrow_a = Arrow(start = plane.c2p(4.2, 0), end = plane.c2p(4.7, 0), color=ManimColor("#00A2FF"), buff=0.0, stroke_width=1, tip_length = 0.1)
            a_name = Text("a", font_size=14).next_to(arrow_a, DOWN * 0.1)

            a_group = VGroup(arrow_a, a_name)
            a_group.set_z_index(2)
            a_group.shift(DOWN * 0.2).set_opacity(0.8)

            #Change_of_coordinates
            d1_new_coord_text = Tex(r"$\boldsymbol{(0, 0)}$", font_size=17)                         # .next_to(d1_text, RIGHT * 0.5)
            d2_new_coord_text1 = Tex(r"$\boldsymbol{(x_2-x_1$, $y_2-y_1)}$", font_size=17)           # .next_to(d2_text, RIGHT * 0.5)
            d2_new_coord_text2 = Tex(r"$\boldsymbol{(\Delta a, \Delta b)}$", font_size=17)          # .next_to(d2_text, RIGHT * 0.5)

            #b_equation
            b_equation_1 = Tex(r"$\boldsymbol{b = ma}$", font_size=21)
            b_equation_2 = Tex(r"$\boldsymbol{m = \frac{\Delta b}{\Delta a}}$", font_size=21)
            b_equation_1.next_to(plane.c2p(2.5, 0), DOWN * 1.5)
            b_equation_2.next_to(b_equation_1.get_bottom(), DOWN * 0.7)

            #Grid_Numbers
            grid_diag_numbers = VGroup()
            grid_vertical_numbers = VGroup()
            for i in range(1, 6):
                grid_diag_numbers.add(Text(str(i), font_size=12).next_to(plane.c2p(i, 0), DOWN * 0.17))

            for i in range(1, 5):
                grid_vertical_numbers.add(Text(str(i), font_size=12).next_to(plane.c2p(0, i), LEFT * 0.17))

            #D2_Traverse
            d2_newpos_name = Tex(r"$\boldsymbol{D_2}$", font_size=21).move_to(plane.c2p(3.2, 2.2))
            d2_new_coord_names = Tex(r"$\boldsymbol{(\Delta a, \Delta b)}$", font_size=17).next_to(d2_newpos_name, RIGHT * 0.5)
            d2_traverse_group = VGroup(d2, d2_newpos_name, d2_new_coord_names)
            d2_traverse_group.set_z_index(4)

            dashed_horizontal_line = DashedLine(start=plane.c2p(3, 0), end=plane.c2p(3, 2), color=WHITE, dash_length=0.1, dashed_ratio=0.5)
            dashed_vertical_line = DashedLine(start=plane.c2p(0, 2), end=plane.c2p(3, 2), color=WHITE, dash_length=0.1, dashed_ratio=0.5)

            dashed_lines = VGroup(dashed_horizontal_line, dashed_vertical_line)
            dashed_lines.set_z_index(3)

            #Undoing_Whats_Done
            d2_original = d2.copy()
            d2_original_name = d2_name.copy()
            d2_original_delta_coord = d2_new_coord_text2.copy().next_to(d2_original_name, RIGHT * 0.5)
            d1d2_original_line = d1d2_line.copy()
            undoing_group = VGroup(d2_original, d2_original_name, d2_original_delta_coord)
            d1d2_original_line.set_z_index(3)
            d1d2_original_line.add_updater(lambda line: line.put_start_and_end_on(d1.get_center(), d2_after_traverse.get_center()))
            undoing_group.set_z_index(4)

            #                                                                  Third Scene                                                                                    #



            # P point
            p_dot = Dot(plane.c2p(1, 1), radius= 0.04, color=GREEN)
            p_name = Tex(r"$\boldsymbol{P}$", font_size = 11).move_to(plane.c2p(0.9, 1.1))

            p_stuff = VGroup(p_dot, p_name)
            p_stuff.set_z_index(4)

            # R point
            r_dot = Dot(plane.c2p(2, 1), radius= 0.04, color=GREEN)
            r_name = Tex(r"$\boldsymbol{R}$", font_size = 11).move_to(plane.c2p(2.1, 0.9))

            r_stuff = VGroup(r_dot, r_name)
            r_stuff.set_z_index(4)

            # Q point
            q_dot = Dot(plane.c2p(2, 2), radius= 0.04, color=GREEN)
            q_name = Tex(r"$\boldsymbol{Q}$", font_size = 11).move_to(plane.c2p(2.1, 2.1))


            q_stuff = VGroup(q_dot, q_name)
            q_stuff.set_z_index(4)


            # S point

            start = d1d2_line.get_start()
            end = d1d2_line.get_end()

            x = 2

            t = (x - plane.p2c(start)[0]) / (plane.p2c(end)[0] - plane.p2c(start)[0])
            y = (1 - t) * plane.p2c(start)[1] + t * plane.p2c(end)[1]

            s_dot = Dot(plane.c2p(x, y), radius= 0.04, color=GREEN)

            s_dot.add_updater(lambda dot: dot.move_to(
                plane.c2p(x, self.interpolate_y_on_line(d1d2_line, x, plane))
            ))

            s_name = Tex(r"$\boldsymbol{S}$", font_size = 11)
            s_name.add_updater(lambda s: s.next_to(s_dot, RIGHT, buff = 0.05))

            static_s_name = Tex(r"$\boldsymbol{S}$", font_size = 11).next_to(s_dot, RIGHT, buff = 0.05)

            s_stuff = VGroup(s_dot, s_name)
            s_stuff.set_z_index(4)

            # Arrow to P
            p_arrow = Arrow(
                start=plane.c2p(0, 0),
                end=p_dot.get_center(),
                color=ManimColor('#FF0000'),
                buff=0.025,
                stroke_width=2,
                tip_length=0.1,
            )
            p_arrow.set_z_index(3)

            # R or Q?
            line_to_r = DashedLine(start = p_dot.get_center(), end = r_dot.get_center(), color = WHITE, dash_length = 0.1, dashed_ratio = 0.5, stroke_width = 1)
            line_to_q = DashedLine(start = p_dot.get_center(), end = q_dot.get_center(), color = WHITE, dash_length = 0.1, dashed_ratio = 0.5, stroke_width = 1)
            dashed_rq = VGroup(line_to_q, line_to_r)
            dashed_rq.set_z_index(3)

            #Triangles

            # projection_point_r = d1d2_line.get_projection(r_dot.get_center())
            # projection_point_q = d1d2_line.get_projection(q_dot.get_center())

            static_projection_r = Line(start = r_dot.get_center(), end = d1d2_line.get_projection(r_dot.get_center()), color = ORANGE, stroke_width = 1)
            projection_r = always_redraw(lambda: Line(start = r_dot.get_center(), end = d1d2_line.get_projection(r_dot.get_center()), color = ORANGE, stroke_width = 1))

            # projection_r.add_updater(lambda line: line.put_start_and_end_on(
            #     r_dot.get_center(), d1d2_line.get_projection(r_dot.get_center())
            # ))

            static_projection_q = Line(start = q_dot.get_center(), end = d1d2_line.get_projection(q_dot.get_center()), color = ORANGE, stroke_width = 1)
            projection_q = always_redraw(lambda: Line(start = q_dot.get_center(), end = d1d2_line.get_projection(q_dot.get_center()), color = ORANGE, stroke_width = 1))
            # projection_q.add_updater(lambda line: line.put_start_and_end_on(
            #     q_dot.get_center(), d1d2_line.get_projection(q_dot.get_center())
            # ))

            static_little_r_name = Tex(r"$\boldsymbol{r}$", font_size = 10).next_to(static_projection_r.get_center(), DOWN+LEFT, buff=0.01 )
            static_little_q_name = Tex(r"$\boldsymbol{q}$", font_size = 10).next_to(static_projection_q.get_center(), UP+RIGHT, buff=0.01 )

            little_r_name = Tex(r"$\boldsymbol{r}$", font_size = 10).next_to(projection_r.get_center(), DOWN+LEFT, buff=0.01 )
            little_r_name.add_updater(lambda name: name.next_to(projection_r.get_center(), DOWN+LEFT, buff=0.01 ))

            little_q_name = Tex(r"$\boldsymbol{q}$", font_size = 10).next_to(projection_q.get_center(), UP+RIGHT, buff=0.01 )
            little_q_name.add_updater(lambda name: name.next_to(projection_q.get_center(), UP+RIGHT, buff=0.01 ))

            # r_part_from_original = Line(start = projection_point_r, end = s_dot.get_center(), color = ORANGE)
            # q_part_from_original = Line(start = projection_point_q, end = s_dot.get_center(), color = ORANGE)
            # parts = VGroup(r_part_from_original, q_part_from_original, line_QR)
            # parts.set_z_index(3)

            static_projections = VGroup(static_projection_r, static_projection_q)
            static_projections.set_z_index(2)

            projections = VGroup(projection_r, projection_q)
            projections.set_z_index(2)

            static_right_angle_r = RightAngle(
                d1d2_line,
                projection_r,
                length=0.07,
                stroke_width = 1,
                quadrant=(1, -1),
                color=ORANGE
            )

            right_angle_r = always_redraw(lambda: RightAngle(
                d1d2_line,
                projection_r,
                length=0.07,
                stroke_width = 1,
                quadrant=(1, -1),
                color=ORANGE
            ))

            static_right_angle_q = RightAngle(
                d1d2_line,
                projection_q,
                length=0.07,
                stroke_width = 1,
                quadrant=(-1, -1),
                color=ORANGE
            )

            right_angle_q = always_redraw(lambda: RightAngle(
                d1d2_line,
                projection_q,
                length=0.07,
                stroke_width = 1,
                quadrant=(-1, -1),
                color=ORANGE
            ))


            #Calculate projection values
            #r:
            r_label = Tex(r"\textbf{r = }", font_size=11)
            r_value = DecimalNumber(0, num_decimal_places=2, font_size=11)

            r_len_text = VGroup(r_label, r_value).arrange(RIGHT, buff=0.05)
            r_len_text.move_to(plane.c2p(3.5, 1.85), aligned_edge=RIGHT)

            r_value.add_updater(lambda r: r.set_value(projection_r.get_length()))
            r_value.add_updater(lambda r2: r2.set_z_index(4))

            #q:
            q_label = Tex(r"\textbf{q = }", font_size=11)
            q_value = DecimalNumber(0, num_decimal_places=2, font_size=11)

            q_len_text = VGroup(q_label, q_value).arrange(RIGHT, buff=0.05)
            q_len_text.next_to(r_len_text, DOWN, buff = 0.05)

            q_value.add_updater(lambda q: q.set_value(projection_q.get_length()))
            q_value.add_updater(lambda q2: q2.set_z_index(4))

            #r-q:
            rq_difference_label = Tex(r"\textbf{r - q}", font_size=11)
            rq_difference_equals = Tex(r"\textbf{=}", font_size=11)
            rq_difference_value = DecimalNumber(0, num_decimal_places=2, font_size=11)
            rq_difference_nabla = Tex(r"$\boldsymbol{\nabla}$", font_size=11)

            # Nabla = r-q:
            rq_nabla_coords = plane.c2p(0.65, 3)
            rq_nabla_temp_group = VGroup(rq_difference_nabla, rq_difference_equals, rq_difference_label)

            rq_nabla_expression = Tex(r"$\boxed{\boldsymbol{\nabla=}\textbf{r - q}}$", font_size=11) # Used for a precise box
            rq_nabla_expression.set_z_index(2)
            rq_nabla_rectangle = Rectangle(                                                          # Used for background
                width=rq_nabla_expression.get_right()[0]-rq_nabla_expression.get_left()[0] - 0.01,
                height=rq_nabla_expression.get_top()[1]-rq_nabla_expression.get_bottom()[1] - 0.01,
                fill_opacity=1.0,
                fill_color=BLACK,
                stroke_opacity=0.0
            )
            rq_nabla_rectangle.set_z_index(3)
            rq_nabla_rectangle_group = VGroup(rq_nabla_expression, rq_nabla_rectangle)
            rq_nabla_rectangle_group.move_to(rq_nabla_coords)

            rq_nabla_group = VGroup(rq_nabla_temp_group, rq_nabla_rectangle_group)

            # Setting up r-q=... :
            rq_difference_text = VGroup(rq_difference_label, rq_difference_equals, rq_difference_value).arrange(RIGHT, buff=0.05)
            rq_difference_text.next_to(q_len_text, DOWN, buff = 0.05)
            rq_difference_text.move_to([rq_difference_text.get_center()[0] - 0.09, rq_difference_text.get_center()[1], rq_difference_text.get_center()[2]])

            rq_difference_nabla.next_to(rq_difference_label)

            rq_difference_value.add_updater(lambda qr: qr.set_value(projection_r.get_length() - projection_q.get_length()))
            rq_difference_value.add_updater(lambda qr2: qr2.set_z_index(4))

            #Where to move explanation objects (idk how to call it lol)
            r_greater_q = Tex(r"$\boldsymbol{>0 \rightarrow move\;diagonally}$", font_size=11).next_to(rq_difference_text, RIGHT, buff = 0.05)
            r_less_q = Tex(r"$\boldsymbol{<0 \rightarrow move\;horizontally}$", font_size=11).next_to(rq_difference_text, RIGHT, buff = 0.13)
            r_zero_q = Tex(r"$\boldsymbol{=0 \rightarrow move\;diagonally}$", font_size=11).next_to(rq_difference_text, RIGHT, buff = 0.05)
            r_equal_q = Tex(r"$\boldsymbol{\geq0 \rightarrow move\;diagonally}$", font_size=11).next_to(rq_difference_text, RIGHT, buff = 0.05)

            arrow_r = Arrow(
                start=p_dot.get_center(),
                end=r_dot.get_center(),
                color=ManimColor('#FF0000'),
                buff=0.025,
                stroke_width=2,
                tip_length=0.1,
            )
            arrow_r.set_z_index(3)

            arrow_q = Arrow(
                start=p_dot.get_center(),
                end=q_dot.get_center(),
                color=ManimColor('#FF0000'),
                buff=0.025,
                stroke_width=2,
                tip_length=0.1,
            )
            arrow_q.set_z_index(3)

            text_rectangle = Rectangle(width=2.5, height=1, fill_opacity=1.0, fill_color=BLACK)
            text_rectangle.set_z_index(4)
            text_rectangle.move_to(plane.c2p(4, 1.5))

            # r>q:
            if_r_greater_q_if = Tex(r"$\boldsymbol{if}$", font_size=11).next_to(rq_difference_text, DOWN, buff=0.05) # This part is out of alignment, might need to fix later
            if_r_greater_q_rq = Tex(r"$\boldsymbol{r-q}$", font_size=11).next_to(if_r_greater_q_if, RIGHT, buff=0.05)
            if_r_greater_q_sign = Tex(r"$\boldsymbol{>}$", font_size=11).next_to(if_r_greater_q_rq, RIGHT, buff=0.05)

            if_r_greater_q_move_arrow = Tex(r"$\boldsymbol{0\rightarrow}$", font_size=11).next_to(if_r_greater_q_sign, RIGHT, buff=0.05)
            if_r_greater_q_move_move = Tex(r"$\boldsymbol{move\;}$", font_size=11).next_to(if_r_greater_q_move_arrow, RIGHT, buff=0.05)
            if_r_greater_q_move_diagonally = Tex(r"$\boldsymbol{diagonally}$", font_size=11).next_to(if_r_greater_q_move_move, RIGHT, buff=0.05)

            if_r_greater_q_move = VGroup(if_r_greater_q_move_arrow, if_r_greater_q_move_move, if_r_greater_q_move_diagonally)

            nudging_factor_greater = 0.25 # Used to offset to the left all the objects that have to do with if_r_greater_q

            if_r_greater_q = VGroup(if_r_greater_q_if, if_r_greater_q_rq, if_r_greater_q_sign, if_r_greater_q_move)
            for item in if_r_greater_q:
                item.move_to([item.get_center()[0] - nudging_factor_greater, item.get_center()[1], item.get_center()[2]])

            if_r_greater_q_nabla = Tex(r"$\boldsymbol{\nabla}$", font_size=11).next_to(if_r_greater_q_if, RIGHT, buff=0.05)
            if_r_greater_q_sign_change = Tex(r"$\boldsymbol{\ge}$", font_size=11).next_to(if_r_greater_q_rq, RIGHT, buff=0.05)


            # r<q:
            if_r_less_q_if = Tex(r"$\boldsymbol{if}$", font_size=11).next_to(if_r_greater_q_if, DOWN, buff=0.05)
            if_r_less_q_rq = Tex(r"$\boldsymbol{r-q}$", font_size=11).next_to(if_r_less_q_if, RIGHT, buff=0.05)
            if_r_less_q_sign = Tex(r"$\boldsymbol{<}$", font_size=11).next_to(if_r_less_q_rq, RIGHT, buff=0.05)

            if_r_less_q_move_arrow = Tex(r"$\boldsymbol{0\rightarrow}$", font_size=11).next_to(if_r_less_q_sign, RIGHT, buff=0.05)
            if_r_less_q_move_move = Tex(r"$\boldsymbol{move\;}$", font_size=11).next_to(if_r_less_q_move_arrow, RIGHT, buff=0.05)
            if_r_less_q_move_horizontally = Tex(r"$\boldsymbol{horizontally}$", font_size=11).next_to(if_r_less_q_move_move, RIGHT, buff=0.05)

            if_r_less_q_move = VGroup(if_r_less_q_move_arrow, if_r_less_q_move_move, if_r_less_q_move_horizontally)

            if_r_less_q = VGroup(if_r_less_q_if, if_r_less_q_rq, if_r_less_q_sign, if_r_less_q_move)
            if_r_less_q_nabla = Tex(r"$\boldsymbol{\nabla}$", font_size=11).next_to(if_r_less_q_if, RIGHT, buff=0.05)

            # Curly bracket:
            curly_brace_if_r = Tex(r"$\begin{cases}\\\end{cases}$", font_size=15)
            curly_brace_if_r.move_to([if_r_greater_q_if.get_center()[0] - 0.09, (if_r_greater_q_if.get_center()[1] + if_r_less_q_if.get_center()[1])/2, if_r_less_q_if.get_center()[2]])


            explanation_text = VGroup(
                r_len_text,
                q_len_text,
                rq_difference_text,
                r_greater_q,
                r_less_q,
                r_zero_q,
                r_equal_q,
                if_r_greater_q,
                if_r_less_q,
                if_r_greater_q_nabla,
                if_r_greater_q_sign_change,
                if_r_less_q_nabla,
                curly_brace_if_r,
                rq_difference_nabla
            )
            explanation_text.set_z_index(4)

            if_nabla_move_group = VGroup(
                if_r_greater_q_nabla,
                if_r_greater_q_sign_change,
                if_r_greater_q_move_arrow,
                if_r_greater_q_move_diagonally,
                if_r_less_q_nabla,
                if_r_less_q_sign,
                if_r_less_q_move_arrow,
                if_r_less_q_move_horizontally,
                curly_brace_if_r
            )

            #Stuff for "How are q and r calculated?"
            perpendicular_line = Line(d1.get_center(), d2_after_traverse.get_center(), color = ORANGE, stroke_width = 1) #Same direction as D1D2 for animation purposes
            perpendicular_line.set_z_index(3)
            movement_line = Line(ORIGIN, d1d2_line.get_projection(r_dot.get_center())) #Determines movement path for the line

            pythagoras_dot = Dot(point=[d1d2_line.get_projection(r_dot.get_center())[0], r_dot.get_y(), 0], color = RED, radius = 0.025) #Used for the triangle that shows Pythagoras
            projection_dot = Dot(point=d1d2_line.get_projection(r_dot.get_center()), color = RED, radius = 0.025)

            pythagoras_dot.set_z_index(3)
            projection_dot.set_z_index(3)

            pythagoras_horizontal_line = Line(
                start=r_dot.get_center(),
                end=pythagoras_dot.get_center(),
                stroke_width=1.6,
                color=RED
            )

            pythagoras_vertical_line = Line(
                start=d1d2_line.get_projection(r_dot.get_center()),
                end=pythagoras_dot.get_center(),
                stroke_width=1.6,
                color=RED
            )

            pythagoras_dashes = VGroup(pythagoras_horizontal_line, pythagoras_vertical_line)
            pythagoras_dashes.set_z_index(2)

            pythagoras_angle = RightAngle(
                pythagoras_horizontal_line,
                pythagoras_vertical_line,
                length=0.08,
                quadrant=(-1,-1),
                color=RED,
                stroke_width=1
            )
            pythagoras_angle.set_z_index(1)

            pythagoras_horizontal_label = Tex(r"c", font_size=8)
            pythagoras_horizontal_label.next_to(pythagoras_horizontal_line, DOWN, buff=0.03)

            pythagoras_vertical_label = Tex(r"d", font_size=8)
            pythagoras_vertical_label.next_to(pythagoras_vertical_line, LEFT, buff=0.03)

            pythagoras_diagonal_label = Tex(r"$\sqrt{c^2+d^2}$", font_size=8)
            pythagoras_diagonal_label.rotate(PI + static_projection_r.get_angle())
            pythagoras_diagonal_label.move_to(static_projection_r.get_center() + RIGHT * 0.05 + UP * 0.03)
            pythagoras_diagonal_label.set_z_index(3)

            #                                                                  Fourth Scene                                                                                    #


            # Angles
            line_QR = Line(start = q_dot.get_center(), end = r_dot.get_center(), color = ORANGE, stroke_width = 1.7)
            lower_angle = Angle(
                d1d2_line,
                line_QR,
                radius=0.1,
                quadrant=(-1, 1),
                stroke_width=0.5,
                color=ORANGE
            )

            upper_angle = Angle(
                d1d2_line,
                line_QR,
                radius=0.1,
                quadrant=(1, -1),
                stroke_width=0.5,
                color=ORANGE
            )

            unnecessary_smaller_angle_right= Angle(
                line_QR,
                d1d2_line,
                radius=0.12,
                quadrant=(1, 1),
                stroke_width=0.5,
                color = GREEN
            )

            unnecessary_bigger_angle_right= Angle(
                line_QR,
                d1d2_line,
                radius=0.14,
                quadrant=(1, 1),
                stroke_width=0.5,
                color = GREEN
            )

            unnecessary_smaller_angle_left = Angle(
                line_QR,
                d1d2_line,
                radius=0.12,
                quadrant=(-1, -1),
                stroke_width=0.5,
                color = GREEN
            )

            unnecessary_bigger_angle_left = Angle(
                line_QR,
                d1d2_line,
                radius=0.14,
                quadrant=(-1, -1),
                stroke_width=0.5,
                color = GREEN
            )

            # Labels for angles:
            nudging_factor_angle_horizontal = 0.13
            nudging_factor_angle_vertical = 0.06
            angle_label_alpha = Tex(r"$\boldsymbol{\alpha}$", font_size=7)
            angle_label_alpha.move_to(s_dot.get_center())
            angle_label_alpha.shift(nudging_factor_angle_horizontal * DOWN).shift(nudging_factor_angle_vertical * LEFT)

            angle_label_beta = Tex(r"$\boldsymbol{\beta}$", font_size=7)
            angle_label_beta.move_to(s_dot.get_center())
            angle_label_beta.shift((nudging_factor_angle_horizontal + 0.01) * UP).shift((nudging_factor_angle_vertical) * RIGHT)

            angle_label_group = VGroup(angle_label_alpha, angle_label_beta)
            angle_label_group.set_z_index(4)

            # Text for algebra:
            '''
            Context: Here are the equations:
            sin(alpha) = sin(beta)
            r / RS = q / QS
            r * QS = q * RS
            r = q * RS / QS
            r / q = RS / QS
            And eventually:
            r / q = r' / q'
            '''
            alpha_text = Tex(r"$\boldsymbol{\alpha}$", font_size=11)
            equals_text = Tex(r"$\boldsymbol{=}$", font_size=11)
            beta_text = Tex(r"$\boldsymbol{\beta}$", font_size=11)

            alpha_is_beta = VGroup(alpha_text, equals_text, beta_text).arrange(RIGHT, buff=0.05)
            alpha_is_beta.move_to(plane.c2p(3.5, 1.55))
            #sin alpha:
            alpha_sine_sine = Tex(r"$\boldsymbol{sin}$", font_size=11)
            alpha_sine_sine.move_to([
                alpha_text.get_center()[0] - 0.165,
                alpha_text.get_center()[1] + 0.0125,
                alpha_text.get_center()[2]
            ])
            alpha_sine = VGroup(alpha_text, alpha_sine_sine)
            #sin beta:
            beta_sine_sine = Tex(r"$\boldsymbol{sin}$", font_size=11)
            beta_sine_sine.move_to([
                equals_text.get_center()[0] + 0.165,
                equals_text.get_center()[1] + 0.0125,
                equals_text.get_center()[2]
            ])
            beta_sine = VGroup(beta_text, beta_sine_sine)

            # r/RS:

            r_fraction_text = Tex(r"$\boldsymbol{r}$", font_size=11)
            rs_fraction_text = Tex(r"$\boldsymbol{RS}$", font_size=11)

            r_rs_fraction_line = Line(
                start=[equals_text.get_left()[0] - get_len(rs_fraction_text) - fraction_offset, equals_text.get_center()[1], equals_text.get_center()[2]],
                end=[equals_text.get_left()[0] - fraction_offset, equals_text.get_center()[1], equals_text.get_center()[2]],
                color=WHITE,
                stroke_width=0.5
            )

            r_fraction_text.move_to([
                r_rs_fraction_line.get_center()[0],
                r_rs_fraction_line.get_center()[1] + get_height(r_fraction_text)/2 + fraction_offset/2,
                r_rs_fraction_line.get_center()[2]])
            rs_fraction_text.move_to([
                r_rs_fraction_line.get_center()[0],
                r_rs_fraction_line.get_center()[1] - get_height(rs_fraction_text)/2 - fraction_offset/2,
                r_rs_fraction_line.get_center()[2]
            ])

            r_rs_group = VGroup(r_rs_fraction_line, r_fraction_text, rs_fraction_text)
            r_rs_group.set_z_index(3)

            # q/QS:
            q_fraction_text = Tex(r"$\boldsymbol{q}$", font_size=11)
            qs_fraction_text = Tex(r"$\boldsymbol{QS}$", font_size=11)

            q_qs_fraction_line = Line(
                start=[equals_text.get_right()[0] + fraction_offset, equals_text.get_center()[1], equals_text.get_center()[2]],
                end=[equals_text.get_right()[0] + get_len(qs_fraction_text) + fraction_offset, equals_text.get_center()[1], equals_text.get_center()[2]],
                color=WHITE,
                stroke_width=0.5
            )

            q_fraction_text.move_to([
                q_qs_fraction_line.get_center()[0],
                q_qs_fraction_line.get_center()[1] + get_height(q_fraction_text)/2 + fraction_offset/2,
                q_qs_fraction_line.get_center()[2]
            ])
            qs_fraction_text.move_to([
                q_qs_fraction_line.get_center()[0],
                q_qs_fraction_line.get_center()[1] - get_height(qs_fraction_text)/2 - fraction_offset/2,
                q_qs_fraction_line.get_center()[2]
            ])

            q_qs_group = VGroup(q_fraction_text, qs_fraction_text, q_qs_fraction_line)

            # r*QS = q*RS

            r_qs_multiplication = Tex(r"$\times$", font_size=11)
            r_qs_multiplication.move_to([
                equals_text.get_left()[0] - get_len(qs_fraction_text) - fraction_offset - get_len(r_qs_multiplication)/2,
                equals_text.get_center()[1], equals_text.get_center()[2]
            ])

            q_rs_multiplication = Tex(r"$\times$", font_size=11)
            q_rs_multiplication.move_to([
                equals_text.get_right()[0] + get_len(q_fraction_text) + fraction_offset + get_len(q_rs_multiplication)/2,
                equals_text.get_center()[1], equals_text.get_center()[2]
            ])

            # r = q*RS/QS
            q_rs_group = VGroup(q_fraction_text, q_rs_multiplication, rs_fraction_text)
            q_rs_fraction_line = Line(
                start=[equals_text.get_right()[0] + fraction_offset/2, equals_text.get_center()[1], equals_text.get_center()[2]],
                end=[
                    equals_text.get_right()[0] + 1.5*fraction_offset + get_len(rs_fraction_text) + get_len(q_rs_multiplication) + get_len(q_fraction_text),
                    equals_text.get_center()[1], equals_text.get_center()[2]
                ],
                color=WHITE,
                stroke_width=0.5
            )

            # r/q = RS/QS
            rs_qs_fraction_line = Line(
                start=[equals_text.get_right()[0] + fraction_offset, equals_text.get_center()[1], equals_text.get_center()[2]],
                end=[equals_text.get_right()[0] + get_len(rs_fraction_text) + fraction_offset, equals_text.get_center()[1], equals_text.get_center()[2]],
                color=WHITE,
                stroke_width=0.5
            )
            r_q_fraction_line = Line(
                start=[equals_text.get_left()[0] - fraction_offset - get_len(q_fraction_text), equals_text.get_center()[1], equals_text.get_center()[2]],
                end=[equals_text.get_left()[0] - fraction_offset, equals_text.get_center()[1], equals_text.get_center()[2]],
                color=WHITE,
                stroke_width=0.5
            )

            # r' label
            r_prime_label = Tex(r"$\boldsymbol{r'}$", font_size=11)
            r_prime_label.move_to([r_dot.get_center()[0] + 0.08, (r_dot.get_center()[1] + s_dot.get_center()[1])/2, r_dot.get_center()[2]])

            # q' label
            q_prime_label = Tex(r"$\boldsymbol{q'}$", font_size=11)
            q_prime_label.move_to([q_dot.get_center()[0] - 0.07, (q_dot.get_center()[1] + s_dot.get_center()[1])/2, q_dot.get_center()[2]])

            # r' and q' texts in the algebra
            r_prime_text = Tex(r"$\boldsymbol{r'}$", font_size=11)
            q_prime_text = Tex(r"$\boldsymbol{q'}$", font_size=11)

            r_prime_q_fraction_line = Line(
                start=[equals_text.get_right()[0] + fraction_offset, equals_text.get_center()[1], equals_text.get_center()[2]],
                end=[equals_text.get_right()[0] + get_len(q_prime_text) + fraction_offset, equals_text.get_center()[1], equals_text.get_center()[2]],
                color=WHITE,
                stroke_width=0.5
            )

            r_prime_text.move_to([
                r_prime_q_fraction_line.get_center()[0],
                r_prime_q_fraction_line.get_top()[1] + fraction_offset + get_height(r_prime_text)/2,
                r_prime_text.get_center()[2]
            ])
            q_prime_text.move_to([
                r_prime_q_fraction_line.get_center()[0],
                r_prime_q_fraction_line.get_bottom()[1] - (fraction_offset - 0.02)  - get_height(q_prime_text)/2,
                r_prime_text.get_center()[2]
            ])

            r_prime_q_group = VGroup(r_prime_text, r_prime_q_fraction_line, q_prime_text)

            # Coordinates part:
            # Arrows to explain the script:

            p_r_arrow = Arrow(start=p_dot.get_center(), end=r_dot.get_center(), color=GREEN, buff=get_len(p_dot)/4, stroke_width=2, tip_length=0.1)
            p_r_arrow_label = Tex(r"$\boldsymbol{+1}$", font_size=10).next_to(p_r_arrow, UP, buff=0.00625)
            p_r_arrow_group = VGroup(p_r_arrow, p_r_arrow_label)
            p_r_arrow_group.set_z_index(2)

            '''
            Quick explanation regarding how the code below works. Originally the coordinates have a form:
            P(???, ????), Q(???, ???), R(???, ???)
            In the code you can also see different offsets. Here's how the offsets are divided in this case (as they do change when the question marks become values):

            P                          (                           ???                           ,                             ???                          )
            | <- fraction_offset/2 -> | | <- fraction_offset/2 -> |   | <- fraction_offset/2 -> | | <- fraction_offset*3/2 -> |   | <- fraction_offset/2 -> |

            (This technically isn't completely true, I've noticed some bugs in the code, but seeing as it works well I don't want to touch it) 
            
            Tallied up that is 3.5*fraction_offset, and that's why when calculating length (either p_name_original_length, q_name_original_length or r_name_original_legnth)
            there is always 3.5*fraction_offset present. That value changes however when the right question mark ([insert dot name here]_name_question_y) becomes a value, as
            this offset:

            P                          (                           ???                           ,                             ???                          )
            | <- fraction_offset/2 -> | | <- fraction_offset/2 -> |   | <- fraction_offset/2 -> | | <- fraction_offset*3/2 -> |   | <- fraction_offset/2 -> |
                                                                                                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                                                                                            This one
            
            becomes too big for values like b_1. That's why the values of the offsets change a bit:

            P                          (                           a1                           ,                         b1                          )
            | <- fraction_offset/2 -> | | <- fraction_offset/2 -> |  | <- fraction_offset/2 -> | | <- fraction_offset -> |  | <- fraction_offset/2 -> |
                                                                                                  ^^^^^^^^^^^^^^^^^^^^^^^
                                                                                                   This value has changed

            That's why the last value for the length of the whole expression (p_name_length or q_name_second_length) is 3*fraction_offset, instead of 3.5*fraction_offset

            The coordinates originally are calculated based on being next to p_name_coords that is calculated based on the coordinates p_dot - the green dot on the screen.
            During animation though this approach is not possible as I wanted to preserve the coordinates' center position on the dot even after the change in length.
            That's why the movements take the center position dot for the anchor and base their possition off its position. Here is an example for the open brace in P (p_name_open_brace):

                   P                                          (                                               a1                                  ,                                 b1                                  )
                                                                                                                                               P_DOT
            |                                                         <- p_name_length/2                                                         |
                                                     
            |length(p_name) ->|fraction_offset/2 ->|length(open_brace) ->|fraction_offset/2 ->|length(a_1)/2 ->|

            The length(a_1)/2 is necessary because mobject.move_to() moves the coordinates of the CENTER of the mobject, and so the length of a_1 has to also be taken into account
            '''
            # P:
            p_name_open_brace = Tex(r"$\boldsymbol{(}$", font_size=11)
            p_name_question_x = Tex(r"$\boldsymbol{???}$", font_size=11)
            p_name_coma = Tex(r"$\boldsymbol{,}$", font_size=11)
            p_name_question_y = Tex(r"$\boldsymbol{???}$", font_size=11)
            p_name_close_brace = Tex(r"$\boldsymbol{)}$", font_size=11)
            p_name_x = Tex(r"$\boldsymbol{a_1}$", font_size=11)
            p_name_y = Tex(r"$\boldsymbol{b_1}$", font_size=11)
            p_name_x.set_z_index(3)
            p_name_y.set_z_index(3)

            p_name_axis_offset = 0.1
            p_name_original_length = get_len(p_dot) + 3.5*fraction_offset + get_len(p_name_open_brace) + get_len(p_name_question_x) + get_len(p_name_coma) + get_len(p_name_question_y) + get_len(p_name_close_brace)


            p_name_coords = [
                p_dot.get_center()[0] - p_name_original_length/2 + get_len(p_dot)/2,
                p_dot.get_center()[1] + p_name_axis_offset + get_height(p_dot)/2,
                p_dot.get_center()[2]
            ]

            p_name_open_brace.move_to([
                p_name_coords[0] + get_len(p_name)/2 + fraction_offset/2,
                p_name_coords[1], p_name_coords[2]
            ])

            p_name_question_x.move_to([
                p_name_open_brace.get_right()[0] + fraction_offset/2 + get_len(p_name_question_x)/2,
                p_name_open_brace.get_center()[1],
                p_name_open_brace.get_center()[2]
            ])

            p_name_coma.move_to([
                p_name_question_x.get_right()[0] + fraction_offset/2 + get_len(p_name_coma)/2,
                p_name_question_x.get_bottom()[1],
                p_name_question_x.get_center()[2]
            ])

            p_name_question_y.move_to([
                p_name_coma.get_right()[0] + fraction_offset*3/2 + get_len(p_name_question_y)/2,
                p_name_question_x.get_center()[1],
                p_name_coma.get_center()[2]
            ])

            p_name_close_brace.move_to([
                p_name_question_y.get_right()[0] + fraction_offset/2 + get_len(p_name_close_brace)/2,
                p_name_coords[1],
                p_name_question_y.get_center()[2]
            ])

            p_name_group = VGroup(p_name_open_brace, p_name_question_x, p_name_coma, p_name_question_y, p_name_close_brace)
            p_name_group.set_z_index(4)

            p_name_length = get_len(p_dot) + 3*fraction_offset + get_len(p_name_open_brace) + get_len(p_name_x) + get_len(p_name_coma) + get_len(p_name_y) + get_len(p_name_close_brace)

            p_name_x.move_to([
                p_dot.get_center()[0] - p_name_length/2 + get_len(p_dot) + get_len(p_name_open_brace) + fraction_offset + get_len(p_name_x)/2,
                p_name_coords[1] - get_height(p_name)/2 + get_height(p_name_x)/2,
                p_name_coords[2]
            ])

            p_name_y.move_to([
                p_dot.get_center()[0] + p_name_length/2 - get_len(p_name_close_brace) - fraction_offset/2 - get_len(p_name_y)/2,
                p_name_coords[1] - get_height(p_name)/2 + get_height(p_name_y)/2,
                p_name_coords[2]
            ])

            p_name_second_group = VGroup(p_name, p_name_open_brace, p_name_x, p_name_coma, p_name_y, p_name_close_brace)
            p_name_second_group.set_z_index(4)

            p_name_rectangle = Rectangle(width=get_len(p_name_second_group), height=get_height(p_name_second_group), fill_opacity=0.75, fill_color=BLACK, stroke_opacity=0.0)
            p_name_rectangle.set_z_index(3)
            p_name_rectangle.move_to([p_dot.get_center()[0], p_dot.get_center()[1] + p_name_axis_offset + get_height(p_dot)/2, p_dot.get_center()[2]])

            # Q:
            q_name_open_brace = Tex(r"$\boldsymbol{(}$", font_size=11)
            q_name_question_x = Tex(r"$\boldsymbol{???}$", font_size=11)
            q_name_coma = Tex(r"$\boldsymbol{,}$", font_size=11)
            q_name_question_y = Tex(r"$\boldsymbol{???}$", font_size=11)
            q_name_close_brace = Tex(r"$\boldsymbol{)}$", font_size=11)
            q_name_x = Tex(r"$\boldsymbol{a_1 + 1}$", font_size=11)
            q_name_y = Tex(r"$\boldsymbol{b_1 + 1}$", font_size=11)

            q_name_axis_offset = 0.1
            q_name_original_length = get_len(q_dot) + 3.5*fraction_offset + get_len(q_name_open_brace) + get_len(q_name_question_x) + get_len(q_name_coma) + get_len(q_name_question_y) + get_len(q_name_close_brace)

            q_name_first_length = get_len(q_dot) + 3.5*fraction_offset + get_len(q_name_open_brace) + get_len(q_name_x) + get_len(q_name_coma) + get_len(q_name_question_y) + get_len(q_name_close_brace)

            q_name_second_length = get_len(q_dot) + 3*fraction_offset + get_len(q_name_open_brace) + get_len(q_name_x) + get_len(q_name_coma) + get_len(q_name_y) + get_len(q_name_close_brace)

            q_name_coords = [
                q_dot.get_center()[0] - q_name_original_length/2 + get_len(q_dot)/2,
                q_dot.get_center()[1] + q_name_axis_offset + get_height(q_dot)/2,
                q_dot.get_center()[2]
            ]

            q_name_open_brace.move_to([
                q_name_coords[0] + get_len(q_name)/2 + fraction_offset/2,
                q_name_coords[1], q_name_coords[2]
            ])

            q_name_question_x.move_to([
                q_name_open_brace.get_right()[0] + fraction_offset/2 + get_len(q_name_question_x)/2,
                q_name_open_brace.get_center()[1],
                q_name_open_brace.get_center()[2]
            ])

            q_name_coma.move_to([
                q_name_question_x.get_right()[0] + fraction_offset/2 + get_len(q_name_coma)/2,
                q_name_question_x.get_bottom()[1],
                q_name_question_x.get_center()[2]
            ])

            q_name_question_y.move_to([
                q_name_coma.get_right()[0] + fraction_offset*3/2 + get_len(q_name_question_y)/2,
                q_name_question_x.get_center()[1],
                q_name_coma.get_center()[2]
            ])

            q_name_close_brace.move_to([
                q_name_question_y.get_right()[0] + fraction_offset/2 + get_len(q_name_close_brace)/2,
                q_name_coords[1],
                q_name_question_y.get_center()[2]
            ])

            q_name_group = VGroup(q_name_open_brace, q_name_question_x, q_name_coma, q_name_question_y, q_name_close_brace)
            q_name_group.set_z_index(4)

            q_name_x.move_to([
                q_dot.get_center()[0] - q_name_first_length/2 + get_len(q_dot) + get_len(q_name_open_brace) + fraction_offset + get_len(q_name_x)/2,
                q_name_coords[1] - get_height(q_name)/2 + get_height(q_name_x)/2,
                q_name_coords[2]
            ])

            q_name_y.move_to([
                q_dot.get_center()[0] + q_name_first_length/2 - get_len(q_name_close_brace) - get_len(q_name_y)/2 + fraction_offset,
                q_name_coords[1] - get_height(q_name)/2 + get_height(q_name_y)/2,
                q_name_coords[2]
            ])

            q_name_second_group = VGroup(q_name, q_name_open_brace, q_name_x, q_name_coma, q_name_y, q_name_close_brace)
            q_name_second_group.set_z_index(4)

            q_name_rectangle = Rectangle(width=get_len(q_name_second_group), height=get_height(q_name_second_group), fill_opacity=0.75, fill_color=BLACK, stroke_opacity=0.0)
            q_name_rectangle.set_z_index(3)
            q_name_rectangle.move_to([q_dot.get_center()[0], q_dot.get_center()[1] + q_name_axis_offset + get_height(q_dot)/2, q_dot.get_center()[2]])

            #R:
            r_name_open_brace = Tex(r"$\boldsymbol{(}$", font_size=11)
            r_name_question_x = Tex(r"$\boldsymbol{???}$", font_size=11)
            r_name_coma = Tex(r"$\boldsymbol{,}$", font_size=11)
            r_name_question_y = Tex(r"$\boldsymbol{???}$", font_size=11)
            r_name_close_brace = Tex(r"$\boldsymbol{)}$", font_size=11)
            r_name_x = Tex(r"$\boldsymbol{a_1 + 1}$", font_size=11)
            r_name_y = Tex(r"$\boldsymbol{b_1}$", font_size=11)
            r_name_x.set_z_index(3)
            r_name_y.set_z_index(3)

            r_name_axis_offset = 0.1
            r_name_original_length = get_len(r_dot) + 3.5*fraction_offset + get_len(r_name_open_brace) + get_len(r_name_question_x) + get_len(r_name_coma) + get_len(r_name_question_y) + get_len(r_name_close_brace)
            r_name_second_length = get_len(r_dot) + 3*fraction_offset + get_len(r_name_open_brace) + get_len(r_name_x) + get_len(r_name_coma) + get_len(r_name_y) + get_len(r_name_close_brace)

            r_name_coords = [
                r_dot.get_center()[0] - r_name_original_length/2 + get_len(r_dot)/2,
                r_dot.get_center()[1] - r_name_axis_offset - get_height(r_dot)/2,
                r_dot.get_center()[2]
            ]

            r_name_open_brace.move_to([
                r_name_coords[0] + get_len(r_name)/2 + fraction_offset/2,
                r_name_coords[1], r_name_coords[2]
            ])

            r_name_question_x.move_to([
                r_name_open_brace.get_right()[0] + fraction_offset/2 + get_len(r_name_question_x)/2,
                r_name_open_brace.get_center()[1],
                r_name_open_brace.get_center()[2]
            ])

            r_name_coma.move_to([
                r_name_question_x.get_right()[0] + fraction_offset/2 + get_len(r_name_coma)/2,
                r_name_question_x.get_bottom()[1],
                r_name_question_x.get_center()[2]
            ])

            r_name_question_y.move_to([
                r_name_coma.get_right()[0] + fraction_offset*3/2 + get_len(r_name_question_y)/2,
                r_name_question_x.get_center()[1],
                r_name_coma.get_center()[2]
            ])

            r_name_close_brace.move_to([
                r_name_question_y.get_right()[0] + fraction_offset/2 + get_len(r_name_close_brace)/2,
                r_name_coords[1],
                r_name_question_y.get_center()[2]
            ])

            r_name_group = VGroup(r_name_open_brace, r_name_question_x, r_name_coma, r_name_question_y, r_name_close_brace)
            r_name_group.set_z_index(4)

            r_name_first_length = get_len(r_dot) + 3.5*fraction_offset + get_len(r_name_open_brace) + get_len(r_name_x) + get_len(r_name_coma) + get_len(r_name_question_y) + get_len(r_name_close_brace)

            r_name_x.move_to([
                r_dot.get_center()[0] - r_name_first_length/2 + get_len(r_dot) + get_len(r_name_open_brace) + fraction_offset + get_len(r_name_x)/2,
                r_name_coords[1] - get_height(r_name)/2 + get_height(r_name_x)/2,
                r_name_coords[2]
            ])

            r_name_y.move_to([
                r_dot.get_center()[0] + r_name_first_length/2 - get_len(r_name_close_brace) - fraction_offset - get_len(r_name_y)/2,
                r_name_coords[1] - get_height(r_name)/2 + get_height(r_name_y)/2,
                r_name_coords[2]
            ])

            r_name_second_group = VGroup(r_name, r_name_open_brace, r_name_x, r_name_coma, r_name_y, r_name_close_brace)
            r_name_second_group.set_z_index(4)

            r_name_rectangle = Rectangle(width=get_len(r_name_second_group), height=get_height(r_name_second_group), fill_opacity=0.75, fill_color=BLACK, stroke_opacity=0.0)
            r_name_rectangle.set_z_index(3)
            r_name_rectangle.move_to([r_dot.get_center()[0], r_dot.get_center()[1] - r_name_axis_offset - get_height(r_dot)/2, r_dot.get_center()[2]])

            # S:
            s_name_open_brace = Tex(r"$\boldsymbol{(}$", font_size=11)
            s_name_question_x = Tex(r"$\boldsymbol{???}$", font_size=11)
            s_name_coma = Tex(r"$\boldsymbol{,}$", font_size=11)
            s_name_question_y = Tex(r"$\boldsymbol{???}$", font_size=11)
            s_name_close_brace = Tex(r"$\boldsymbol{)}$", font_size=11)
            s_name_x = Tex(r"$\boldsymbol{a_1 + 1}$", font_size=11)
            s_name_y = Tex(r"$\boldsymbol{\frac{\Delta b}{\Delta a}(a_1 + 1)}$", font_size=14)

            s_name_axis_offset = 0.1
            s_name_original_length = get_len(s_dot) + 3.5*fraction_offset + get_len(s_name_open_brace) + get_len(s_name_question_x) + get_len(s_name_coma) + get_len(s_name_question_y) + get_len(s_name_close_brace)

            s_name_first_length = get_len(s_dot) + 3.5*fraction_offset + get_len(s_name_open_brace) + get_len(s_name_x) + get_len(s_name_coma) + get_len(s_name_question_y) + get_len(s_name_close_brace)

            s_name_second_length = get_len(s_dot) + 3*fraction_offset + get_len(s_name_open_brace) + get_len(s_name_x) + get_len(s_name_coma) + get_len(s_name_y) + get_len(s_name_close_brace)

            s_name_coords = static_s_name.get_center()

            s_name_open_brace.move_to([
                s_name_coords[0] + get_len(s_name),
                s_name_coords[1], s_name_coords[2]
            ])

            s_name_question_x.move_to([
                s_name_open_brace.get_right()[0] + fraction_offset/2 + get_len(s_name_question_x)/2,
                s_name_open_brace.get_center()[1],
                s_name_open_brace.get_center()[2]
            ])

            s_name_coma.move_to([
                s_name_question_x.get_right()[0] + fraction_offset/2 + get_len(s_name_coma)/2,
                s_name_question_x.get_bottom()[1],
                s_name_question_x.get_center()[2]
            ])

            s_name_question_y.move_to([
                s_name_coma.get_right()[0] + fraction_offset*3/2 + get_len(s_name_question_y)/2,
                s_name_question_x.get_center()[1],
                s_name_coma.get_center()[2]
            ])

            s_name_close_brace.move_to([
                s_name_question_y.get_right()[0] + fraction_offset/2 + get_len(s_name_close_brace)/2,
                s_name_coords[1],
                s_name_question_y.get_center()[2]
            ])

            s_name_group = VGroup(s_name_open_brace, s_name_question_x, s_name_coma, s_name_question_y, s_name_close_brace)
            s_name_group.set_z_index(4)

            s_name_x.move_to([
                s_name_open_brace.get_right()[0] + fraction_offset/2 + get_len(s_name_x)/2,
                s_name_coords[1] - get_height(s_name)/2 + get_height(s_name_x)/2,
                s_name_coords[2]
            ])

            s_name_rectangle = q_name_rectangle.copy()
            s_name_rectangle.set_z_index(3)

            removal_group = VGroup( # Used for the explanation of S
                p_name_second_group,
                p_name_rectangle,
                q_name_second_group,
                q_name_rectangle,
                r_name_second_group,
                r_name_rectangle,
                p_dot,
                lower_angle,
                upper_angle,
                little_r_name,
                little_q_name,
                projection_r,
                projection_q,
                q_dot,
                r_dot,
                right_angle_q,
                right_angle_r
            )
            removed_group = VGroup(
                equals_text,
                r_prime_text,
                q_prime_text,
                r_fraction_text,
                q_fraction_text,
                r_q_fraction_line,
                r_prime_q_fraction_line,
            )
            active_mobjects_group = VGroup(
                little_r_name,
                little_q_name,
                projection_r,
                projection_q,
                right_angle_r,
                right_angle_q,
            )
            returning_mobjects_group = VGroup(
                q_prime_label,
                r_prime_label,
            )

            # Equation for S:
            b_equation_b = Tex(r"$\boldsymbol{b}$", font_size=11)
            b_equation_equals = Tex(r"$\boldsymbol{=}$", font_size=11)
            b_equation_m = Tex(r"$\boldsymbol{m}$", font_size=11)
            b_equation_a = Tex(r"$\boldsymbol{a}$", font_size=11)

            b_equation_m_m = Tex(r"$\boldsymbol{m}$", font_size=11)
            b_equation_m_equals = Tex(r"$\boldsymbol{=}$", font_size=11)
            b_equation_delta = Tex(r"$\boldsymbol{\frac{\Delta b}{\Delta a}}$", font_size=14)

            b_equation_times = Tex(r"$\boldsymbol{\times}$", font_size=11)
            
            b_equation_question = s_name_question_y.copy()
            b_equation_a1 = s_name_x.copy()

            b_equation_open_brace = Tex(r"$\boldsymbol{(}$", font_size=11)
            b_equation_close_brace = Tex(r"$\boldsymbol{)}$", font_size=11)

            b_equation_start_coords = plane.c2p(3.5, 1.6)
            b_equation_equals.move_to(b_equation_start_coords)
            
            b_equation_b.next_to(b_equation_equals, LEFT, buff=fraction_offset/2)
            b_equation_m.next_to(b_equation_equals, RIGHT, buff=fraction_offset/2)
            b_equation_a.next_to(b_equation_m, RIGHT, buff=0)

            b_equation_m_equals.next_to(b_equation_equals, DOWN, buff=5/2*fraction_offset)
            b_equation_m_m.next_to(b_equation_m_equals, LEFT, buff=fraction_offset/2)
            b_equation_delta.next_to(b_equation_m_equals, RIGHT, buff=fraction_offset/2)

            b_equation_times.move_to([
                b_equation_equals.get_right()[0] + fraction_offset + get_len(b_equation_delta) + get_len(b_equation_times)/2,
                b_equation_start_coords[1], b_equation_start_coords[2]
            ])
        
            # Square for the last step:
            b_equation_rectangle = Rectangle(height=get_height(b_equation_delta), width=get_len(b_equation_a1), fill_opacity=0.75, fill_color=BLACK, stroke_opacity=0.0)
            b_equation_rectangle.set_z_index(3)

            # Groups:
            b_equation = VGroup(b_equation_b, b_equation_equals, b_equation_m, b_equation_a, b_equation_m_m, b_equation_m_equals, b_equation_delta)

            b_second_equation = VGroup(b_equation_b, b_equation_equals, b_equation_delta, b_equation_times, b_equation_a)

            b_third_equation = VGroup(b_equation_delta, b_equation_times, b_equation_open_brace, b_equation_a1, b_equation_close_brace)
            b_third_equation.set_z_index(4)

            s_name_second_group = VGroup(s_name, s_name_open_brace, s_name_x, s_name_coma, b_third_equation, s_name_close_brace)
            s_name_second_group.set_z_index(4)
            
            # Braces for the last part of Scene 4:
            q_prime_brace = BraceBetweenPoints(q_dot.get_center(), s_dot.get_center(), buff=get_len(q_dot)/2, sharpness=2.0)
            q_prime_brace.width = 0.1
            q_prime_brace.stretch_to_fit_height(q_dot.get_center()[1] - s_dot.get_center()[1])
            q_prime_brace.move_to([q_dot.get_left()[0] - get_len(q_prime_brace)/2, q_prime_brace.get_center()[1], q_prime_brace.get_center()[2]])
            q_prime_brace.set_z_index(3)

            r_prime_brace = BraceBetweenPoints(s_dot.get_center(), r_dot.get_center(), buff=get_len(r_dot)/2, sharpness=2.0, direction=[1.0, 0.0, 0.0])
            r_prime_brace.width = 0.1
            r_prime_brace.stretch_to_fit_height(s_dot.get_center()[1] - r_dot.get_center()[1])
            r_prime_brace.move_to([r_dot.get_right()[0] + get_len(r_prime_brace)/2, r_prime_brace.get_center()[1], r_prime_brace.get_center()[2]])
            r_prime_brace.set_z_index(3)
            
            # Equations for the last part of Scene 4:
            q_prime_equation = Tex(r"$\boldsymbol{=Q_{vertical}-S_{vertical}}$", font_size=11)
            q_prime_brace.put_at_tip(q_prime_equation, buff=fraction_offset)
            q_prime_equation.shift([0, -0.01, 0])
            q_prime_equation.set_z_index(4)

            q_prime_equation_rectangle = Rectangle(width=get_len(q_prime_equation), height=get_height(q_prime_equation), fill_opacity=0.75, fill_color=BLACK, stroke_opacity=0.0)
            q_prime_equation_rectangle.move_to(q_prime_equation.get_center())
            q_prime_equation_rectangle.set_z_index(3)
            
            r_prime_equation = Tex(r"$\boldsymbol{=S_{vertical}-R_{vertical}}$", font_size=11)
            r_prime_equation.next_to(r_prime_label, RIGHT, buff=fraction_offset + get_len(r_prime_label))
            r_prime_equation.shift([0, -0.01, 0])
            r_prime_equation.set_z_index(4)

            r_prime_equation_rectangle = Rectangle(width=get_len(r_prime_equation), height=get_height(r_prime_equation), fill_opacity=0.75, fill_color=BLACK, stroke_opacity=0.0)
            r_prime_equation_rectangle.move_to(r_prime_equation.get_center())
            r_prime_equation_rectangle.set_z_index(3)

            #                                                                       ANIMATIONS
            self.next_section(skip_animations=True)
            #Animation_Square
            self.play(Create(square))
            self.wait(2)
            self.play(Create(dot), run_time=1)

            #Animation_Arrow_1mm
            self.play(Create(arrow_1mm), run_time=1)
            self.wait(2)
            self.play(Write(text_1mm), run_time=1)
            self.wait(2)


            #Animation_Arrow_2mm
            self.play(Create(arrow_2mm), run_time=1)
            self.wait(2)
            self.play(Write(text_2mm), run_time=1)
            self.wait(2)
            self.play(Transform(text_2mm, text_2mm_approx), run_time=1)
            self.wait(1)

            #Animation_unzoom
            self.play(self.camera.frame.animate.scale(2).move_to(ORIGIN), Unwrite(all_text_in_sqare), Unwrite(all_arrows_in_square),run_time=2)
            self.play(Create(box), run_time = 4)

            #D1D2 Animation
            self.play(Create(d1), Create(d2), run_time=1) #По сути лишний код (часть "Create(d1)" ), у нас уже есть эта точка, но в коде выглядит логичнее так
            self.wait(2)
            self.play(Create(d1d2_line), run_time=2)
            self.wait(2)
            self.play(Write(d1d2_names), run_time=1)

            self.play(d1_name.animate.shift(LEFT * 0.17), d2_name.animate.shift(LEFT * 0.17), run_time=1)

            self.play(Write(x1y1_text.next_to(d1_name, RIGHT * 0.5)), Write(x2y2_text.next_to(d2_name, RIGHT * 0.5)), run_time=1)
            self.wait(1.5)

            #Animation_arrows_on_sides
            self.play(Write(b_group), Write(a_group), run_time=1)
            self.wait(1)


            self.wait(1)

            #Animation_Change_of_coordinates
            self.play(Unwrite(x1y1_text), run_time=1)
            self.wait(0.2)
            self.play(Write(d1_new_coord_text.next_to(d1_name, RIGHT * 0.5)), run_time=1)

            self.wait(1)

            self.play(Unwrite(x2y2_text), run_time=1)
            self.wait(0.2)
            self.play(Write(d2_new_coord_text1.next_to(d2_name, RIGHT * 0.5)), run_time=1)

            self.wait(1)

            self.play(Unwrite(d2_new_coord_text1), run_time=1)
            self.wait(0.2)
            self.play(Write(d2_new_coord_text2.next_to(d2_name, RIGHT * 0.5)), run_time=1)

            self.wait(1)

            #Animation_b_equation

            self.play(Write(b_equation_1), run_time=2)
            self.wait(0.5)
            self.play(Write(b_equation_2), run_time=2)
            self.wait(1)

            #Animation_grid_numbers
            self.play(Write(grid_diag_numbers), Write(grid_vertical_numbers), run_time=2)

            self.wait(2)

            #Animation_D2_Traverse
            self.play(Uncreate(d1d2_line), run_time=1)
            self.play(Uncreate(d2_name), Uncreate(d2_new_coord_text2) ,run_time=0.5)

            self.wait(0.5)

            self.play(d2.animate.move_to(plane.c2p(3.4, 2.2)), run_time=2)

            self.wait(1)

            self.play(Create(dashed_horizontal_line), Create(dashed_vertical_line), run_time=2)

            self.wait(1)

            self.play(d2.animate.move_to(plane.c2p(3.0, 2.0)), run_time=1)
            self.play(Write(d2_newpos_name), Write(d2_new_coord_names), run_time=0.7)

            self.wait(2)

            #Undoing_Whats_Done
            self.play(Uncreate(dashed_lines), Unwrite(d2_newpos_name), Unwrite(d2_new_coord_names), Uncreate(d2), run_time=2)
            self.wait(0.7)

            self.play(Create(d2_original), run_time=1)
            self.play(Write(d2_original_name), Write(d2_original_delta_coord.next_to(d2_original_name, RIGHT * 0.5)), run_time=1)
            self.wait(2)
            self.play(Create(d1d2_original_line), run_time=2)
            self.wait(3)

            self.next_section(skip_animations=True)

            #                                                                  Third Scene                                                                                    #

            self.play(self.camera.frame.animate.move_to(plane.c2p(2, 1.5)).scale(0.45), run_time=2)
            self.wait(1.5)

            #P
            self.play(Create(p_arrow))
            self.play(Create(p_dot), Write(p_name))
            self.play(Uncreate(p_arrow))

            self.wait(1.5)

            #R and Q
            self.play(Create(r_dot), Write(r_name), Create(q_dot), Write(q_name))
            self.wait(1.5)

            #S
            self.play(Write(s_dot), Write(s_name))

            #R or Q?

            self.play(Create(line_to_r), Create(line_to_q))
            self.wait(1.5)

            self.play(Uncreate(line_to_r), Uncreate(line_to_q))
            self.wait(1.5)
            self.play(Create(static_projections))
            self.wait(1)
            self.play(Create(static_right_angle_r), Create(static_right_angle_q))

            self.play(Write(static_little_q_name), Write(static_little_r_name))
            self.wait(3)

            #How are q and r calculated?
            self.play(Unwrite(static_little_q_name), Unwrite(static_little_r_name))
            self.play(Uncreate(static_right_angle_r), Uncreate(static_right_angle_q), Uncreate(static_projections))

            self.play(Create(perpendicular_line, run_time=3))
            self.wait(1)
            self.play(Rotate(perpendicular_line, angle=1/2*PI, about_point=ORIGIN, rate_func=smooth))

            perpendicular_line_right_angle = RightAngle(
                d1d2_line,
                perpendicular_line,
                length=0.1,
                stroke_width = 1.3,
                quadrant=(1, 1),
                color=ORANGE
            )
            perpendicular_line_right_angle.set_z_index(2)

            self.play(Create(perpendicular_line_right_angle))
            self.wait(0.2)
            self.play(Uncreate(perpendicular_line_right_angle))

            self.play(MoveAlongPath(perpendicular_line, movement_line, rate_func=smooth))
            temp_perpendicular_line1 = Line(start=d1d2_line.get_projection(r_dot.get_center()), end=perpendicular_line.get_end(), color = ORANGE, stroke_width = 1)
            temp_perpendicular_line2 = Line(start=d1d2_line.get_projection(r_dot.get_center()), end=perpendicular_line.get_start(), color = ORANGE, stroke_width = 1)
            self.add(temp_perpendicular_line1)
            self.add(temp_perpendicular_line2)
            self.add(projection_r)
            self.remove(perpendicular_line)
            self.play(Uncreate(temp_perpendicular_line1), Uncreate(temp_perpendicular_line2))

            self.play(Create(pythagoras_dashes))
            self.play(Create(pythagoras_angle), Create(pythagoras_dot), Create(projection_dot))
            self.wait(1)

            self.play(Create(pythagoras_horizontal_label, run_time=0.5), Create(pythagoras_vertical_label, run_time=0.5))
            self.play(Create(pythagoras_diagonal_label, run_time=0.5))

            self.wait(3)

            #Returning back to normal:
            self.play(Uncreate(pythagoras_dot), Uncreate(projection_dot))
            self.play(Uncreate(pythagoras_diagonal_label, run_time=0.5), Uncreate(pythagoras_horizontal_label, run_time=0.5), Uncreate(pythagoras_vertical_label, run_time=0.5))
            self.play(Uncreate(pythagoras_angle, run_time=0.5), Uncreate(pythagoras_dashes, run_time=0.5))
            self.play(Create(projection_q))
            self.play(Create(right_angle_q), Create(right_angle_r))
            self.play(Write(little_q_name), Write(little_r_name))

            self.next_section(skip_animations=True)

            #r-q:
            self.play(self.camera.frame.animate.shift(RIGHT * 1.2), runtime = 0.7)
            self.wait(0.5)
            self.play(FadeIn(text_rectangle))

            self.play(Write(r_len_text), Write(q_len_text))
            self.wait(1.5)
            self.play(Write(rq_difference_text))
            self.wait(2)

            self.play(Create(arrow_q))
            self.play(Write(r_greater_q))
            self.wait(0.5)
            self.play(ReplacementTransform(r_greater_q, if_r_greater_q))
            self.wait(2)

            self.play(Uncreate(arrow_q))
            self.wait(1)
            self.play(d2_after_traverse.animate.move_to(plane.c2p(5, 3.3)), run_time=3)
            self.wait(1)
            self.play(Create(arrow_r))
            self.play(Write(r_less_q))
            self.wait(0.5)
            self.play(ReplacementTransform(r_less_q, if_r_less_q), Write(curly_brace_if_r))
            self.wait(2)

            self.play(Uncreate(arrow_r))
            self.play(d2_after_traverse.animate.move_to(plane.c2p(6, 4.5)), run_time=3)
            self.wait(1)
            self.play(Write(r_zero_q))
            self.wait(1)
            self.play(Unwrite(r_zero_q), ReplacementTransform(if_r_greater_q_sign, if_r_greater_q_sign_change))


            self.play(d2_after_traverse.animate.move_to(plane.c2p(5,4)))
            self.play(
                ReplacementTransform(if_r_greater_q_rq, if_r_greater_q_nabla),
                ReplacementTransform(if_r_less_q_rq, if_r_less_q_nabla),
                Uncreate(rq_difference_value)
            )
            self.next_section(skip_animations=True)
            self.play(
                Write(rq_difference_nabla),
                if_r_greater_q_sign_change.animate.next_to(if_r_greater_q_nabla, buff=0.05),
                if_r_less_q_sign.animate.next_to(if_r_less_q_nabla, buff=0.05)
            )
            self.play(
                if_r_greater_q_move.animate.next_to(if_r_greater_q_sign_change, buff=0.05),
                if_r_less_q_move.animate.next_to(if_r_less_q_sign, buff=0.05),
                rq_difference_nabla.animate.next_to(rq_difference_equals, LEFT, buff=0.05),
                rq_difference_label.animate.next_to(rq_difference_equals, RIGHT, buff=0.05),
            )
            '''
            Note: the movements in the following self.play() are heavily based on the ideas explained previously in the code regarding
            the animation of coordinates that comes a bit later in the animation.
            Here the movements are also based on an anchor, only now this anchor is the curly brace. For example, for the '>=' sign the instructions look something like this:

            {                           nabla                                           >= 0 -> diagonally
            |fraction_offset/2 ->|length(nabla) ->|fraction_offset/2 ->|length('>=')/2 ->|
            
            It is important to note, however, that only the x-coordinate (or a-coordinate, doesn't really matter in this context) changes in such a way, the y and the z are not changed.
            '''
            self.play(
                rq_difference_label.animate.move_to([
                    rq_difference_label.get_center()[0],
                    rq_difference_label.get_center()[1] - 0.01, # Nudge for aesthetic reasons, without it r-q is a not in center
                    rq_difference_label.get_center()[2]
                ]),
                FadeOut(if_r_greater_q_if),
                FadeOut(if_r_less_q_if),
                FadeOut(if_r_greater_q_move_move),
                FadeOut(if_r_less_q_move_move),
                if_r_greater_q_nabla.animate.move_to([
                    curly_brace_if_r.get_right()[0] + get_len(if_r_greater_q_nabla)/2,
                    if_r_greater_q_nabla.get_center()[1], if_r_greater_q_nabla.get_center()[2]
                ]),
                if_r_less_q_nabla.animate.move_to([
                    curly_brace_if_r.get_right()[0] + get_len(if_r_greater_q_nabla)/2,
                    if_r_less_q_nabla.get_center()[1], if_r_less_q_nabla.get_center()[2]
                ]),
                if_r_greater_q_sign_change.animate.move_to([
                    curly_brace_if_r.get_right()[0] + get_len(if_r_greater_q_nabla) + fraction_offset + get_len(if_r_greater_q_sign_change)/2,
                    if_r_greater_q_sign_change.get_center()[1], if_r_greater_q_sign_change.get_center()[2]
                ]),
                if_r_less_q_sign.animate.move_to([
                    curly_brace_if_r.get_right()[0] + get_len(if_r_less_q_nabla) + fraction_offset + get_len(if_r_less_q_sign)/2,
                    if_r_less_q_sign.get_center()[1], if_r_less_q_sign.get_center()[2]
                ]),
                if_r_greater_q_move_arrow.animate.move_to([
                    curly_brace_if_r.get_right()[0] + get_len(if_r_greater_q_nabla) + 2*fraction_offset + get_len(if_r_greater_q_sign_change) + get_len(if_r_greater_q_move_arrow)/2,
                    if_r_greater_q_move_arrow.get_center()[1], if_r_greater_q_move_arrow.get_center()[2]
                ]),
                if_r_greater_q_move_diagonally.animate.move_to([
                    curly_brace_if_r.get_right()[0] + get_len(if_r_greater_q_nabla) + 3*fraction_offset + get_len(if_r_greater_q_sign_change) + get_len(if_r_greater_q_move_arrow) + get_len(if_r_greater_q_move_diagonally)/2,
                    if_r_greater_q_move_diagonally.get_center()[1], if_r_greater_q_move_diagonally.get_center()[2]
                ]),
                if_r_less_q_move_arrow.animate.move_to([
                    curly_brace_if_r.get_right()[0] + get_len(if_r_less_q_nabla) + 2*fraction_offset + get_len(if_r_less_q_sign) + get_len(if_r_less_q_move_arrow)/2,
                    if_r_less_q_move_arrow.get_center()[1], if_r_less_q_move_arrow.get_center()[2]
                ]),
                if_r_less_q_move_horizontally.animate.move_to([
                    curly_brace_if_r.get_right()[0] + get_len(if_r_less_q_nabla) + 3*fraction_offset + get_len(if_r_less_q_sign) + get_len(if_r_less_q_move_arrow) + get_len(if_r_less_q_move_horizontally)/2,
                    if_r_less_q_move_horizontally.get_center()[1], if_r_less_q_move_horizontally.get_center()[2]
                ]),

            )

            # Transitioning to Scene 4:
            self.play(
                Unwrite(r_len_text),
                Unwrite(q_len_text),
                Uncreate(text_rectangle),
                rq_nabla_temp_group.animate.move_to(rq_nabla_coords),
                Create(rq_nabla_rectangle),
                if_nabla_move_group.animate.move_to([
                    rq_nabla_coords[0] - get_len(rq_nabla_rectangle_group)/2 + get_len(if_nabla_move_group)/2,
                    rq_nabla_coords[1] - get_height(rq_nabla_rectangle_group)/2 - get_height(if_nabla_move_group)/2,
                    rq_nabla_coords[2]
                ]),
            )

            rq_nabla_rectangle_group.move_to([
                rq_nabla_temp_group.get_center()[0] - 0.005, # Same logic for the nudge as the previous nudge - aesthetic reasons
                rq_nabla_temp_group.get_center()[1] + 0.005,
                rq_nabla_temp_group.get_center()[2]
            ])

            self.play(Create(rq_nabla_expression), run_time=0.5)
            shift_value = LEFT * 1.225
            scale_value = 0.7
            self.play(
                self.camera.frame.animate.shift(shift_value).scale(scale_value),
                rq_nabla_group.animate.shift(shift_value).shift((scale_value + 0.2) * RIGHT).shift(1/np.sqrt(2) * scale_value * DOWN), # Got from trial and error
                if_nabla_move_group.animate.shift(shift_value).shift((scale_value) * RIGHT).shift(1/np.sqrt(2) * (scale_value - 0.045) * DOWN).scale(scale_value), # Also trial and error :(
                runtime = 1
            )

            self.wait(1)
            #                                                                  Fourth Scene                                                                                    #
            self.play(Create(lower_angle), Create(upper_angle))
            self.wait(0.7)
            s_name.clear_updaters()
            self.play(
                s_name.animate.shift(RIGHT * 0.1),
                Create(unnecessary_smaller_angle_right),
                Create(unnecessary_smaller_angle_left),
                Create(unnecessary_bigger_angle_right),
                Create(unnecessary_bigger_angle_left),
                runtime = 0.4
            )
            self.wait(2)
            self.play(
                s_name.animate.shift(LEFT * 0.1),
                Uncreate(unnecessary_smaller_angle_right),
                Uncreate(unnecessary_smaller_angle_left),
                Uncreate(unnecessary_bigger_angle_right),
                Uncreate(unnecessary_bigger_angle_left),
                runtime = 0.5
            )
            self.next_section(skip_animations=True)

            self.play(Write(angle_label_group))
            self.wait(1)
            shift_value = 1
            self.play(
                self.camera.frame.animate.shift(shift_value * RIGHT),
                rq_nabla_group.animate.shift(shift_value * RIGHT),
                if_nabla_move_group.animate.shift(shift_value * RIGHT),
                ReplacementTransform(angle_label_group, alpha_is_beta)
            )
            self.wait(1)
            self.play(
                beta_text.animate(run_time=0.7, rate_func=smooth).move_to([
                    beta_text.get_center()[0] + get_len(beta_sine_sine),
                    beta_text.get_center()[1],
                    beta_text.get_center()[2],
                ]),
                Create(alpha_sine_sine, run_time=0.7),
                Create(beta_sine_sine, run_time=0.7)
            )
            self.wait(1)
            self.play(
                ReplacementTransform(alpha_sine, r_rs_group),
                ReplacementTransform(beta_sine, q_qs_group)
            )
            self.wait(0.5)
            self.play(
                FadeOut(r_rs_fraction_line),
                FadeOut(q_qs_fraction_line),
                r_fraction_text.animate.move_to([
                    r_qs_multiplication.get_left()[0] - get_len(r_fraction_text)/2 - fraction_offset/2,
                    equals_text.get_center()[1], r_fraction_text.get_center()[2]
                ]),
                q_fraction_text.animate.move_to([
                    equals_text.get_right()[0] + get_len(q_fraction_text)/2 + fraction_offset/2,
                    equals_text.get_center()[1], q_fraction_text.get_center()[2]
                ]),
                rs_fraction_text.animate.move_to([
                    q_rs_multiplication.get_right()[0] + get_len(rs_fraction_text)/2 + fraction_offset/2,
                    equals_text.get_center()[1], rs_fraction_text.get_center()[2]
                ]),
                qs_fraction_text.animate.move_to([
                    equals_text.get_left()[0] - get_len(qs_fraction_text)/2 - fraction_offset/2,
                    equals_text.get_center()[1], qs_fraction_text.get_center()[2]
                ]),
                FadeIn(r_qs_multiplication),
                FadeIn(q_rs_multiplication)
            )
            self.wait(0.5)
            self.play(
                FadeOut(r_qs_multiplication),
                q_rs_group.animate.move_to([
                    q_rs_group.get_center()[0],
                    q_rs_fraction_line.get_top()[1] + get_height(rs_fraction_text)/2 + fraction_offset/2,
                    q_rs_group.get_center()[2]
                ]),
                Create(q_rs_fraction_line),
                qs_fraction_text.animate.move_to([
                    q_rs_fraction_line.get_center()[0],
                    q_rs_fraction_line.get_bottom()[1] - get_height(qs_fraction_text)/2 - fraction_offset/2,
                    qs_fraction_text.get_center()[2]
                ]),
                r_fraction_text.animate.move_to([
                    equals_text.get_left()[0] - get_len(r_fraction_text) - fraction_offset/2,
                    r_fraction_text.get_center()[1], r_fraction_text.get_center()[2]
                ])
            )
            self.wait(0.5)
            self.play(
                r_fraction_text.animate.move_to([
                    r_q_fraction_line.get_center()[0],
                    r_q_fraction_line.get_top()[1] + get_height(r_fraction_text)/2 + fraction_offset/2,
                    r_fraction_text.get_center()[2]
                ]),
                Create(r_q_fraction_line),
                FadeOut(q_rs_multiplication),
                q_fraction_text.animate.move_to([
                    r_q_fraction_line.get_center()[0],
                    r_q_fraction_line.get_bottom()[1] - get_height(q_fraction_text)/2 - fraction_offset/2,
                    q_fraction_text.get_center()[2]
                ]),
                ReplacementTransform(q_rs_fraction_line, rs_qs_fraction_line),
                rs_fraction_text.animate.move_to([rs_qs_fraction_line.get_center()[0], rs_fraction_text.get_center()[1], rs_fraction_text.get_center()[2]]),
                qs_fraction_text.animate.move_to([rs_qs_fraction_line.get_center()[0], qs_fraction_text.get_center()[1], qs_fraction_text.get_center()[2]]),
            )
            self.wait(1)
            self.play(
                Write(r_prime_label),
                Write(q_prime_label),
                ReplacementTransform(rs_fraction_text, r_prime_text),
                ReplacementTransform(qs_fraction_text, q_prime_text),
                ReplacementTransform(rs_qs_fraction_line, r_prime_q_fraction_line),
                r_q_fraction_line.animate.put_start_and_end_on([
                    r_q_fraction_line.get_end()[0] - get_len(r_prime_q_fraction_line),
                    equals_text.get_center()[1],
                    equals_text.get_center()[2]
                ], r_q_fraction_line.get_end()
                ),
                q_fraction_text.animate.move_to([
                    r_q_fraction_line.get_end()[0] - get_len(r_prime_q_fraction_line)/2,
                    q_prime_text.get_bottom()[1] + (q_fraction_text.get_top()[1] - q_fraction_text.get_bottom()[1])/2,
                    q_fraction_text.get_center()[2]
                ]),
                r_fraction_text.animate.move_to([
                    r_q_fraction_line.get_end()[0] - get_len(r_prime_q_fraction_line)/2,
                    r_prime_text.get_bottom()[1] + get_height(r_fraction_text)/2,
                    r_fraction_text.get_center()[2]
                ])
            )
            self.next_section(skip_animations=True)
            self.wait()

            self.play(
                self.camera.frame.animate.shift(shift_value * LEFT),
                rq_nabla_group.animate.shift(shift_value * LEFT),
                if_nabla_move_group.animate.shift(shift_value * LEFT),
            )
            # P(???, ???), Q(???, ???), R(???, ???):
            self.play(
                p_name.animate.move_to(p_name_coords),
                q_name.animate.move_to(q_name_coords),
                r_name.animate.move_to(r_name_coords),
                Create(p_name_group),
                Create(q_name_group),
                Create(r_name_group),
                Create(p_name_rectangle),
                Create(q_name_rectangle),
                Create(r_name_rectangle)
            )
            self.wait()
            # P(a1, b1), Q(???, ???), R(???, ???):
            self.play(
                FadeOut(p_name_question_x),
                FadeOut(p_name_question_y),
                Write(p_name_x),
                Write(p_name_y),
                p_name.animate.move_to([
                    p_dot.get_center()[0] - p_name_length/2 + get_len(p_name)/2,
                    p_name.get_center()[1],
                    p_name.get_center()[2]
                ]),
                p_name_open_brace.animate.move_to([
                    p_dot.get_center()[0] - p_name_length/2 + get_len(p_name) + fraction_offset/2 + get_len(p_name_open_brace)/2,
                    p_name_open_brace.get_center()[1], p_name_open_brace.get_center()[2]
                ]),
                p_name_close_brace.animate.move_to([
                    p_dot.get_center()[0] + p_name_length/2 - get_len(p_name_close_brace)/2,
                    p_name_close_brace.get_center()[1], p_name_close_brace.get_center()[2]
                ]),
                p_name_coma.animate.move_to([
                    p_dot.get_center()[0] + p_name_length/2 - get_len(p_name_close_brace) - get_len(p_name_y) - get_len(p_name_coma)/2 - 1.5*fraction_offset,
                    p_name_coma.get_center()[1], p_name_coma.get_center()[2]
                ]),
            )
            self.wait(1)
            # Arrow for clarifying script:
            self.play(Create(p_r_arrow), Write(p_r_arrow_label))
            p_r_arrow_label.add_updater(lambda label: label.next_to(p_r_arrow, UP, buff=0.00625))
            self.play(
                p_r_arrow.animate.move_to([p_r_arrow.get_center()[0], q_dot.get_center()[1], p_r_arrow.get_center()[2]])
            )
            p_r_arrow_label.clear_updaters()
            self.play(Uncreate(p_r_arrow), FadeOut(p_r_arrow_label))
            self.wait(1)

            # P(a1, b1), Q(a1+1, ???), R(a1+1, ???):
            self.play(
                # Q:
                Write(q_name_x),
                FadeOut(q_name_question_x),
                q_name.animate.move_to([
                    q_dot.get_center()[0] - q_name_first_length/2 + get_len(q_name)/2,
                    q_name.get_center()[1],
                    q_name.get_center()[2]
                ]),
                q_name_open_brace.animate.move_to([
                    q_dot.get_center()[0] - q_name_first_length/2 + get_len(q_name) + fraction_offset/2 + get_len(q_name_open_brace)/2,
                    q_name_open_brace.get_center()[1], q_name_open_brace.get_center()[2]
                ]),
                q_name_close_brace.animate.move_to([
                    q_dot.get_center()[0] + q_name_first_length/2 - get_len(q_name_close_brace)/2,
                    q_name_close_brace.get_center()[1], q_name_close_brace.get_center()[2]
                ]),
                q_name_coma.animate.move_to([
                    q_dot.get_center()[0] + q_name_first_length/2 - get_len(q_name_close_brace) - get_len(q_name_question_y) - get_len(q_name_coma)/2 - 2*fraction_offset,
                    q_name_coma.get_center()[1], q_name_coma.get_center()[2]
                ]),
                q_name_question_y.animate.move_to([
                    q_dot.get_center()[0] + q_name_first_length/2 - get_len(q_name_close_brace) - fraction_offset/2 - get_len(q_name_question_y)/2,
                    q_name_question_y.get_center()[1], q_name_question_y.get_center()[2]
                ]),
                # R:
                Write(r_name_x),
                FadeOut(r_name_question_x),
                r_name.animate.move_to([
                    r_dot.get_center()[0] - r_name_first_length/2 + get_len(r_name)/2,
                    r_name.get_center()[1],
                    r_name.get_center()[2]
                ]),
                r_name_open_brace.animate.move_to([
                    r_dot.get_center()[0] - r_name_first_length/2 + get_len(r_name) + fraction_offset/2 + get_len(r_name_open_brace)/2,
                    r_name_open_brace.get_center()[1], r_name_open_brace.get_center()[2]
                ]),
                r_name_close_brace.animate.move_to([
                    r_dot.get_center()[0] + r_name_first_length/2 - get_len(r_name_close_brace)/2,
                    r_name_close_brace.get_center()[1], r_name_close_brace.get_center()[2]
                ]),
                r_name_coma.animate.move_to([
                    r_dot.get_center()[0] + r_name_first_length/2 - get_len(r_name_close_brace) - get_len(r_name_question_y) - get_len(r_name_coma)/2 - 2*fraction_offset,
                    r_name_coma.get_center()[1], r_name_coma.get_center()[2]
                ]),
                r_name_question_y.animate.move_to([
                    r_dot.get_center()[0] + r_name_first_length/2 - get_len(r_name_close_brace) - fraction_offset/2 - get_len(r_name_question_y)/2,
                    r_name_question_y.get_center()[1], r_name_question_y.get_center()[2]
                ]),
            )
            self.wait(1)
            # P(a1, b1), Q(a1+1, b1+1), R(a1+1, b1):
            self.play(
                # Q:
                Write(q_name_y),
                FadeOut(q_name_question_y),
                q_name.animate.move_to([
                    q_dot.get_center()[0] - q_name_second_length/2 + get_len(q_name)/2,
                    q_name.get_center()[1],
                    q_name.get_center()[2]
                ]),
                q_name_open_brace.animate.move_to([
                    q_dot.get_center()[0] - q_name_second_length/2 + get_len(q_name) + fraction_offset/2 + get_len(q_name_open_brace)/2,
                    q_name_open_brace.get_center()[1], q_name_open_brace.get_center()[2]
                ]),
                q_name_close_brace.animate.move_to([
                    q_dot.get_center()[0] + q_name_second_length/2 - get_len(q_name_close_brace)/2,
                    q_name_close_brace.get_center()[1], q_name_close_brace.get_center()[2]
                ]),
                q_name_coma.animate.move_to([
                    q_dot.get_center()[0] + q_name_second_length/2 - get_len(q_name_close_brace) - get_len(q_name_y) - get_len(q_name_coma)/2 - 1.5*fraction_offset,
                    q_name_coma.get_center()[1], q_name_coma.get_center()[2]
                ]),
                q_name_x.animate.move_to([
                    q_dot.get_center()[0] - q_name_second_length/2 + get_len(q_name_open_brace) + get_len(q_name) + get_len(q_name_x)/2 + fraction_offset,
                    q_name_x.get_center()[1], q_name_x.get_center()[2]
                ]),
                # R:
                Write(r_name_y),
                FadeOut(r_name_question_y),
                r_name.animate.move_to([
                    r_dot.get_center()[0] - r_name_second_length/2 + get_len(r_name)/2,
                    r_name.get_center()[1],
                    r_name.get_center()[2]
                ]),
                r_name_open_brace.animate.move_to([
                    r_dot.get_center()[0] - r_name_second_length/2 + get_len(r_name) + fraction_offset/2 + get_len(r_name_open_brace)/2,
                    r_name_open_brace.get_center()[1], r_name_open_brace.get_center()[2]
                ]),
                r_name_close_brace.animate.move_to([
                    r_dot.get_center()[0] + r_name_second_length/2 - get_len(r_name_close_brace)/2,
                    r_name_close_brace.get_center()[1], r_name_close_brace.get_center()[2]
                ]),
                r_name_coma.animate.move_to([
                    r_dot.get_center()[0] + r_name_second_length/2 - get_len(r_name_close_brace) - get_len(r_name_y) - get_len(r_name_coma)/2 - 1.5*fraction_offset,
                    r_name_coma.get_center()[1], r_name_coma.get_center()[2]
                ]),
                r_name_x.animate.move_to([
                    r_dot.get_center()[0] - r_name_second_length/2 + get_len(r_name_open_brace) + get_len(r_name) + get_len(r_name_x)/2 + fraction_offset,
                    r_name_x.get_center()[1], r_name_x.get_center()[2]
                ]),
            )
            self.next_section(skip_animations=True)
            self.wait(1)
            # S(???, ???):
            self.play(FadeIn(s_name_group))
            self.wait(1)
            '''
            Similar thing happening here as with other points, but here the anchor is s_name, which means that open_brace is also called as an anchor,
            as well as s_name_x because both of the mobjects don't move after they have been called
            '''
            # S(a1+1, ???):
            self.play(
                FadeOut(s_name_question_x),
                Write(s_name_x),
                s_name_coma.animate.move_to([
                    s_name_x.get_right()[0] + fraction_offset/2 + get_len(s_name_coma)/2,
                    s_name_coma.get_center()[1], s_name_coma.get_center()[2]
                ]),
                s_name_question_y.animate.move_to([
                    s_name_x.get_right()[0] + 2*fraction_offset + get_len(s_name_coma) + get_len(s_name_question_y)/2,
                    s_name_question_y.get_center()[1], s_name_question_y.get_center()[2] 
                ]),
                s_name_close_brace.animate.move_to([
                    s_name_x.get_right()[0] + 2.5*fraction_offset + get_len(s_name_coma) + get_len(s_name_question_y) + get_len(s_name_close_brace)/2,
                    s_name_close_brace.get_center()[1], s_name_close_brace.get_center()[2]
                ])
            )
            # Removing the clutter on the screen for the explanation:
            active_mobjects_group.clear_updaters()
            self.camera.frame.save_state()
            self.play(FadeOut(removal_group), FadeOut(removed_group), returning_mobjects_group.animate.set_opacity(0.0))
            self.wait(1)
            self.play(self.camera.frame.animate.shift(RIGHT * 1.45))
            self.play(Write(b_equation))
            # First transform:
            self.play(
                FadeOut(b_equation_m),
                b_equation_delta.animate.next_to(b_equation_equals, buff=fraction_offset/2),
                FadeOut(b_equation_m_m),
                FadeOut(b_equation_m_equals),
                FadeIn(b_equation_times),
                b_equation_a.animate.next_to(b_equation_times, buff=fraction_offset/2)
            )
            self.play(b_second_equation.animate.move_to([b_equation_start_coords]))
            self.wait(1)
            # Parameters for wiggle:
            scaling_value = 1.5
            number_wiggles = 15
            angle_wiggle = 0.25
            wiggle_runtime = 3
            # First wiggle:
            self.play(
                Wiggle(b_equation_a, scale_value=scaling_value, n_wiggles=number_wiggles, rotation_angle=angle_wiggle, run_time=wiggle_runtime),
                Wiggle(s_name_x, scale_value=scaling_value-0.25, n_wiggles=number_wiggles, rotation_angle=angle_wiggle-0.2, run_time=wiggle_runtime)
            )
            self.wait(1)
            # Second wiggle:
            self.play(
                Wiggle(b_equation_b, scale_value=scaling_value, n_wiggles=number_wiggles, rotation_angle=angle_wiggle, run_time=wiggle_runtime),
                Wiggle(s_name_question_y, scale_value=scaling_value-0.25, n_wiggles=number_wiggles, rotation_angle=angle_wiggle, run_time=wiggle_runtime)
            )
            self.wait(1)
            # Second transform:
            b_equation_question.move_to(s_name_question_y.get_center())
            b_equation_open_brace.next_to(b_equation_times, RIGHT, buff=fraction_offset/2)
            b_equation_close_brace.next_to(b_equation_open_brace, RIGHT, buff= fraction_offset + get_len(b_equation_a1))
            b_equation_rectangle.next_to(b_equation_open_brace, RIGHT, buff= fraction_offset + get_len(b_equation_a1)/2)
            self.add(b_equation_question, b_equation_a1)
            self.play(
                FadeOut(b_equation_b),
                b_equation_question.animate.next_to(b_equation_equals, LEFT, buff=fraction_offset/2),
                FadeOut(b_equation_a),
                b_equation_a1.animate.next_to(b_equation_open_brace, RIGHT, buff=fraction_offset/2),
                Write(b_equation_open_brace),
                Write(b_equation_close_brace),
                FadeIn(b_equation_rectangle)
            )
            self.wait(1)
            # S (a1+1, deltaB/deltaA*(a1+1)):
            s_name_rectangle.next_to(s_name_x, RIGHT)
            self.play(
                FadeOut(b_equation_equals),
                FadeOut(b_equation_question),
                FadeOut(s_name_question_y),
                FadeOut(b_equation_rectangle),
                b_third_equation.animate.next_to(s_name_x, RIGHT, buff = get_len(s_name_coma) + 2*fraction_offset),
                s_name_close_brace.animate.next_to(s_name_x, RIGHT, buff = get_len(s_name_coma) + get_len(b_third_equation) + 2.5*fraction_offset),
                FadeIn(s_name_rectangle)
            )
            self.next_section(skip_animations=True)
            self.wait(1)
            # Restoring everything back to 'normal' - even though the mobjects in animation_group are not responding anymore :(
            self.play(Restore(self.camera.frame))
            self.play(FadeIn(removal_group), returning_mobjects_group.animate.set_opacity(1.0))
            self.wait(1)
            r_prime_label.save_state()
            q_prime_label.save_state()
            self.play(
                FadeIn(q_prime_brace),
                FadeIn(r_prime_brace),
                r_prime_label.animate.shift([(get_len(r_prime_brace) + fraction_offset/2), 0, 0]),
                q_prime_label.animate.shift([-(get_len(q_prime_brace) + fraction_offset), 0, 0])
            )
            self.wait(1)
            self.play(
                q_prime_label.animate.shift([-(get_len(q_prime_equation) + fraction_offset/2), 0, 0]),
                Write(r_prime_equation),
                Create(r_prime_equation_rectangle, run_time=2.0),
                Write(q_prime_equation),
                Create(q_prime_equation_rectangle, run_time=2.0)
            )
            self.wait(1)
            self.play(
                Uncreate(q_prime_equation_rectangle),
                Uncreate(r_prime_equation_rectangle),
                Restore(r_prime_label),
                Restore(q_prime_label),
                FadeOut(r_prime_equation),
                FadeOut(q_prime_equation),
                FadeOut(q_prime_brace),
                FadeOut(r_prime_brace)
            )
            '''
            NOTE FOR THE VIDEO EDITING:
            '''

            self.play(
                FadeOut(b_equation_1),
                FadeOut(b_equation_2),
            )
            self.next_section(skip_animations=True)
            self.wait(1)
            shift_value = DOWN * 10
            self.play(self.camera.frame.animate.shift(shift_value))




        def interpolate_y_on_line(self, line, x_value, plane):
            start = line.get_start()
            end = line.get_end()
            start_coords = plane.p2c(start)
            end_coords = plane.p2c(end)
            if end_coords[0] - start_coords[0] == 0:
                return start_coords[1]
            t = (x_value - start_coords[0]) / (end_coords[0] - start_coords[0])
            return (1 - t) * start_coords[1] + t * end_coords[1]


class FifthScene(MovingCameraScene):
    def construct(self):
        text_size = 44
        text_buff = 0.25

        #q_prime_equation = Tex(r"$\boldsymbol{q' = b_1 + 1 - \frac{\Delta b}{\Delta a}(a_1 + 1)}$", font_size = text_size)

        q_prime = Tex(r"$\boldsymbol{q' =}$", font_size = text_size)
        q_prime_before_minus = Tex(r"$\boldsymbol{b_1 + 1}$", font_size = text_size)
        q_prime_minus = Tex(r"$\boldsymbol{-}$", font_size = text_size)
        q_prime_after_minus = Tex(r"$\boldsymbol{\frac{\Delta b}{\Delta a}(a_1 + 1)}$", font_size = text_size)
        q_prime_equation = VGroup(q_prime, q_prime_before_minus, q_prime_minus, q_prime_after_minus).arrange(RIGHT, buff=text_buff)
        # q_prime_equation.move_to([self.camera.frame.get_center()[0], self.camera.frame.get_top()[1] - get_height(q_prime_equation), 0])
    
        #curly brackets <3 (q)
        q_prime_bracket_down = Brace(q_prime_before_minus, sharpness=1.0, color = BLUE)
        q_prime_bottom_text = Tex(r"$\textbf{Q vertical coordinate}$", font_size = text_size, color = BLUE)

        q_prime_bracket_up = Brace(q_prime_after_minus, sharpness=1.0, color = GREEN).rotate(PI)
        q_prime_up_text = Tex(r"$\textbf{S vertical coordinate}$", font_size = text_size, color = GREEN)

        # R:
        r_prime = Tex(r"$\boldsymbol{r' =}$", font_size = text_size)
        r_prime_before_minus = q_prime_after_minus.copy()
        r_prime_minus = Tex(r"$\boldsymbol{-}$", font_size = text_size)
        r_prime_after_minus = Tex(r"$\boldsymbol{b_1}$", font_size = text_size)
        r_prime_equation = VGroup(r_prime, r_prime_before_minus, r_prime_minus, r_prime_after_minus).arrange(RIGHT, buff=text_buff)

        #curly brackets <3 (r)
        r_prime_bracket_down = Brace(r_prime_before_minus, sharpness=1.0, color = GREEN)
        r_prime_bottom_text = Tex(r"$\textbf{S vertical coordinate}$", font_size = text_size, color = GREEN)

        r_prime_bracket_up = Brace(r_prime_after_minus, sharpness=1.0, color = RED).rotate(PI)
        r_prime_up_text = Tex(r"$\textbf{R vertical coordinate}$", font_size = text_size, color = RED)

        # Moving q and r to the top right of the screen
        prime_equations = VGroup(r_prime_equation, q_prime_equation)

        # r/q = r'/q'
        rq_identity = Tex(r"$\boldsymbol{\frac{r}{q}=\frac{r'}{q'}}$", font_size=text_size*4/3)
        rq_identity.move_to([
            self.camera.frame.get_left()[0],
            self.camera.frame.get_top()[1] - 3/2*fraction_offset - get_height(r_prime_equation) - get_height(q_prime_equation) - get_height(rq_identity)/2,
            rq_identity.get_center()[2]
        ])
        # Shifting out of sight:
        rq_identity.shift([-get_len(rq_identity), 0, 0])
        
        # nabla = r-q
        nabla = Tex(r"$\boldsymbol{\nabla = }$", font_size=text_size*4/3)
        nabla_rq = Tex(r"$\boldsymbol{r-q}$", font_size=text_size*4/3)
        nabla_expression = VGroup(nabla, nabla_rq).arrange(RIGHT, buff=text_buff)
        nabla_rq.shift([0, -text_buff/3, 0])
        # Positioning:
        nabla_expression.move_to([
            self.camera.frame.get_right()[0] - get_len(nabla_expression)/2,
            self.camera.frame.get_top()[1] - get_height(nabla_expression)/2 - text_buff,
            nabla_expression.get_center()[2]
        ])

        # Condition with nabla:
        nabla_condition = Tex(r"$\boldsymbol{\begin{cases}\nabla\ge0\rightarrow diagonally\\\nabla<0\rightarrow horizontally\end{cases}}$", font_size=text_size)
        # Positioniing that sucker:
        nabla_condition.move_to([
            nabla_expression.get_right()[0] - get_len(nabla_condition)/2,
            nabla_expression.get_bottom()[1] - get_height(nabla_condition)/2 - fraction_offset,
            nabla_condition.get_center()[2]
        ])

        nabla_group = VGroup(nabla_expression, nabla_condition)
        # Shifting out of sight:
        nabla_group.shift([3/2*get_len(nabla_group), 0, 0])

        '''
        The idea here is that there is a system of conditions that change from instance to instance.
        First instance:
            Nabla >= 0 if r-q >= 0
            Nabla < 0 if r-q < 0

        Second instance:
            r-q >= 0 if r >= q
            r-q < 0 if r < q

        Afterwards the system moves to the right down besides the other conditional (maybe change this?)
        '''
        # First Instance:
        r_q_brace = Tex(r"$\begin{cases}\\\end{cases}$", font_size=4/3*text_size)
        # nabla >= 0 if r-q >= 0:
        r_q_nabla_bigger = Tex(r"$\boldsymbol{\nabla \ge 0}$", font_size=text_size)
        r_q_if_bigger = Tex(r"$\boldsymbol{if}$", font_size=text_size)
        r_q_zero_rq_bigger = Tex(r"$\boldsymbol{r-q}$", font_size=text_size)
        r_q_zero_zero_bigger = Tex(r"$\boldsymbol{\ge 0}$", font_size=text_size)
        r_q_zero_bigger = VGroup(r_q_zero_rq_bigger, r_q_zero_zero_bigger).arrange(RIGHT, buff=text_buff)
        r_q_bigger_first = VGroup(r_q_nabla_bigger, r_q_if_bigger, r_q_zero_bigger).arrange(RIGHT, buff=text_buff)
        
        # nabla < 0 if r-q < 0:
        r_q_nabla_smaller = Tex(r"$\boldsymbol{\nabla < 0}$", font_size=text_size)
        r_q_if_smaller = Tex(r"$\boldsymbol{if}$", font_size=text_size)
        r_q_zero_rq_smaller = Tex(r"$\boldsymbol{r-q}$", font_size=text_size)
        r_q_zero_zero_smaller = Tex(r"$\boldsymbol{< 0}$", font_size=text_size)
        r_q_zero_smaller = VGroup(r_q_zero_rq_smaller, r_q_zero_zero_smaller).arrange(RIGHT, buff=text_buff)
        r_q_smaller_first = VGroup(r_q_nabla_smaller, r_q_if_smaller, r_q_zero_smaller).arrange(RIGHT, buff=text_buff)

        # Arranging everything for the first time. Anchor: the brace, after which everything is centered
        r_q_bigger_first.next_to(r_q_brace, RIGHT, buff=text_buff/2)
        r_q_bigger_first.shift([0, get_height(r_q_brace)/4, 0])

        r_q_smaller_first.next_to(r_q_brace, RIGHT, buff=text_buff/2)
        r_q_smaller_first.shift([0, -get_height(r_q_brace)/4, 0])

        r_q_first_instance = VGroup(r_q_brace, r_q_bigger_first, r_q_smaller_first)
        r_q_first_instance.move_to(self.camera.frame.get_center())

        # Second instance
        # r - q >= 0 if r >= q:
        r_q_r_q_bigger = Tex(r"$\boldsymbol{r \ge q}$", font_size=text_size)
        r_q_bigger_second = VGroup(r_q_zero_bigger, r_q_if_bigger, r_q_r_q_bigger)


        # r - q < 0 if r < q:
        r_q_r_q_smaller = Tex(r"$\boldsymbol{r<q}$", font_size=text_size)
        r_q_smaller_second = VGroup(r_q_zero_smaller, r_q_if_smaller, r_q_r_q_smaller)

        r_q_second_instance = VGroup(r_q_brace, r_q_bigger_second, r_q_smaller_second)
        # Second condition
        '''
        The idea behind this one is as follows:
        First instance:
            r/q >= 1 if r >= q
            r/q < 1 if r < q
        
        Second instance:
            r/q - 1 >= 0 if r >= q
            r/q - 1 < 0 if r < q
        
        Third instance:
            r'/q' - 1 >= 0 if r >= q
            r'/q' - 1 < 0 if r < q
        
        (Here is should move to the left side and change there)
        After third instance in the center make the following equation (in a different set of variables):
        r'/q' - 1 = r'/q' - q'/q' = (r'-q')/q'

        Fourth instance:
            (r'-q')/q' >= 0 if r >= q
            (r'-q')/q' < 0 if r < q
        
        Fifth instance:
            r' - q' >= 0 if r >= q
            r' - q' >= q if r < q
        '''
        # First instance:
        r_div_brace = Tex(r"$\begin{cases}\\\end{cases}$", font_size=4/3*4/3*4/3*text_size)
        
        # r/q >= 1 if r >= q
        r_div_rq_bigger = Tex(r"$\boldsymbol{\frac{r}{q}}$", font_size=4/3*text_size)
        r_div_sign_bigger = Tex(r"$\boldsymbol{\ge}$", font_size=text_size)
        r_div_one_bigger = Tex(r"$\boldsymbol{1}$", font_size=text_size)
        r_div_if_bigger = Tex(r"$\boldsymbol{if \; r \ge q}$", font_size=text_size)
        
        r_div_bigger_first = VGroup(r_div_rq_bigger, r_div_sign_bigger, r_div_one_bigger, r_div_if_bigger).arrange(RIGHT, buff=text_buff)

        # r/q < 1 if r < q:
        r_div_rq_smaller = Tex(r"$\boldsymbol{\frac{r}{q}}$", font_size=4/3*text_size)
        r_div_sign_smaller = Tex(r"$\boldsymbol{<}$", font_size=text_size)
        r_div_one_smaller = Tex(r"$\boldsymbol{1}$", font_size=text_size)
        r_div_if_smaller = Tex(r"$\boldsymbol{if \; r<q}$", font_size=text_size)

        r_div_smaller_first = VGroup(r_div_rq_smaller, r_div_sign_smaller, r_div_one_smaller, r_div_if_smaller).arrange(RIGHT, buff=text_buff)

        # Aligning everything:
        r_div_bigger_first.next_to(r_div_brace, RIGHT, buff=text_buff/2)
        r_div_bigger_first.shift([0, get_height(r_div_brace)/4, 0])

        r_div_smaller_first.next_to(r_div_brace, RIGHT, buff=text_buff/2)
        r_div_smaller_first.shift([0, -get_height(r_div_brace)/4, 0])

        r_div_first = VGroup(r_div_bigger_first, r_div_smaller_first, r_div_brace)
        r_div_first.move_to(self.camera.frame.get_center())

        # Second instance:
        # r/q - 1 >= 0 if r >= q
        r_div_minus_bigger = Tex(r"$\boldsymbol{-}$", font_size=text_size)
        r_div_zero_bigger = Tex(r"$\boldsymbol{0}$", font_size=text_size)
        r_div_bigger_second = VGroup(r_div_rq_bigger, r_div_minus_bigger, r_div_one_bigger, r_div_sign_bigger, r_div_zero_bigger, r_div_if_bigger)

        # r/q - 1 < 0 if r < q
        r_div_minus_smaller = Tex(r"$\boldsymbol{-}$", font_size=text_size)
        r_div_zero_smaller = Tex(r"$\boldsymbol{0}$", font_size=text_size)
        r_div_smaller_second = VGroup(r_div_rq_smaller, r_div_minus_smaller, r_div_one_smaller, r_div_sign_smaller, r_div_zero_smaller, r_div_if_smaller)

        # Positioning:
        r_div_minus_bigger.next_to(r_div_rq_bigger, RIGHT, buff=text_buff)
        r_div_minus_smaller.next_to(r_div_rq_smaller, RIGHT, buff=text_buff)

        r_div_second = VGroup(r_div_bigger_second, r_div_smaller_second, r_div_brace)

        # Third instance:
        # r'/q' - 1 >= 0 if r >= q
        r_div_prime_bigger = Tex(r"$\boldsymbol{\frac{r'}{q'}}$", font_size=4/3*text_size)
        r_div_bigger_third = VGroup(r_div_prime_bigger, r_div_minus_bigger, r_div_one_bigger, r_div_sign_bigger, r_div_zero_bigger, r_div_if_bigger)
        r_div_replacement_group_bigger = VGroup(r_div_prime_bigger, r_div_minus_bigger, r_div_one_bigger)
        r_div_replacement_group_bigger_copy = r_div_replacement_group_bigger.copy()

        # r'/q' - 1 < 0 if r < q
        r_div_prime_smaller = Tex(r"$\boldsymbol{\frac{r'}{q'}}$", font_size=4/3*text_size)
        r_div_smaller_third = VGroup(r_div_prime_smaller, r_div_minus_smaller, r_div_one_smaller, r_div_sign_smaller, r_div_zero_smaller, r_div_if_smaller)
        r_div_replacement_group_smaller = VGroup(r_div_prime_smaller, r_div_minus_smaller, r_div_one_smaller)

        r_div_third = VGroup(r_div_bigger_third, r_div_smaller_third, r_div_brace)
        
        # Break for an equation:
        '''
        Reminder: this is how the equation should look like:
        r'/q' - 1 = r'/q' - q'/q' = (r'-q')/q'   
        '''
        r_eq_first = Tex(r"$\boldsymbol{\frac{r'}{q'}-1}$", font_size=4/3*text_size)
        r_eq_second = Tex(r"$\boldsymbol{=\frac{r'}{q'}-\frac{q'}{q'}}$", font_size=4/3*text_size)
        r_eq_equals = Tex(r"$\boldsymbol{=}$", font_size=4/3*text_size)

        r_eq_final_rq = Tex(r"$\boldsymbol{r'-q'}$", font_size=text_size)
        r_eq_final_q = Tex(r"$\boldsymbol{q'}$", font_size=text_size)
        r_eq_final_line = Line(start=ORIGIN, end=[fraction_offset*2 + get_len(r_eq_final_rq), 0, 0], color=WHITE, stroke_width=2)
        r_eq_final = VGroup(r_eq_final_rq, r_eq_final_line, r_eq_final_q).arrange(DOWN, buff=fraction_offset)

        r_eq_final_bottom_rq = Tex(r"$\boldsymbol{r'-q'}$", font_size=text_size)
        r_eq_final_bottom_q = Tex(r"$\boldsymbol{q'}$", font_size=text_size)
        r_eq_final_bottom_line = Line(start=ORIGIN, end=[fraction_offset*2 + get_len(r_eq_final_bottom_rq), 0, 0], color=WHITE, stroke_width=2)
        r_eq_final_bottom = VGroup(r_eq_final_bottom_rq, r_eq_final_bottom_line, r_eq_final_bottom_q).arrange(DOWN, buff=fraction_offset)

        r_eq_final_top_rq = Tex(r"$\boldsymbol{r'-q'}$", font_size=text_size)
        r_eq_final_top_q = Tex(r"$\boldsymbol{q'}$", font_size=text_size)
        r_eq_final_top_line = Line(start=ORIGIN, end=[fraction_offset*2 + get_len(r_eq_final_top_rq), 0, 0], color=WHITE, stroke_width=2)
        r_eq_final_top = VGroup(r_eq_final_top_rq, r_eq_final_top_line, r_eq_final_top_q).arrange(DOWN, buff=fraction_offset)

        r_eq_first_group = VGroup(r_eq_first, r_eq_second)
        r_eq_group = VGroup(r_eq_first, r_eq_second, r_eq_equals, r_eq_final).arrange(RIGHT, buff=text_buff)

        # Sign:
        '''
        The equation has the following form:
        q>0 => Sign((r'-q')/q') = Sign(r'-q')
        '''
        r_sign_left = Tex(r"$\boldsymbol{\Rightarrow \textbf{Sign}(}$", font_size=text_size)
        q_bigger_than_zero = Tex(r"$\boldsymbol{q'>0}$", font_size=text_size)
        r_brace_left = Tex(r"$\boldsymbol{)=}$", font_size=text_size)
        r_sign_right = Tex(r"$\boldsymbol{\textbf{Sign}(}$", font_size=text_size)
        r_minus_q = Tex(r"$\boldsymbol{r'-q'}$", font_size=text_size)
        r_brace_right = Tex(r"$\boldsymbol{)}$", font_size=text_size)

        q_bigger_group = VGroup(r_sign_left, r_brace_left, r_sign_right, r_minus_q, r_brace_right)

        # Fourth instance:
        r_div_smaller_brace = r_q_brace.copy()
        r_div_fourth_bigger = VGroup(r_eq_final_top_rq, r_div_sign_bigger, r_div_zero_bigger, r_div_if_bigger)
        r_div_fourth_smaller = VGroup(r_eq_final_bottom_rq, r_div_sign_smaller, r_div_zero_smaller, r_div_if_smaller)

        r_div_fourth = VGroup(r_div_smaller_brace, r_div_fourth_bigger, r_div_fourth_smaller)

        # Nabla for comparison of r - q and r' - q':
        nabla_comparison_normal_top = Tex(r"$\boldsymbol{\nabla}$", font_size=text_size, color=ManimColor("#9059FF"))
        nabla_comparison_normal_bottom = nabla_comparison_normal_top.copy()

        nabla_comparison_prime_top = Tex(r"$\boldsymbol{\nabla ?}$", font_size=text_size, color=ManimColor("#FFF700"))
        nabla_comparison_prime_bottom = nabla_comparison_prime_top.copy()

        # Fifth instance:
        r_div_fifth_bigger = VGroup(r_div_sign_bigger, r_div_zero_bigger, r_div_if_bigger, nabla_comparison_prime_top)
        r_div_fifth_smaller = VGroup(r_div_sign_smaller, r_div_zero_smaller, r_div_if_smaller, nabla_comparison_prime_bottom)

        r_div_fifth = VGroup(r_div_fifth_bigger, r_div_fifth_smaller, r_div_smaller_brace)

        r_q_third_instance_bigger = VGroup(nabla_comparison_normal_top, r_q_zero_zero_bigger, r_q_if_bigger, r_q_r_q_bigger)
        r_q_third_instance_smaller = VGroup(nabla_comparison_normal_bottom, r_q_zero_zero_smaller, r_q_if_smaller, r_q_r_q_smaller)

        r_q_third_instance = VGroup(r_q_brace, r_q_third_instance_bigger, r_q_third_instance_smaller)
        
        #******************************************************Long equations simplification part******************************************************

        
        #new_nabla_rq.shift([0, -text_buff/3, 0])
        nabla_rq_prime = Tex(
            r"$\boldsymbol{r'}$", 
            r"$- $",  
            r"$\boldsymbol{q'}$", 
            font_size=text_size*4/3, color = ManimColor("#9059FF")
        )
        
        nabla_rq_equals = Tex(r"$\boldsymbol{\vphantom{\nabla} = }$", font_size=text_size*4/3, color = ManimColor("#9059FF"))
        new_nabla_expression = VGroup(nabla_rq_equals, nabla_rq_prime).arrange(RIGHT, buff=text_buff)

        r_prime_stuff_color = GREEN
        q_prime_stuff_color = BLUE_B

        brace_one = Tex(r"$\boldsymbol{(}$", font_size=text_size)
        r_prime_phantom = Tex(r"$\boldsymbol{\frac{\Delta b}{\Delta a}(a_1 + 1) - b_1}$", font_size=text_size)
        brace_two = Tex(r"$\boldsymbol{)}$", font_size=text_size)
        phantom_minus = Tex(r"$\boldsymbol{-}$", font_size=text_size)
        brace_three = brace_one.copy()
        q_prime_phantom = Tex(r"$\boldsymbol{b_1 + 1 - \frac{\Delta b}{\Delta a}(a_1 + 1)}$", font_size=text_size)
        brace_four = brace_two.copy()

        new_q_prime_before_equal = Tex(r"$\boldsymbol{q' = }$", font_size=text_size)
        new_q_prime_after_equal = q_prime_phantom.copy()
        new_q_prime = VGroup(new_q_prime_before_equal, new_q_prime_after_equal).arrange(RIGHT, buff=text_buff)

        new_r_prime_before_equal = Tex(r"$\boldsymbol{r' = }$", font_size=text_size)
        new_r_prime_after_equal = r_prime_phantom.copy()
        new_r_prime = VGroup(new_r_prime_before_equal, new_r_prime_after_equal).arrange(RIGHT, buff=text_buff)

        new_prime_equations = VGroup(new_r_prime, new_q_prime).arrange(DOWN, buff = text_buff).move_to(prime_equations.get_center())

        equal_before_phantom = Tex(r"$\boldsymbol{ = }$", font_size=text_size)
        equal_after_phantom = equal_before_phantom.copy()
        equal_after_phantom.add_updater(lambda x: x.next_to(equation_one, RIGHT * text_buff))
        equal_after_new_nabla = nabla_rq_equals.copy().set_color(WHITE)

        phantom_equation = VGroup(equal_before_phantom, brace_one, r_prime_phantom, brace_two, phantom_minus, brace_three, q_prime_phantom, brace_four, equal_after_phantom).arrange(RIGHT, buff=text_buff).move_to(self.camera.frame.get_center()).shift(DOWN * get_height(new_q_prime) * 1.4)

        #Those are anchors.
        row1 = Tex(r"$anchor$", font_size = text_size).move_to(self.camera.frame.get_center())
        row2 = Tex(r"$anchor$", font_size = text_size)
        row3 = Tex(r"$anchor$", font_size = text_size)
        row4 = Tex(r"$anchor$", font_size = text_size)

        rows = VGroup(row1, row2, row3, row4).arrange(UP, buff = 0.35) # change buff to set distance between equations

        #variable used with scale()
        shrink = 0.8

        #simplification steps
        equation_one = VGroup (brace_one, new_r_prime_after_equal, brace_two, phantom_minus, brace_three, new_q_prime_after_equal, brace_four)

        equation_two = Tex(r"$\boldsymbol{= \frac{\Delta b}{\Delta a}(a_1 + 1) - b_1 - b_1 - 1 + \frac{\Delta b}{\Delta a}(a_1 + 1)}$", font_size=text_size)

        equal_after_two = equal_before_phantom.copy()
        equal_after_two.add_updater(lambda x: x.next_to(equation_two, RIGHT * text_buff))

        equation_three = Tex(r"$\boldsymbol{= \frac{\Delta b}{\Delta a}(a_1 + 1) - \frac{b_1\Delta a}{\Delta a} - \frac{\Delta a}{\Delta a} + \frac{\Delta b}{\Delta a}(a_1 + 1)}$", font_size=text_size)

        equal_after_three = equal_before_phantom.copy()
        equal_after_three.add_updater(lambda x: x.next_to(equation_three, RIGHT * text_buff))

        equation_four = Tex(r"$\boldsymbol{= \frac{2\Delta b(a_1 + 1) - 2\Delta ab_1 - \Delta a}{\Delta a} }$", font_size=text_size)

        equal_after_four = equal_after_phantom.copy()
        equal_after_four.add_updater(lambda x: x.next_to(equation_four, RIGHT * text_buff))

        equal_before_five = Tex(r"$\boldsymbol{=}$", font_size=text_size)
        equation_five = Tex(r"$\boldsymbol{\frac{2a_1\Delta b + 2\Delta b - 2\Delta ab_1 -  \Delta a}{\Delta a} }$", font_size=text_size)
        
        equation_five_group = VGroup(equal_before_five, equation_five).arrange(RIGHT, buff = text_buff)


        #------ Делаем новую фантомную штуку ------

        # phantom final nabla Expression
        final_nabla_phantom = Tex(r"$\boldsymbol{\nabla}$", font_size=text_size)

        final_nabla_equals_phantom = Tex(r"$\boldsymbol{=}$", font_size=text_size)

        delta_a_1_phantom = Tex(r"$\boldsymbol{\Delta a}$", font_size=text_size)

        delta_bracket_1_phantom = Tex(r"$\boldsymbol{(}$", font_size=text_size).set_color(BLUE)

        new_rq_prime_phantom = Tex(r"$\boldsymbol{r'-q'}$", font_size=text_size)

        delta_bracket_2_phantom = Tex(r"$\boldsymbol{)}$", font_size=text_size).set_color(BLUE)

        phantom_final_nabla_group = VGroup( final_nabla_phantom, final_nabla_equals_phantom, new_rq_prime_phantom)
        phantom_final_nabla_group.set_color(GREEN)

        # phantom 5th equation 

        equal_before_five_phantom = final_nabla_equals_phantom.copy()


        delta_a_2_phantom = delta_a_1_phantom.copy()

        delta_bracket_3_phantom = delta_bracket_1_phantom.copy()

        equation_five_phantom = equation_five.copy() # Выглядит забавно, я знаю. Это чтобы не забыть порядок

        delta_bracket_4_phantom = delta_bracket_2_phantom.copy()

        phantom_delta_equation = VGroup(final_nabla_phantom, final_nabla_equals_phantom, delta_a_1_phantom, delta_bracket_1_phantom, new_rq_prime_phantom,  delta_bracket_2_phantom, equal_before_five_phantom, delta_a_2_phantom, delta_bracket_3_phantom, equation_five_phantom, delta_bracket_4_phantom).arrange(RIGHT, buff = text_buff)

        phantom_delta_equation.move_to(row2.get_center())

        #------ Теперь не фантомную штуку ------

        # final nabla Expression
        new_nabla = final_nabla_phantom.copy()

        new_nabla_equals = final_nabla_equals_phantom.copy()

        new_rq_prime = new_rq_prime_phantom.copy()

        final_nabla_expression = VGroup(new_nabla, new_nabla_equals, new_rq_prime).arrange(RIGHT, buff = text_buff)

        #final form

        
        equal_after_five = final_nabla_equals_phantom.copy()
        equal_before_final = final_nabla_equals_phantom.copy()
        final_form = Tex(r"$\boldsymbol{2a_1\Delta b + 2\Delta b - 2\Delta ab_1 -  \Delta a}$", font_size=3.5/4 * text_size)

        final_form_group = VGroup(equal_before_final, final_form).arrange(RIGHT, buff = text_buff)

        #**************************************************************Animation sextion***********************************************
        self.next_section(skip_animations=True)
        # self.camera.frame.scale(0.4) <- Not used
        self.play(Write(q_prime_equation))
        self.wait(1)
        self.play(FadeToColor(q_prime_before_minus, BLUE))
        self.wait(0.5)
        # Lower bracket:
        self.play(Write(q_prime_bracket_down.next_to(q_prime_before_minus, DOWN, buff=0.1)))
        self.play(Write(q_prime_bottom_text.next_to(q_prime_bracket_down, DOWN, buff=0.2)))
        self.wait(1)
        # Upper Bracket:
        self.play(FadeToColor(q_prime_after_minus, GREEN))
        self.play(
            Write(q_prime_bracket_up.next_to(q_prime_after_minus, UP, buff=0.1), runtime = 1.3),
            Write(q_prime_up_text.next_to(q_prime_bracket_up, UP, buff=0.2)),
        )
        self.wait(1)
        # Moving q to the top left corner:
        self.play(
            FadeOut(q_prime_bracket_down),
            FadeOut(q_prime_bottom_text),
            FadeOut(q_prime_bracket_up),
            FadeOut(q_prime_up_text),
            q_prime_equation.animate.move_to([
                self.camera.frame.get_left()[0] + get_len(q_prime_equation)/2 + fraction_offset*2,
                self.camera.frame.get_top()[1] - get_height(q_prime_equation)/2 - fraction_offset*2,
                q_prime_equation.get_center()[2]
            ])
        )
        # R:
        # Lower bracket:
        self.play(
            Write(r_prime_equation.move_to(self.camera.frame.get_center())),
            FadeToColor(q_prime_before_minus, WHITE), FadeToColor(q_prime_after_minus, WHITE), 
        )
        self.wait(1)
        self.play(FadeToColor(r_prime_before_minus, GREEN))
        self.wait(0.5)
        self.play(
            Write(r_prime_bracket_down.next_to(r_prime_before_minus, DOWN, buff=0.1), runtime = 1.3),
            Write(r_prime_bottom_text.next_to(r_prime_bracket_down, DOWN, buff=0.2)),
        )
        # Upper bracket:
        self.wait(1)
        self.play(FadeToColor(r_prime_after_minus, RED))
        self.play(
            Write(r_prime_bracket_up.next_to(r_prime_after_minus, UP, buff=0.1), runtime = 1.3),
            Write(r_prime_up_text.next_to(r_prime_bracket_up, UP, buff=0.2)),
        )
        # Moving r to the top left corner:
        self.play(
            FadeOut(r_prime_bracket_down),
            FadeOut(r_prime_bottom_text),
            FadeOut(r_prime_bracket_up),
            FadeOut(r_prime_up_text),
            r_prime_equation.animate.move_to([
                self.camera.frame.get_left()[0] + get_len(r_prime_equation)/2 + fraction_offset*2,
                self.camera.frame.get_top()[1] - get_height(q_prime_equation) - get_height(r_prime_equation)/2 - 3/2*fraction_offset,
                r_prime_equation.get_center()[2]
            ]),
        )

        # Moving r/q = r'/q' into sight and moving it on top:
        self.play(
            rq_identity.animate.shift([3/2*get_len(rq_identity) + text_buff, 0, 0]),
            FadeToColor(r_prime_after_minus, WHITE),
            FadeToColor(r_prime_before_minus, WHITE)
        )
        self.wait(1)
        self.play(
            rq_identity.animate.move_to([
                rq_identity.get_center()[0],
                self.camera.frame.get_top()[1] - get_height(rq_identity)/2 - text_buff/2,
                rq_identity.get_center()[2]
            ]),
            prime_equations.animate.move_to([
                prime_equations.get_center()[0] + text_buff/2,
                self.camera.frame.get_top()[1] - get_height(rq_identity) - text_buff - get_height(prime_equations)/2,
                prime_equations.get_center()[2]
            ])
        )
        self.wait(1)

        # Moving nabla and its condition into sight:
        self.play(
            nabla_group.animate.shift([-3/2*get_len(nabla_group) - text_buff, 0, 0]),
            prime_equations.animate.set_opacity(0.0)
        )
        self.wait(1)
        self.next_section(skip_animations=True)
        self.wait()
        # Wiggle 
        scaling_value = 1.2
        number_wiggles = 15
        angle_wiggle = 0.25
        wiggle_runtime = 1.5
        # First wiggle (r/q = r'/q'):
        self.play(FadeToColor(rq_identity, ManimColor("#FFF700")))
        self.play(Wiggle(rq_identity, scale_value=scaling_value, n_wiggles=number_wiggles, rotation_angle=angle_wiggle, run_time=wiggle_runtime))
        self.wait(1)

        # Second wiggle (nabla):
        self.play(FadeToColor(nabla_expression, ManimColor("#9059FF")))
        self.play(Wiggle(nabla_expression, scale_value=scaling_value, n_wiggles=number_wiggles, rotation_angle=angle_wiggle, run_time=wiggle_runtime))
        self.next_section(skip_animations=True)
        self.wait(1)
        # self.play(FadeToColor(rq_identity, WHITE), FadeToColor(nabla_expression, WHITE))

        # First instance of the conditional:
        nabla_condition_copy = nabla_condition.copy()
        self.add(nabla_condition_copy)
        self.play(ReplacementTransform(nabla_condition, r_q_first_instance))
        self.wait(1)

        # Transitioning into second instance:
        self.play(
            FadeOut(r_q_nabla_bigger),
            r_q_zero_bigger.animate.move_to([
                r_q_brace.get_right()[0] + text_buff/2 + get_len(r_q_zero_bigger)/2,
                r_q_zero_bigger.get_center()[1], r_q_zero_bigger.get_center()[2]
            ]),
            FadeOut(r_q_nabla_smaller),
            r_q_zero_smaller.animate.move_to([
                r_q_brace.get_right()[0] + text_buff/2 + get_len(r_q_zero_smaller)/2,
                r_q_zero_smaller.get_center()[1], r_q_zero_smaller.get_center()[2]
            ]),
            Write(r_q_r_q_bigger.next_to(r_q_brace, RIGHT, buff=2*text_buff + get_len(r_q_zero_bigger) + get_len(r_q_if_bigger)).shift([0, get_height(r_q_brace)/4, 0])),

            r_q_if_bigger.animate.move_to([
                r_q_brace.get_right()[0] + 3/2*text_buff + get_len(r_q_zero_smaller) + get_len(r_q_if_bigger)/2,
                r_q_if_bigger.get_center()[1], r_q_if_bigger.get_center()[2]
            ]),
            Write(r_q_r_q_smaller.next_to(r_q_brace, RIGHT, buff=2*text_buff + get_len(r_q_zero_smaller) + get_len(r_q_if_smaller)).shift([0, -get_height(r_q_brace)/4, 0])),
            r_q_if_smaller.animate.move_to([
                r_q_brace.get_right()[0] + 3/2*text_buff + get_len(r_q_zero_smaller) + get_len(r_q_if_smaller)/2,
                r_q_if_smaller.get_center()[1], r_q_if_smaller.get_center()[2]
            ]),
            nabla_condition_copy.animate.set_opacity(0.0)

        )
        self.wait(1.5)
        # Moving the conditional:
        self.play(
            r_q_second_instance.animate.next_to(nabla_expression, DOWN, buff=text_buff/2).shift([get_len(nabla_expression)/2 - get_len(r_q_second_instance)/2, 0, 0]),
        )
        self.play(
            FadeToColor(r_q_zero_rq_bigger, ManimColor("#9059FF")),
            FadeToColor(r_q_zero_rq_smaller, ManimColor("#9059FF"))
        )
        self.next_section(skip_animations=True)
        self.wait(1)

        # Second conditional:
        # First instance:
        self.play(Write(r_div_first))

        # Second instance:
        self.wait(1)
        self.play(
            # bigger:
            Create(r_div_minus_bigger),
            r_div_one_bigger.animate.next_to(r_div_minus_bigger, RIGHT, buff=text_buff),
            r_div_sign_bigger.animate.next_to(r_div_minus_bigger, RIGHT, buff=2*text_buff + get_len(r_div_one_bigger)),
            Create(r_div_zero_bigger.next_to(r_div_minus_bigger, RIGHT, buff=3*text_buff + get_len(r_div_one_bigger) + get_len(r_div_sign_bigger))),
            r_div_if_bigger.animate.next_to(r_div_minus_bigger, RIGHT, buff=4*text_buff + get_len(r_div_one_bigger) + get_len(r_div_sign_bigger) + get_len(r_div_zero_bigger)),
            # smaller:
            Create(r_div_minus_smaller),
            r_div_one_smaller.animate.next_to(r_div_minus_smaller, RIGHT, buff=text_buff),
            r_div_sign_smaller.animate.next_to(r_div_minus_smaller, RIGHT, buff=2*text_buff + get_len(r_div_one_smaller)),
            Create(r_div_zero_smaller.next_to(r_div_minus_smaller, RIGHT, buff=3*text_buff + get_len(r_div_one_smaller) + get_len(r_div_sign_smaller))),
            r_div_if_smaller.animate.next_to(r_div_minus_smaller, RIGHT, buff=4*text_buff + get_len(r_div_one_smaller) + get_len(r_div_sign_smaller) + get_len(r_div_zero_smaller)),
        )
        self.play(
            r_div_second.animate.move_to(self.camera.frame.get_center())
        )
        self.wait(1)
        # Third instance:
        r_div_prime_bigger.move_to(r_div_rq_bigger.get_center())
        r_div_prime_smaller.move_to(r_div_rq_smaller.get_center())
        self.play(
            ReplacementTransform(r_div_rq_bigger, r_div_prime_bigger),
            ReplacementTransform(r_div_rq_smaller, r_div_prime_smaller),
        )
        self.wait(1)
        self.play(
            r_div_third.animate.next_to(rq_identity, DOWN, buff=text_buff).shift([-get_len(rq_identity)/2 + get_len(r_div_third)/2 - text_buff/2, 0, 0])
        )
        self.play(
            FadeToColor(r_div_prime_bigger, ManimColor("#FFF700")), FadeToColor(r_div_prime_smaller, ManimColor("#FFF700")),
            rq_identity.animate.shift([get_len(r_div_prime_bigger), 0, 0])
        )
        self.next_section(skip_animations=True)
        self.wait(1)
        # Writing the equation
        r_eq_first.move_to(self.camera.frame.get_center())
        r_div_replacement_group_smaller_copy = r_div_replacement_group_smaller.copy()
        self.play(ReplacementTransform(r_div_replacement_group_smaller_copy, r_eq_first))        
        self.wait(1)
        self.play(
            Write(r_eq_second.next_to(r_eq_first, RIGHT, buff=text_buff)),
            Write(r_eq_equals.next_to(r_eq_first_group, RIGHT, buff=text_buff)),
            Write(r_eq_final.next_to(r_eq_first_group, RIGHT, buff=2*text_buff + get_len(r_eq_equals)))
        )
        self.play(
            r_eq_group.animate.move_to(self.camera.frame.get_center())
        )
        # Replacing r'/q' -1 with (r'-q')/q':
        r_eq_final_bottom.move_to(r_eq_final) 
        self.wait(1)
        self.play(
            r_eq_final_bottom.animate.move_to(r_div_replacement_group_smaller.get_center()),
            FadeOut(r_div_replacement_group_smaller),
            FadeOut(r_eq_first_group),
            FadeOut(r_eq_equals),
            r_eq_final.animate.move_to(self.camera.frame.get_center())
        )
        r_eq_final_top.move_to(r_eq_final_bottom)
        self.play(
            FadeToColor(r_eq_final_bottom, ManimColor("#FFF700")),
            FadeOut(r_div_replacement_group_bigger),
            r_eq_final_top.animate.move_to(r_div_replacement_group_bigger)
        )
        self.play(FadeToColor(r_eq_final_top, ManimColor("#FFF700")))
        self.wait(1)
        # q>0 => Sign((r'-q')/q') = Sign(r'-q')
        r_sign_left.next_to(r_eq_final, LEFT, buff=text_buff/2)
        q_bigger_than_zero.next_to(r_sign_left, LEFT, buff=text_buff)
        r_brace_left.next_to(r_eq_final, RIGHT, buff=text_buff/2)
        r_sign_right.next_to(r_brace_left, RIGHT, buff=text_buff)
        r_minus_q.next_to(r_sign_right, RIGHT, buff=text_buff/4)
        r_brace_right.next_to(r_minus_q, RIGHT, buff=text_buff/4)
        self.play(Write(q_bigger_than_zero))
        self.wait(0.5)
        self.play(Write(q_bigger_group), run_time=3)
        self.wait(1)
        self.play(
            FadeOut(r_eq_final_top_q),
            FadeOut(r_eq_final_top_line),
            FadeOut(r_eq_final_bottom_q),
            FadeOut(r_eq_final_bottom_line)
        )
        self.play(
            r_eq_final_top_rq.animate.match_y(r_div_sign_bigger),
            r_eq_final_bottom_rq.animate.match_y(r_div_sign_smaller)
        )
        self.next_section(skip_animations=True)
        self.wait(1)
        # Adapting to the new brace:
        r_div_smaller_brace.move_to([r_div_brace.get_center()[0], r_div_brace.get_top()[1] - get_height(r_div_smaller_brace)/2, r_div_brace.get_center()[2]])
        self.play(
            ReplacementTransform(r_div_brace, r_div_smaller_brace),
            r_div_fourth_bigger.animate.move_to([r_div_fourth_bigger.get_center()[0], r_div_smaller_brace.get_center()[1] + get_height(r_div_smaller_brace)/4, r_div_fourth_bigger.get_center()[2]]),
            r_div_fourth_smaller.animate.move_to([r_div_fourth_smaller.get_center()[0], r_div_smaller_brace.get_center()[1] - get_height(r_div_smaller_brace)/4, r_div_fourth_smaller.get_center()[2]]),
            FadeOut(q_bigger_group),
            FadeOut(r_eq_final),
            FadeOut(q_bigger_than_zero)
        )

        # Moving the braces 
        self.play(
            r_div_fourth.animate.move_to([
                self.camera.frame.get_center()[0] - get_len(self.camera.frame)/4,
                self.camera.frame.get_center()[1], r_div_fourth.get_center()[2]
            ]),
            r_q_second_instance.animate.move_to([
                self.camera.frame.get_center()[0] + get_len(self.camera.frame)/4,
                self.camera.frame.get_center()[1], r_q_second_instance.get_center()[2]]),
        )
        self.wait(1)
        self.play(
            nabla_condition_copy.animate.set_opacity(1.0)
        )
        self.wait(1)
        # Converting everything to Nabla:
        nabla_comparison_normal_top.next_to(r_q_zero_zero_bigger, LEFT, buff=text_buff)
        nabla_comparison_normal_bottom.next_to(r_q_zero_zero_smaller, LEFT, buff=text_buff)
        nabla_comparison_prime_top.next_to(r_div_sign_bigger, LEFT, buff=text_buff)
        nabla_comparison_prime_bottom.next_to(r_div_sign_smaller, LEFT, buff=text_buff)
        self.play(
            ReplacementTransform(r_q_zero_rq_bigger, nabla_comparison_normal_top),
            ReplacementTransform(r_q_zero_rq_smaller, nabla_comparison_normal_bottom),
            r_q_brace.animate.move_to([
                nabla_comparison_normal_top.get_left()[0] - get_len(r_q_brace)/2 - text_buff/2,
                r_q_brace.get_center()[1], r_q_brace.get_center()[2]
            ])
        )
        self.wait()
        self.play(
            ReplacementTransform(r_eq_final_top_rq, nabla_comparison_prime_top),
            ReplacementTransform(r_eq_final_bottom_rq, nabla_comparison_prime_bottom),
            r_div_smaller_brace.animate.move_to([
                nabla_comparison_prime_top.get_left()[0] - get_len(r_div_smaller_brace)/2 - text_buff/2,
                r_div_smaller_brace.get_center()[1], r_div_smaller_brace.get_center()[2]
            ]),
        )
        self.next_section(skip_animations=True)
        self.wait(1)
        self.play(
            rq_identity.animate.set_opacity(0.0),
            r_div_fifth.animate.set_opacity(0.0),
            r_q_third_instance.animate.set_opacity(0.0),
            nabla_condition_copy.animate.set_opacity(0.0),
            nabla_expression.animate.move_to(self.camera.frame.get_center())
        )

        '''
        Handy tips for animating:
        ****************************************************************************************************************************************
        I have left two equations:
        q' = b1 + 1 - delta(b)/delta(a)(a1 + 1)
        r' = delta(b)/delta(a)(a1+1) - b1

        in one variable that shows the equation at the top left of the screen.
        The variable is called prime_equations, and to make it visible run:

        self.play(prime_equations.animate.set_opacity(1.0))

        prime_equations = VGroup(r_prime_equation, q_prime_equation)

        ****************************************************************************************************************************************
        The variable that was used for the expression nabla = r - q is called nabla_expression, and it is a VGroup that is composed of two parts:
    
            Nabla =         r - q
        | <- nabla -> | <- nabla_rq -> |

        (here is the code original code for the variable)
        nabla = Tex(r"$\boldsymbol{\nabla = }$", font_size=text_size*4/3)
        nabla_rq = Tex(r"$\boldsymbol{r-q}$", font_size=text_size*4/3)
        nabla_expression = VGroup(nabla, nabla_rq).arrange(RIGHT, buff=text_buff)

        nabla = Tex(r"$\boldsymbol{\nabla = }$", font_size=text_size*4/3)
        nabla_rq = Tex(r"$\boldsymbol{r-q}$", font_size=text_size*4/3)

        Don't forget that you can use nabla_expression.add() or nabla_expression.remove() for ease of use when changing from r-q to r'-q'
        as it is a VGroup!

        ****************************************************************************************************************************************
        '''

        self.next_section()
        self.wait(1.5)
        
        #Приписываем прайм штуки
        self.play(nabla_expression.animate.shift(LEFT * get_len(new_nabla_expression)/2))
        self.play(Write(new_nabla_expression.next_to(nabla_expression, RIGHT, buff = text_buff)))
        self.wait(2)

        #Заменяем
        self.play(Unwrite(nabla_rq), Unwrite(nabla_rq_equals))
        self.play(nabla.animate.shift(RIGHT * get_len(nabla_rq)), nabla_rq_prime.animate.shift(LEFT * get_len(nabla_rq)))
        nabla_expression.remove(nabla_rq)
        nabla_expression.add(nabla_rq_prime)
        self.wait(1)


        self.wait(1.5)
        #Спавним за камерой, потом двигаем на место
        self.add(new_prime_equations.move_to(self.camera.frame.get_left()).shift(LEFT * get_len(new_prime_equations)).shift(UP * get_height(new_prime_equations)*2))

        self.play(new_prime_equations.animate.shift(RIGHT * get_len(new_prime_equations) *1.6))

        self.wait(1)

        # Рисуем скобочки и штучки
        self.play(
            #Write(equal_after_new_nabla.move_to(nabla_expression.get_center()).shift(RIGHT * (get_len(nabla_expression)/2 + get_len(equal_after_new_nabla)))),
            Write(equal_after_new_nabla.next_to(nabla_expression, RIGHT, buff = text_buff)),
            Write(equal_before_phantom),
            Write(brace_one), 
            Write(brace_two), 
            Write(phantom_minus),
            Write(brace_three), 
            Write(brace_four) 
        )
        self.wait(1)

        # Меняем цвет 
        self.play(
            nabla_rq_prime[0].animate.set_color(r_prime_stuff_color),
            new_r_prime.animate.set_color(r_prime_stuff_color),
        )
        self.wait(1)

        self.wait(1)
        # Двигаем в между скобочек
        self.play( 
            new_r_prime_after_equal.animate.move_to(r_prime_phantom.get_center()),
            FadeOut(new_r_prime_before_equal)
        )
        self.wait(1)

        # Меняем цвет
        self.play(
            nabla_rq_prime[2].animate.set_color(q_prime_stuff_color),
            new_q_prime.animate.set_color(q_prime_stuff_color) 
        )

        self.wait(1)
        # Двигаем в между скобочек
        self.play( 
            new_q_prime_after_equal.animate.move_to(q_prime_phantom.get_center()),
            FadeOut(new_q_prime_before_equal)
        )

        # Убираем лишнее
        self.play(
            nabla_expression.animate.set_opacity(0),
            FadeOut(equal_after_new_nabla),
            FadeOut(equal_before_phantom),
        )
        self.wait(1)

        self.play(equation_one.animate.set_color(WHITE))
        self.wait(1)

        #Итерация упрощений 1 (ниже закоментил знаки "=" после каждого equation, чтобы сравнить как лучше)
        #equation_one.add(equal_after_phantom)
        #self.play(FadeIn(equal_after_phantom.next_to(equation_one, RIGHT * text_buff)))
        self.play(
            equation_one.animate.move_to(row2.get_center()).scale(shrink),
            FadeIn(equation_two.move_to(row1.get_center()))
        )
        self.wait(1)

        #Итерация упрощений 2
        #self.play(FadeIn(equal_after_two))

        self.play(
            equation_one.animate.move_to(row3.get_center()).scale(shrink),
            #equal_after_phantom.animate.scale(shrink),
            equation_two.animate.move_to(row2.get_center()).scale(shrink),
            #equal_after_two.animate.scale(shrink),
            FadeIn(equation_three.move_to(row1.get_center()))
        )

        self.wait(1)

        #Итерация упрощений 3
        #self.play(FadeIn(equal_after_three))

        self.play(
            equation_one.animate.move_to(row4.get_center()).scale(shrink).set_opacity(0),
            #equal_after_phantom.animate.scale(shrink).set_opacity(0),
            equation_two.animate.move_to(row3.get_center()).scale(shrink),
            #equal_after_two.animate.scale(shrink),
            equation_three.animate.move_to(row2.get_center()).scale(shrink),
            #equal_after_three.animate.scale(shrink),
            FadeIn(equation_four.move_to(row1.get_center()))

        )

        self.wait(1)

        #Итерация упрощений 4
        #self.play(FadeIn(equal_after_four))

        self.play(
            equation_two.animate.move_to(row4.get_center()).scale(shrink).set_opacity(0),
            #equal_after_two.animate.scale(shrink).set_opacity(0),
            equation_three.animate.move_to(row3.get_center()).scale(shrink),
            #equal_after_three.animate.scale(shrink),
            equation_four.animate.move_to(row2.get_center()).scale(shrink),
            #equal_after_four.animate.scale(shrink),
            FadeIn(equation_five_group.move_to(row1.get_center()))
        )
        
        self.wait(2)

        #Итерация упрощений 5. Тут оставляем только 5 equation
        self.play(
            equation_five_group.animate.move_to(row2.get_center()),
            equation_four.animate.move_to(row3.get_center()).scale(shrink).set_opacity(0),
            #equal_after_four.animate.scale(shrink).set_opacity(0),
            equation_three.animate.move_to(row4.get_center()).scale(shrink).set_opacity(0),
            #equal_after_three.animate.scale(shrink).set_opacity(0),

        )
        
        self.next_section()

        #Спавним наблу за камерой
        final_nabla_expression.move_to([
            self.camera.frame.get_left()[0] - get_len(final_nabla_expression) * 4/3,
            row2.get_center()[1],
            0
        ])

        final_nabla_expression.set_color(GREEN_C)

        # Вставляем на место так, чтобы все было по центру
        self.play(
            equation_five_group.animate.shift(RIGHT * ((get_len(final_nabla_expression) + text_buff )/2 )),
            final_nabla_expression.animate.next_to(equation_five_group, LEFT, buff = text_buff/2 - (get_len(final_nabla_expression)/2))
        )


        self.wait(3)
        
        #Група которая меняется на phantom_delta_equation. Решил именно тут в секции анимаций делать, чтобы было понятнее
        preinstance = VGroup(final_nabla_expression, equation_five_group)

        self.play(TransformMatchingTex(preinstance, phantom_delta_equation))

        self.wait(1)

        # Чуть подімаем
        self.play(
            phantom_delta_equation.animate.move_to(row3.get_center()),
        )

        # Рисуем знак "="
        self.play(
            phantom_delta_equation.animate.shift(LEFT * ((get_len(equal_after_five) + text_buff )/2 )),
            FadeIn(equal_after_five.next_to(phantom_delta_equation, RIGHT, buff = text_buff/2 - (get_len(equal_after_five)/2)))
        )

        # Спваним финальную форму
        self.play(
            FadeIn(final_form_group.move_to(row2.get_center()))
        )

        self.wait(2)

        # убираем все лишнее и ставим уравнение в нужное место
        self.play(
            FadeOut(phantom_delta_equation),
            FadeOut(equal_after_five),
            FadeOut(equal_before_final),
            final_form.animate.shift(LEFT * ((get_len(equal_before_final)/2) + text_buff/2))
        )
        self.wait(3)


class SixthScene(MovingCameraScene):
    def construct(self):
        # border = always_redraw(lambda: Rectangle(width=get_len(self.camera.frame), height=get_height(self.camera.frame), stroke_width=1)) # For ease of debugging
        text_size = 44
        text_buff = 0.25
        # "Let’s re-write the indices to make everything look a bit more like computer code rather than some maths:"
        # The first equation:
        nabla_i = Tex(r"$\boldsymbol{\nabla_i = 2a_{i-1}\Delta b + 2\Delta b - 2\Delta ab_{i-1} - \Delta a}$", font_size=text_size)
        nabla_i.move_to(self.camera.frame.get_center()) # Maybe redundant, but just to be sure

        # The second equation:
        nabla_i_plus = Tex(r"$\boldsymbol{\nabla_{i+1} = 2a_i\Delta b + 2\Delta b - 2\Delta ab_i - \Delta a}$", font_size=text_size)
        nabla_i_plus.next_to(nabla_i, DOWN, buff=text_buff).shift([- 1/2*get_len(nabla_i) + 1/2*get_len(nabla_i_plus), 0, 0])

        # i є [1, \Delta a]:
        nabla_i_e = Tex(r"$\boldsymbol{for\;i\; \epsilon\;[1, \Delta a]:}$", font_size=text_size)
        nabla_i_e.next_to(nabla_i, UP, buff=text_buff).shift([- 1/2*get_len(nabla_i) + 1/2*get_len(nabla_i_e), 0, 0])

        nabla_i_group = VGroup(nabla_i, nabla_i_plus, nabla_i_e).set_z_index(2)

        # Rectangle for the equations:
        nabla_i_scale = 0.7
        nabla_i_rectangle = Rectangle(
            width = get_len(nabla_i_group) * nabla_i_scale + text_buff/2,
            height = get_height(nabla_i_group) * nabla_i_scale + text_buff/4,
            stroke_width = 1,
            fill_opacity = 0.7,
            fill_color=BLACK
        ).move_to([
            self.camera.frame.get_left()[0] + text_buff + 1/2*get_len(nabla_i_group) * nabla_i_scale,
            self.camera.frame.get_top()[1] - text_buff - 1/2*get_height(nabla_i_group) * nabla_i_scale,
            nabla_i_group.get_center()[2]
        ]).set_z_index(1)

        # Grid and points on the grid:
        # Plane:
        plane_square_size = 4.5
        num_squares_x = 4
        num_squares_y = 3
        tick_size = 0.15
        line_stroke_width = 5
        background_stroke_width = 3
        plane = NumberPlane(
            x_range = [0, num_squares_x, 1],
            y_range = [0, num_squares_y, 1],
            x_length = plane_square_size * num_squares_x,
            y_length = plane_square_size * num_squares_y,
            axis_config = {
                "include_numbers": True,
                "font_size": text_size,
                "include_ticks": True,
                "tick_size": tick_size,
                "line_to_number_buff": text_buff,
                "stroke_width": line_stroke_width
            },
            x_axis_config = {
                "label_direction": DOWN
            },
            y_axis_config = {
                "label_direction": LEFT
            },
            background_line_style={
                "stroke_width": background_stroke_width
            },

        )
        plane_upper_line = Line(start=plane.c2p(0, num_squares_x*plane_square_size), end=plane.c2p(num_squares_x*plane_square_size, num_squares_y*plane_square_size), stroke_width= 2, color=WHITE)
        plane_right_line = Line(start=plane.c2p(num_squares_x*plane_square_size, num_squares_y*plane_square_size), end=plane.c2p(num_squares_x*plane_square_size,0), stroke_width= 2, color=WHITE)

        plane_box = VGroup(plane, plane_upper_line, plane_right_line)
        plane_box.move_to([
            self.camera.frame.get_left()[0] + 3/16*get_len(self.camera.frame) + 1/2*get_len(plane_box),
            self.camera.frame.get_bottom()[1] + 1/4*get_height(self.camera.frame) + 1/2*get_len(plane_box), plane_box.get_center()[2]
        ]).set_z_index(0)

        # Points:
        d1_dot = Dot(plane.c2p(0, 0), radius= 0.1, color=GREEN).set_z_index(2)
        d1_label = Tex(r"$\boldsymbol{D_1 (0, 0)}$", font_size=text_size).next_to(d1_dot, DOWN, buff=text_buff/2)
        d1_group = VGroup(d1_dot, d1_label)

        # Rectangle for the equations on the number plane:
        plane_rectangle = Rectangle(
            width = pixels_to_munits(background_stroke_width) + text_buff,
            height = plane_square_size - tick_size - pixels_to_munits(background_stroke_width) - 0.01,
            fill_opacity = 0.7,
            stroke_opacity = 0.0,
            stroke_width = 0.0,
            fill_color = BLACK
        ).move_to([
            plane.c2p(2, 0.5)[0],
            plane.c2p(2, 0.5)[1] + 1/2*tick_size,
            plane.c2p(2, 0.5)[2]
        ]).set_z_index(1)

        # Nabla equation in the rectangle:
        nabla_plane_temp = Tex(r"$\boldsymbol{a}$", font_size=text_size)
        # nabla_i: \boldsymbol{\nabla_i = 2a_{i-1}\Delta b + 2\Delta b - 2\Delta ab_{i-1} - \Delta a
        nabla_plane_nabla = Tex(r"$\boldsymbol{\nabla_i}$", font_size = nabla_i_scale * text_size)
        nabla_plane_equals_equals = Tex(r"$\boldsymbol{=}$", font_size = nabla_i_scale * text_size).next_to(nabla_plane_nabla, RIGHT, buff=text_buff)
        nabla_plane_equals_two = Tex(r"$\boldsymbol{2}$", font_size= nabla_i_scale * text_size).next_to(nabla_plane_equals_equals, RIGHT, buff=text_buff/2)
        nabla_plane_equals = VGroup(nabla_plane_equals_equals, nabla_plane_equals_two)
        nabla_plane_a = Tex(r"$\boldsymbol{a_{i-1}}$", font_size = nabla_i_scale * text_size).next_to(nabla_plane_equals, RIGHT, buff=text_buff/4).shift([0, -0.05, 0])
        nabla_plane_delta_b_b = Tex(r"$\boldsymbol{\Delta b \;+}$", font_size = nabla_i_scale * text_size).next_to(nabla_plane_a, RIGHT, buff=text_buff/4).shift([0, -0.0125, 0])
        nabla_plane_delta_b_2b = Tex(r"$\boldsymbol{2\Delta b}$", font_size = nabla_i_scale * text_size).next_to(nabla_plane_delta_b_b, RIGHT, buff=text_buff/2).shift([0, 0.0125, 0])
        nabla_plane_delta_b_a = Tex(r"$\boldsymbol{-\;2\Delta a}$", font_size = nabla_i_scale * text_size).next_to(nabla_plane_delta_b_2b, RIGHT, buff=text_buff/2)
        nabla_plane_delta_b = VGroup(nabla_plane_delta_b_b, nabla_plane_delta_b_2b, nabla_plane_delta_b_a)
        nabla_plane_b = Tex(r"$\boldsymbol{b_{i-1}}$", font_size = nabla_i_scale * text_size).next_to(nabla_plane_delta_b, RIGHT, buff=text_buff/4).shift([0, -0.025, 0])
        nabla_plane_delta_a = Tex(r"$\boldsymbol{- \Delta a}$", font_size = nabla_i_scale * text_size).next_to(nabla_plane_b, RIGHT, buff=text_buff/4).match_y(nabla_plane_nabla)

        nabla_plane_remove = VGroup(nabla_plane_nabla, nabla_plane_a, nabla_plane_b)

        nabla_plane_group = VGroup(nabla_plane_nabla, nabla_plane_equals, nabla_plane_a, nabla_plane_delta_b, nabla_plane_b, nabla_plane_delta_a)
        nabla_plane_group.move_to(plane.c2p(2, 0.5)).set_z_index(2)

        # Second instance of the equation:
        i_is_one = Tex(r"$\boldsymbol{i=1:}$", font_size= nabla_i_scale * text_size).next_to(nabla_plane_nabla, LEFT, buff=text_buff/2)
        nabla_one_nabla = Tex(r"$\boldsymbol{\nabla_1}$", font_size = nabla_i_scale * text_size).move_to(nabla_plane_nabla.get_center())
        nabla_one_a = Tex(r"$\boldsymbol{\times a_0 \times}$", font_size = nabla_i_scale * text_size).move_to(nabla_plane_a.get_center())
        nabla_one_a.next_to(nabla_one_nabla, RIGHT, buff=text_buff + get_len(nabla_plane_equals)).shift([0, -0.025, 0])
        nabla_one_b = Tex(r"$\boldsymbol{\times b_0}$", font_size = nabla_i_scale * text_size).move_to(nabla_plane_b.get_center())
        nabla_one_b.next_to(nabla_one_nabla, RIGHT, buff=6/4*text_buff + get_len(nabla_plane_equals) + get_len(nabla_one_a) + get_len(nabla_plane_delta_b))

        nabla_one_remove = VGroup(nabla_one_nabla, nabla_one_a, nabla_one_b)

        nabla_one_group = VGroup(i_is_one, nabla_one_nabla, nabla_plane_equals, nabla_one_a, nabla_plane_delta_b, nabla_one_b, nabla_plane_delta_a).set_z_index(2)

        # a0 = 0, b0 = 0:
        a_is_zero = Tex(r"$\boldsymbol{a_0=0}$", font_size = nabla_i_scale * text_size)
        b_is_zero = Tex(r"$\boldsymbol{b_0=0}$", font_size = nabla_i_scale * text_size).next_to(a_is_zero, DOWN, buff=text_buff/2)
        group_is_zero = VGroup(a_is_zero, b_is_zero)
        group_is_zero.next_to(i_is_one, UP, buff=text_buff/2)

        # Third instance of the equation:
        nabla_zero_a = Tex(r"$\boldsymbol{\times 0 \times}$", font_size = nabla_i_scale * text_size).next_to(nabla_one_nabla, RIGHT, buff=3/4*text_buff + get_len(nabla_plane_equals))
        nabla_zero_b = Tex(r"$\boldsymbol{\times 0}$", font_size = nabla_i_scale * text_size)
        nabla_zero_b.next_to(nabla_one_nabla, RIGHT, buff=5/4*text_buff + get_len(nabla_plane_equals) + get_len(nabla_zero_a) + get_len(nabla_plane_delta_b))

        # Removal group:
        nabla_removal_group = VGroup(nabla_plane_equals_two, nabla_zero_a, nabla_plane_delta_b_b, nabla_plane_delta_b_a, nabla_zero_b)
        nabla_simplified = VGroup(nabla_one_nabla, nabla_plane_equals_equals, nabla_plane_delta_b_2b, nabla_plane_delta_a)

        # Bigger rectangle for the top left:
        nabla_i_bigger_rectangle = Rectangle(
            width = get_len(nabla_i_group) * nabla_i_scale + text_buff/2,
            height = get_height(nabla_i_group) * nabla_i_scale + get_height(nabla_simplified) + 3/4*text_buff,
            stroke_width = 1,
            fill_opacity = 0.7,
            fill_color=BLACK
        ).move_to([
            self.camera.frame.get_left()[0] + text_buff + 1/2*get_len(nabla_i_group) * nabla_i_scale,
            self.camera.frame.get_top()[1] - 5/4*text_buff - 1/2*get_height(nabla_i_group) * nabla_i_scale - 1/2*get_height(nabla_simplified),
            nabla_i_group.get_center()[2]
        ]).set_z_index(1)

        nabla_i_movement_group = VGroup(nabla_i_group, nabla_i_bigger_rectangle, nabla_simplified)

        # 'If we have just moved diagonally':
        starting_dot = Dot(plane.c2p(1, 1), radius = 0.1, color=GREEN).set_z_index(2)
        starting_label = Tex(r"$\boldsymbol{(a_{i-1}, \; b_{i-1})}$", font_size=text_size).next_to(starting_dot, DOWN, buff=text_buff).set_z_index(2)
        starting_rectangle = Rectangle(
            width = get_len(starting_label),
            height = get_height(starting_label),
            fill_opacity = 0.7,
            fill_color = BLACK,
            stroke_opacity = 0.0
        ).move_to(starting_label.get_center()).set_z_index(1)

        d1_d2_line_diagonally = Line(
            start = d1_dot.get_center(),
            end = plane.c2p(4, 3.6),
            stroke_width = 10,
            color = WHITE
        )

        starting_arrow = Arrow(
            start = d1_dot.get_center(),
            end = plane.c2p(1, 1),
            color = ManimColor("#FF0000"),
            buff = 1/2*get_len(starting_dot)
        ).set_z_index(-1)

        diagonal_dot = Dot(plane.c2p(2, 2), radius = 0.1, color=GREEN).set_z_index(2)
        diagonal_label = Tex(r"$\boldsymbol{(a_i, \; b_i)}$", font_size=text_size).next_to(diagonal_dot, UP, buff=text_buff).set_z_index(2)
        diagonal_rectangle = Rectangle(
            width = get_len(diagonal_label),
            height = get_height(diagonal_label),
            fill_opacity = 0.7,
            fill_color = BLACK,
            stroke_opacity = 0.0
        ).move_to(diagonal_label.get_center()).set_z_index(1)

        diagonal_arrow = Arrow(
            start = starting_dot.get_center(),
            end = diagonal_dot.get_center(),
            color = ManimColor("#FF0000"),
            buff = get_len(diagonal_dot)/2
        )

        # 'If you move diagonally/horizontally' labels and text:
        # Diagonally:

        diagonal_explanation_if_if = Tex(r"$\boldsymbol{\textbf{if}}$", font_size=text_size)
        diagonal_explanation_if_move = Tex(r"$\boldsymbol{\textbf{you move diagonally:}}$", font_size=text_size).next_to(diagonal_explanation_if_if, RIGHT, buff=text_buff/2)
        diagonal_explanation_if = VGroup(diagonal_explanation_if_if, diagonal_explanation_if_move)

        diagonal_explanation_if_nabla = Tex(r"$\boldsymbol{\nabla_i \ge 0}$", r"$\boldsymbol{\,:}$", font_size=text_size).set_z_index(2)

        # diagonal_explanation_if = Tex(r"$\boldsymbol{\textbf{if you move diagonally:}}$", font_size = text_size)
        diagonal_explanation_a = Tex(r"$\boldsymbol{a_i = a_{i-1}+1}$", font_size=text_size).next_to(diagonal_explanation_if, DOWN, buff=text_buff/2)
        diagonal_explanation_a.shift([-1/2*get_len(diagonal_explanation_if) + 1/2*get_len(diagonal_explanation_a), 0, 0])

        diagonal_explanation_b = Tex(r"$\boldsymbol{b_i = b_{i-1}+1}$", font_size=text_size).next_to(diagonal_explanation_a, DOWN, buff=text_buff/2)
        diagonal_explanation_b.shift([-1/2*get_len(diagonal_explanation_a) + 1/2*get_len(diagonal_explanation_b), 0, 0])

        diagonal_explanation = VGroup(diagonal_explanation_if, diagonal_explanation_a, diagonal_explanation_b)
        diagonal_explanation.move_to(plane.c2p(3,1.75)).set_z_index(2)

        diagonal_bullet = Tex(r"$\bullet$", font_size=text_size).next_to(diagonal_explanation_if, LEFT, buff=text_buff/2).set_z_index(2)

        diagonal_movement_group = VGroup(diagonal_bullet, diagonal_explanation_if_if, diagonal_explanation_if_nabla, diagonal_explanation_a, diagonal_explanation_b)

        # Horizontally:
        horizontal_dot = Dot(plane.c2p(2, 1), radius = 0.1, color=GREEN).set_z_index(2)
        horizontal_label = diagonal_label.copy().next_to(horizontal_dot, DOWN, buff=text_buff)
        horizontal_rectangle = diagonal_rectangle.copy().move_to(horizontal_label.get_center())

        horizontal_arrow = Arrow(
            start = starting_dot.get_center(),
            end = horizontal_dot.get_center(),
            color = ManimColor("#FF0000"),
            buff = get_len(horizontal_dot)/2
        ).set_z_index(1)

        horizontal_explanation_if_if = Tex(r"$\boldsymbol{\textbf{if}}$", font_size=text_size).next_to(diagonal_explanation, DOWN, buff=text_buff)
        horizontal_explanation_if_if.match_x(diagonal_explanation_if_if)
        horizontal_explanation_if_move = Tex(r"$\boldsymbol{\textbf{you move horizontally:}}$", font_size=text_size).next_to(horizontal_explanation_if_if, RIGHT, buff=text_buff/2)
        horizontal_explanation_if = VGroup(horizontal_explanation_if_if, horizontal_explanation_if_move)

        horizontal_explanation_if_nabla = Tex(r"$\boldsymbol{\nabla_i < 0}$", r"$\boldsymbol{\,:}$", font_size=text_size).set_z_index(2)

        horizontal_explanation_a = Tex(r"$\boldsymbol{a_i = a_{i-1}+1}$", font_size=text_size).next_to(horizontal_explanation_if, DOWN, buff=text_buff/2)
        horizontal_explanation_a.shift([-1/2*get_len(horizontal_explanation_if) + 1/2*get_len(horizontal_explanation_a), 0, 0])

        horizontal_explanation_b = Tex(r"$\boldsymbol{b_i = b_{i-1}}$", font_size=text_size).next_to(horizontal_explanation_a, DOWN, buff=text_buff/2)
        horizontal_explanation_b.shift([-1/2*get_len(horizontal_explanation_a) + 1/2*get_len(horizontal_explanation_b), 0, 0])

        horizontal_explanation = VGroup(horizontal_explanation_if, horizontal_explanation_a, horizontal_explanation_b)
        horizontal_explanation.set_z_index(2)

        horizontal_bullet = Tex(r"$\bullet$", font_size=text_size).next_to(horizontal_explanation_if, LEFT, buff=text_buff/2).set_z_index(2)

        explanation_rectangle = Rectangle(
            width = horizontal_explanation_if.get_right()[0] - diagonal_bullet.get_left()[0],
            height = plane_square_size - pixels_to_munits(background_stroke_width) - 0.01,
            fill_opacity = 0.7,
            stroke_opacity = 0.0,
            stroke_width = 0.0,
            fill_color = BLACK
        ).move_to([
            diagonal_bullet.get_left()[0] + 1/2*(horizontal_explanation_if.get_right()[0] - diagonal_bullet.get_left()[0]),
            plane.c2p(3, 1.5)[1], plane.c2p(3, 1.5)[2]
        ]).set_z_index(1)
        explanation_movement_group = VGroup(diagonal_explanation, diagonal_bullet, horizontal_explanation, horizontal_bullet, explanation_rectangle)

        horizontal_movement_group = VGroup(horizontal_bullet, horizontal_explanation_if_if, horizontal_explanation_if_nabla, horizontal_explanation_a, horizontal_explanation_b)

        explanation_second_movement_group = VGroup(diagonal_movement_group, horizontal_movement_group)

        # Comparing "if you move diagonally" with nabla:
        # nabla >= 0 -> move diagonally:
        nabla_condition = Tex(r"$\boxed{\boldsymbol{\begin{cases}\nabla\ge0\rightarrow move\;diagonally\\\nabla<0\rightarrow move\;horizontally\end{cases}}}$", font_size=text_size * nabla_i_scale)
        nabla_condition.set_z_index(2)
        nabla_condition_rectangle = Rectangle(
            width = get_len(nabla_condition),
            height = get_height(nabla_condition),
            fill_opacity = 0.7,
            fill_color = BLACK,
            stroke_opacity = 0.0
        ).move_to(nabla_condition.get_center())
        nabla_condition_group = VGroup(nabla_condition, nabla_condition_rectangle)

        # Connecting nabla_i and nabla_{i+1}:
        nabla_i_start = Tex(r"$\boldsymbol{\nabla_{i+1} =}$", r"$\boldsymbol{\>2}$", r"$\boldsymbol{a_i}$", r"$\boldsymbol{\Delta b + 2\Delta b - 2\Delta a}$", r"$\boldsymbol{b_i}$", r"$\boldsymbol{ - \Delta a}$", font_size = text_size)
        nabla_i_start_equals = Tex(r"$\boldsymbol{=}$", font_size=text_size)

        nabla_i_copy = Tex(
            r"$\boldsymbol{=2}$",
            r"$\boldsymbol{a_i}$",
            r"$\boldsymbol{\Delta b + 2\Delta b - 2\Delta a}$",
            r"$\boldsymbol{b_i}$",
            r"$\boldsymbol{ - \Delta a}$",
            font_size = text_size
        )
        nabla_i_plus_transformed = Tex(
            r"$\boldsymbol{=2}$",
            r"$\boldsymbol{(a_{i-1}+1)}$",
            r"$\boldsymbol{\Delta b + 2\Delta b - 2\Delta a}$",
            r"$\boldsymbol{(b_{i-1}+1)}$",
            r"$\boldsymbol{ - \Delta a}$",
            font_size = text_size
        )
        nabla_i_plus_transformed_equals = nabla_i_start_equals.copy()
        nabla_i_opened_braces = Tex(
            r"$\boldsymbol{=2}$",
            r"$\boldsymbol{a_{i-1}\Delta b + 2}$",
            r"$\boldsymbol{\Delta b + 2\Delta b - 2\Delta a}$",
            r"$\boldsymbol{b_{i-1}-2\Delta a}$",
            r"$\boldsymbol{ - \Delta a}$",
            font_size = text_size
        )
        nabla_i_opened_braces_equals = nabla_i_start_equals.copy()
        nabla_i_opened_braces_copy = Tex(
            r"$\boldsymbol{\,=\>}$",
            r"$\boldsymbol{2a_{i-1}\Delta b}$",
            r"$\boldsymbol{\,+\,2\Delta b}$",
            r"$\boldsymbol{\,+\,2\Delta b}$",
            r"$\boldsymbol{\,-\,2\Delta ab_{i-1}}$",
            r"$\boldsymbol{\,-\,2\Delta a}$",
            r"$\boldsymbol{\,-\,\Delta a}$",
            font_size = text_size
        )
        nabla_i_reordered = Tex(
            r"$\boldsymbol{\,=\>}$",
            r"$\boldsymbol{2a_{i-1}\Delta b}$",
            r"$\boldsymbol{\,+\,2\Delta b}$",
            r"$\boldsymbol{\,-\,2\Delta ab_{i-1}}$",
            r"$\boldsymbol{\,-\,\Delta a}$",
            r"$\boldsymbol{\,-\,2\Delta a}$",
            r"$\boldsymbol{\,+\,2\Delta b}$",
            font_size = text_size
        )
        nabla_i_reordered_open_brace = Tex(r"$\boldsymbol{(}$", font_size=text_size)
        nabla_i_reordered_close_brace = Tex(r"$\boldsymbol{)}$", font_size=text_size)
        # For nabla < 0:
        nabla_horizontal_start = Tex(r"$\boldsymbol{\nabla_{i+1} =}$", r"$\boldsymbol{\>2}$", r"$\boldsymbol{a_i}$", r"$\boldsymbol{\Delta b + 2\Delta b - 2\Delta a}$", r"$\boldsymbol{b_i}$", r"$\boldsymbol{ - \Delta a}$", font_size = text_size)
        nabla_horizontal_start_equals = Tex(r"$\boldsymbol{=}$", font_size=text_size)

        nabla_horizontal_copy = Tex(
            r"$\boldsymbol{=2}$",
            r"$\boldsymbol{a_i}$",
            r"$\boldsymbol{\Delta b + 2\Delta b - 2\Delta a}$",
            r"$\boldsymbol{b_i}$",
            r"$\boldsymbol{ - \Delta a}$",
            font_size = text_size
        )
        nabla_horizontal_plus_transformed = Tex(
            r"$\boldsymbol{=2}$",
            r"$\boldsymbol{(a_{i-1}+1)}$",
            r"$\boldsymbol{\Delta b + 2\Delta b - 2\Delta a}$",
            r"$\boldsymbol{b_{i-1}}$",
            r"$\boldsymbol{ - \Delta a}$",
            font_size = text_size
        )
        nabla_horizontal_plus_transformed_equals = nabla_horizontal_start_equals.copy()
        nabla_horizontal_opened_braces = Tex(
            r"$\boldsymbol{=2}$",
            r"$\boldsymbol{a_{i-1}\Delta b + 2}$",
            r"$\boldsymbol{\Delta b + 2\Delta b - 2\Delta a}$",
            r"$\boldsymbol{b_{i-1}}$",
            r"$\boldsymbol{ - \Delta a}$",
            font_size = text_size
        )
        nabla_horizontal_opened_braces_equals = nabla_horizontal_start_equals.copy()
        nabla_horizontal_opened_braces_copy = Tex(
            r"$\boldsymbol{\,=\>}$",
            r"$\boldsymbol{2a_{i-1}\Delta b}$",
            r"$\boldsymbol{\,+\,2\Delta b}$",
            r"$\boldsymbol{\,+\,2\Delta b}$",
            r"$\boldsymbol{\,-\,2\Delta ab_{i-1}}$",
            r"$\boldsymbol{\,-\,\Delta a}$",
            font_size = text_size
        )
        nabla_horizontal_reordered = Tex(
            r"$\boldsymbol{\,=\>}$",
            r"$\boldsymbol{2a_{i-1}\Delta b}$",
            r"$\boldsymbol{\,+\,2\Delta b}$",
            r"$\boldsymbol{\,-\,2\Delta ab_{i-1}}$",
            r"$\boldsymbol{\,-\,\Delta a}$",
            r"$\boldsymbol{\,+\,2\Delta b}$",
            font_size = text_size
        )
        nabla_horizontal_reordered_open_brace = Tex(r"$\boldsymbol{(}$", font_size=text_size)
        nabla_horizontal_reordered_close_brace = Tex(r"$\boldsymbol{)}$", font_size=text_size)


        ################################################################################## ANIMATION ##################################################################################
        self.next_section()
        # Adding the equations:
        self.play(Write(nabla_i))
        self.wait(1)
        self.play(Write(nabla_i_plus))
        self.wait(1)
        self.play(Write(nabla_i_e))

        # Putting the equations aside:
        self.play(
            nabla_i_group.animate.scale(nabla_i_scale).move_to([
                self.camera.frame.get_left()[0] + text_buff + 1/2*get_len(nabla_i_group) * nabla_i_scale,
                self.camera.frame.get_top()[1] - text_buff - 1/2*get_height(nabla_i_group) * nabla_i_scale,
                nabla_i_group.get_center()[2]
            ]),
        )
        # Creating a plane:
        self.next_section()
        self.wait(1)
        self.play(Create(plane_box), Create(nabla_i_rectangle), run_time=2)
        self.play(Create(d1_dot), Write(d1_label))
        self.wait(1)
        self.play(
            Create(plane_rectangle),
            ReplacementTransform(nabla_i.copy(), nabla_plane_group)
        )
        self.wait(1)
        self.play(Write(i_is_one))
        self.play(
            FadeOut(nabla_plane_remove),
            Write(nabla_one_remove),
            nabla_plane_equals.animate.next_to(nabla_one_nabla, RIGHT, buff=1/2*text_buff),
            nabla_plane_delta_b.animate.next_to(nabla_one_nabla, RIGHT, buff=5/4*text_buff + get_len(nabla_plane_equals) + get_len(nabla_one_a)),
            nabla_plane_delta_a.animate.next_to(nabla_one_nabla, RIGHT, buff=7/4*text_buff + get_len(nabla_plane_equals) + get_len(nabla_one_a) + get_len(nabla_plane_delta_b) + get_len(nabla_one_b)),
        )
        self.wait(1)
        # Wiggle D1:
        scaling_value = 1.5
        number_wiggles = 15
        angle_wiggle = 0.25
        wiggle_runtime = 1
        self.play(
            Wiggle(d1_label, scale_value=scaling_value, n_wiggles=number_wiggles, rotation_angle=angle_wiggle, run_time=wiggle_runtime)
        )
        self.next_section()
        self.wait(1)
        self.play(
            ReplacementTransform(d1_label.copy(), group_is_zero)
        )
        self.wait(1)
        self.play(
            FadeOut(nabla_one_a),
            FadeOut(nabla_one_b),
            Write(nabla_zero_a),
            Write(nabla_zero_b),
            nabla_plane_delta_b.animate.next_to(nabla_one_nabla, RIGHT, buff=4/4*text_buff + get_len(nabla_plane_equals) + get_len(nabla_zero_a)),
            nabla_plane_delta_a.animate.next_to(nabla_one_nabla, RIGHT, buff=6/4*text_buff + get_len(nabla_plane_equals) + get_len(nabla_zero_a) + get_len(nabla_plane_delta_b) + get_len(nabla_zero_b)).shift([0, 0.025, 0]),
        )
        self.play(
            FadeOut(nabla_removal_group),
            nabla_plane_delta_b_2b.animate.move_to([
                nabla_plane_equals_equals.get_center()[0] + text_buff + 1/2*get_len(nabla_plane_delta_b_2b),
                nabla_plane_delta_b_2b.get_center()[1],
                nabla_plane_delta_b_2b.get_center()[2]
            ]),
            nabla_plane_delta_a.animate.move_to([
                nabla_plane_equals_equals.get_center()[0] + 3/2*text_buff + get_len(nabla_plane_delta_b_2b) + 1/2*get_len(nabla_plane_delta_a),
                nabla_plane_delta_a.get_center()[1],
                nabla_plane_delta_a.get_center()[2]
            ])
        )
        self.wait(1)
        self.play(
            FadeOut(i_is_one),
            FadeOut(group_is_zero),
            ReplacementTransform(nabla_i_rectangle, nabla_i_bigger_rectangle),
            nabla_i.animate.shift([0, -get_height(nabla_simplified) - 1/2*text_buff, 0]),
            nabla_i_plus.animate.shift([0, -get_height(nabla_simplified) - 1/2*text_buff, 0]),
            nabla_simplified.animate.move_to([
                nabla_i_group.get_left()[0] + 1/2*get_len(nabla_simplified),
                nabla_i_group.get_top()[1] - 1/2*text_buff - get_height(nabla_i_e) - 1/2*get_height(nabla_simplified),
                nabla_simplified.get_center()[2]
            ]),
            FadeOut(plane_rectangle)
        )
        self.next_section()
        self.wait(1)
        # Moving to 'If you move diagonally/horizontally':
        self.play(Create(d1_d2_line_diagonally))
        self.play(Create(starting_arrow))
        self.play(
            self.camera.frame.animate.shift([1.4*plane_square_size, 1.3*plane_square_size, 0]),
            nabla_i_movement_group.animate.shift([1.4*plane_square_size, 1.3*plane_square_size, 0]),
            Create(starting_dot)
        )
        self.play(
            FadeOut(starting_arrow),
            Create(diagonal_arrow),
            Create(diagonal_dot)
        )
        self.wait(1)
        self.play(
            Write(starting_label),
            FadeIn(starting_rectangle),
            Write(diagonal_label),
            FadeIn(diagonal_rectangle)
        )
        self.wait(1)
        # If you move diagonally:
        self.play(FadeIn(explanation_rectangle), Write(diagonal_explanation_if), Write(diagonal_bullet))
        self.play(Write(diagonal_explanation_a), Write(diagonal_explanation_b))
        self.wait(1)
        # Moving the line horizontally:
        self.play(
            FadeOut(diagonal_rectangle),
            FadeOut(diagonal_label),
            FadeOut(diagonal_arrow),
            FadeOut(diagonal_dot),
            d1_d2_line_diagonally.animate.put_start_and_end_on(d1_dot.get_center(), plane.c2p(4, 2.6))
        )
        self.play(
            Create(horizontal_arrow),
            Create(horizontal_label),
            Create(horizontal_dot),
            FadeIn(horizontal_rectangle),
            self.camera.frame.animate.shift([0, -0.6*plane_square_size, 0]),
            nabla_i_movement_group.animate.shift([0, -0.6*plane_square_size, 0]),
            diagonal_explanation.animate.shift([0, -0.6*plane_square_size, 0]),
            diagonal_bullet.animate.shift([0, -0.6*plane_square_size, 0]),
            explanation_rectangle.animate.shift([0, -0.6*plane_square_size, 0]),
        )
        horizontal_explanation.shift([0, -0.6*plane_square_size, 0])
        horizontal_bullet.shift([0, -0.6*plane_square_size, 0])
        # If you move horizontally:
        self.play(Write(horizontal_explanation_if), Write(horizontal_bullet))
        self.play(Write(horizontal_explanation_a), Write(horizontal_explanation_b))
        self.wait(1)

        # Nabla condition group:
        nabla_condition_group.move_to([
            self.camera.frame.get_right()[0] + 1/2* get_len(nabla_condition_group),
            self.camera.frame.get_top()[1] - text_buff - 1/2*get_height(nabla_condition_group),
            self.camera.frame.get_center()[2]
        ])
        nabla_condition_group.save_state()
        diagonal_explanation_if_nabla.next_to(diagonal_explanation_if_if, RIGHT, buff=text_buff*3/4).shift([0, - 3/16 * text_buff, 0])
        horizontal_explanation_if_nabla.next_to(horizontal_explanation_if_if, RIGHT, buff=text_buff*3/4).shift([0, - 3/16 * text_buff, 0])
        self.play(nabla_condition_group.animate.shift([- get_len(nabla_condition_group) - text_buff, 0, 0]))
        self.wait(1)
        self.play(
            FadeOut(diagonal_explanation_if_move),
            FadeOut(horizontal_explanation_if_move),
            Write(diagonal_explanation_if_nabla),
            Write(horizontal_explanation_if_nabla)
        )
        self.next_section()
        self.wait(1)
        self.play(
            Restore(nabla_condition_group),
            FadeOut(plane),
            FadeOut(horizontal_arrow),
            FadeOut(horizontal_label),
            FadeOut(horizontal_rectangle),
            FadeOut(starting_label),
            FadeOut(starting_rectangle),
            FadeOut(explanation_rectangle),
            FadeOut(starting_dot),
            FadeOut(horizontal_dot),
            FadeOut(d1_d2_line_diagonally),
            diagonal_movement_group.animate.move_to([
                self.camera.frame.get_center()[0] - 1/4*get_len(self.camera.frame),
                self.camera.frame.get_center()[1] + 1/8 * get_height(self.camera.frame), self.camera.frame.get_center()[2]
            ]),
            horizontal_movement_group.animate.move_to([
                self.camera.frame.get_center()[0] + 1/4*get_len(self.camera.frame),
                self.camera.frame.get_center()[1] + 1/8 * get_height(self.camera.frame), self.camera.frame.get_center()[2]
            ]),
        )
        self.play(
            diagonal_movement_group.animate.shift([1/4*get_len(self.camera.frame), 0, 0]),
            horizontal_movement_group.animate.shift([1/4*get_len(self.camera.frame) + 1/2*get_len(horizontal_movement_group), 0, 0])
        )

        # Connecting nabla_i and nabla_{i+1}:
        nabla_i_start.move_to(nabla_i_plus.get_center()).scale(nabla_i_scale)
        self.play(nabla_i_start.animate.next_to(diagonal_movement_group, DOWN, buff=text_buff).scale(1/nabla_i_scale))

        nabla_i_plus_transformed.next_to(nabla_i_start, DOWN, buff=text_buff/2)
        nabla_i_copy.move_to(nabla_i_start.get_center()).shift([1/2*get_len(nabla_i_start) - 1/2*get_len(nabla_i_copy), 0, 0])
        nabla_i_start_equals.next_to(nabla_i_start, RIGHT, buff=text_buff/4)
        self.add(nabla_i_copy)
        self.play(
            nabla_i_copy.animate.shift([0, -text_buff/2 - get_height(nabla_i_copy), 0]),
            FadeIn(nabla_i_start_equals)
        )
        self.play(ReplacementTransform(nabla_i_copy, nabla_i_plus_transformed))
        nabla_i_opened_braces.next_to(nabla_i_plus_transformed, DOWN, buff=text_buff/2)
        nabla_i_plus_transformed_equals.next_to(nabla_i_plus_transformed, RIGHT, buff=text_buff/4)
        self.wait(1)
        self.play(
            ReplacementTransform(nabla_i_plus_transformed.copy(), nabla_i_opened_braces),
            FadeIn(nabla_i_plus_transformed_equals)
        )
        self.wait(1)
        nabla_i_opened_braces_copy.move_to(nabla_i_opened_braces.get_center()).shift([0, -text_buff/2 - get_height(nabla_i_opened_braces), 0])
        nabla_i_reordered.next_to(nabla_i_opened_braces, DOWN, buff=text_buff/2)
        nabla_i_opened_braces_equals.next_to(nabla_i_opened_braces, RIGHT, buff=text_buff/4)
        self.play(
            TransformMatchingShapes(nabla_i_opened_braces.copy(), nabla_i_opened_braces_copy),
            FadeIn(nabla_i_opened_braces_equals)
        )
        self.play(TransformMatchingTex(nabla_i_opened_braces_copy, nabla_i_reordered))
        self.wait(1)
        nabla_i_reordered_open_brace.next_to(nabla_i_reordered[1], LEFT, buff=text_buff/4)
        nabla_i_reordered_close_brace.next_to(nabla_i_reordered[4], RIGHT, buff=text_buff/4).match_y(nabla_i_reordered[0])
        self.play(
            FadeIn(nabla_i_reordered_open_brace),
            FadeIn(nabla_i_reordered_close_brace),
            nabla_i_reordered[0].animate.shift([-get_len(nabla_i_reordered_open_brace), 0, 0]),
            nabla_i_reordered[5].animate.shift([get_len(nabla_i_reordered_open_brace), 0, 0]),
            nabla_i_reordered[6].animate.shift([get_len(nabla_i_reordered_open_brace), 0, 0]),
        )
        self.next_section()
        self.wait(1)
        nabla_i_copy = nabla_i.copy()
        nabla_i_replacement_group = VGroup(nabla_i_reordered[1], nabla_i_reordered[2], nabla_i_reordered[3], nabla_i_reordered[4], nabla_i_reordered_open_brace, nabla_i_reordered_close_brace)
        replacement_nabla = Tex(r"$\boldsymbol{\nabla_i}$", font_size=text_size, color=GREEN).next_to(nabla_i_reordered[0], RIGHT, buff=text_buff/2)
        nabla_i_movement_group = VGroup(replacement_nabla, nabla_i_reordered[5], nabla_i_reordered[6])
        self.play(
            nabla_i_copy.animate.move_to([
                nabla_i_reordered_close_brace.get_left()[0] - 1/2*(get_len(nabla_i_copy)*1/nabla_i_scale),
                nabla_i_reordered.get_bottom()[1] - text_buff/2 - 1/2*(get_height(nabla_i_copy)*1/nabla_i_scale),
                nabla_i_copy.get_center()[2]
            ]).scale(1/nabla_i_scale)
        )
        self.play(
            FadeToColor(nabla_i_reordered[1], GREEN),
            FadeToColor(nabla_i_reordered[2], GREEN),
            FadeToColor(nabla_i_reordered[3], GREEN),
            FadeToColor(nabla_i_reordered[4], GREEN),
        )
        self.wait(1)
        self.play(
            ReplacementTransform(nabla_i_replacement_group, replacement_nabla),
            nabla_i_reordered[5].animate.shift([-get_len(nabla_i_replacement_group) + get_len(replacement_nabla) + text_buff/4, 0, 0]),
            nabla_i_reordered[6].animate.shift([-get_len(nabla_i_replacement_group) + get_len(replacement_nabla) + text_buff/4, 0, 0]),
            FadeOut(nabla_i_copy)
        )
        self.play(FadeToColor(replacement_nabla, WHITE))
        self.play(
            FadeOut(nabla_i_plus_transformed),
            FadeOut(nabla_i_plus_transformed_equals),
            FadeOut(nabla_i_start[1]),
            FadeOut(nabla_i_start[2]),
            FadeOut(nabla_i_start[3]),
            FadeOut(nabla_i_start[4]),
            FadeOut(nabla_i_start[5]),
            FadeOut(nabla_i_start_equals),
            FadeOut(nabla_i_opened_braces),
            FadeOut(nabla_i_opened_braces_equals),
            FadeOut(nabla_i_reordered[0]),
            nabla_i_movement_group.animate.next_to(nabla_i_start[0], RIGHT, buff=text_buff),
        )
        nabla_i_connection = VGroup(nabla_i_movement_group, nabla_i_start[0])
        diagonal_explanation_final = VGroup(diagonal_explanation_if_if, diagonal_explanation_if_nabla, diagonal_bullet, nabla_i_connection)
        self.play(
            FadeOut(diagonal_explanation_a),
            FadeOut(diagonal_explanation_b),
            nabla_i_connection.animate.next_to(diagonal_explanation_if_if, DOWN, buff=text_buff).shift([-1/2*get_len(diagonal_explanation_if_if) + 1/2*get_len(nabla_i_connection), 0, 0])
        )
        self.wait(1)
        self.play(
            diagonal_explanation_final.animate.move_to([
                self.camera.frame.get_left()[0] - 1/2*get_len(diagonal_explanation_final),
                diagonal_explanation_final.get_center()[1],
                diagonal_explanation_final.get_center()[2]
            ]),
            horizontal_movement_group.animate.shift([-1/2*get_len(self.camera.frame) - 1/2*get_len(horizontal_movement_group), 0, 0])
        )

        # For nabla < 0:

        nabla_horizontal_start.move_to(nabla_i_plus.get_center()).scale(nabla_i_scale)
        self.play(nabla_horizontal_start.animate.next_to(horizontal_movement_group, DOWN, buff=text_buff).scale(1/nabla_i_scale))

        nabla_horizontal_plus_transformed.next_to(nabla_horizontal_start, DOWN, buff=text_buff/2)
        nabla_horizontal_copy.move_to(nabla_horizontal_start.get_center()).shift([1/2*get_len(nabla_horizontal_start) - 1/2*get_len(nabla_horizontal_copy), 0, 0])
        nabla_horizontal_start_equals.next_to(nabla_horizontal_start, RIGHT, buff=text_buff/4)
        self.add(nabla_horizontal_copy)
        self.play(
            nabla_horizontal_copy.animate.shift([0, -text_buff/2 - get_height(nabla_horizontal_copy), 0]),
            FadeIn(nabla_horizontal_start_equals)
        )
        self.play(ReplacementTransform(nabla_horizontal_copy, nabla_horizontal_plus_transformed))
        nabla_horizontal_opened_braces.next_to(nabla_horizontal_plus_transformed, DOWN, buff=text_buff/2)
        nabla_horizontal_plus_transformed_equals.next_to(nabla_horizontal_plus_transformed, RIGHT, buff=text_buff/4)
        self.play(
            ReplacementTransform(nabla_horizontal_plus_transformed.copy(), nabla_horizontal_opened_braces),
            FadeIn(nabla_horizontal_plus_transformed_equals)
        )
        nabla_horizontal_opened_braces_copy.move_to(nabla_horizontal_opened_braces.get_center()).shift([0, -text_buff/2 - get_height(nabla_horizontal_opened_braces), 0])
        nabla_horizontal_reordered.next_to(nabla_horizontal_opened_braces, DOWN, buff=text_buff/2)
        nabla_horizontal_opened_braces_equals.next_to(nabla_horizontal_opened_braces, RIGHT, buff=text_buff/4)
        self.play(
            TransformMatchingShapes(nabla_horizontal_opened_braces.copy(), nabla_horizontal_opened_braces_copy),
            FadeIn(nabla_horizontal_opened_braces_equals)
        )
        self.play(TransformMatchingTex(nabla_horizontal_opened_braces_copy, nabla_horizontal_reordered))
        nabla_horizontal_reordered_open_brace.next_to(nabla_horizontal_reordered[1], LEFT, buff=text_buff/4)
        nabla_horizontal_reordered_close_brace.next_to(nabla_horizontal_reordered[4], RIGHT, buff=text_buff/4).match_y(nabla_horizontal_reordered[0])
        self.play(
            FadeIn(nabla_horizontal_reordered_open_brace),
            FadeIn(nabla_horizontal_reordered_close_brace),
            nabla_horizontal_reordered[0].animate.shift([-get_len(nabla_horizontal_reordered_open_brace), 0, 0]),
            nabla_horizontal_reordered[5].animate.shift([get_len(nabla_horizontal_reordered_open_brace), 0, 0]),
        )
        self.next_section()
        replacement_nabla = Tex(r"$\boldsymbol{\nabla_i}$", font_size=text_size, color=GREEN).next_to(nabla_horizontal_reordered[0], RIGHT, buff=text_buff/2)
        nabla_horizontal_copy = nabla_i.copy()
        nabla_horizontal_replacement_group = VGroup(nabla_horizontal_reordered[1], nabla_horizontal_reordered[2], nabla_horizontal_reordered[3], nabla_horizontal_reordered[4], nabla_horizontal_reordered_open_brace, nabla_horizontal_reordered_close_brace)
        nabla_horizontal_movement_group = VGroup(replacement_nabla, nabla_horizontal_reordered[5])
        self.play(
            nabla_horizontal_copy.animate.move_to([
                nabla_horizontal_reordered_close_brace.get_left()[0] - 1/2*(get_len(nabla_horizontal_copy)*1/nabla_i_scale),
                nabla_horizontal_reordered.get_bottom()[1] - text_buff/2 - 1/2*(get_height(nabla_horizontal_copy)*1/nabla_i_scale),
                nabla_horizontal_copy.get_center()[2]
            ]).scale(1/nabla_i_scale)
        )
        self.play(
            FadeToColor(nabla_horizontal_reordered[1], GREEN),
            FadeToColor(nabla_horizontal_reordered[2], GREEN),
            FadeToColor(nabla_horizontal_reordered[3], GREEN),
            FadeToColor(nabla_horizontal_reordered[4], GREEN),
        )
        self.play(
            ReplacementTransform(nabla_horizontal_replacement_group, replacement_nabla),
            nabla_horizontal_reordered[5].animate.shift([-get_len(nabla_horizontal_replacement_group) + get_len(replacement_nabla) + text_buff/4, 0, 0]),
            FadeOut(nabla_horizontal_copy)
        )
        self.play(FadeToColor(replacement_nabla, WHITE))
        self.play(
            FadeOut(nabla_horizontal_plus_transformed),
            FadeOut(nabla_horizontal_plus_transformed_equals),
            FadeOut(nabla_horizontal_start[1]),
            FadeOut(nabla_horizontal_start[2]),
            FadeOut(nabla_horizontal_start[3]),
            FadeOut(nabla_horizontal_start[4]),
            FadeOut(nabla_horizontal_start[5]),
            FadeOut(nabla_horizontal_start_equals),
            FadeOut(nabla_horizontal_opened_braces),
            FadeOut(nabla_horizontal_opened_braces_equals),
            FadeOut(nabla_horizontal_reordered[0]),
            nabla_horizontal_movement_group.animate.next_to(nabla_horizontal_start[0], RIGHT, buff=text_buff),
        )
        nabla_horizontal_connection = VGroup(nabla_horizontal_movement_group, nabla_horizontal_start[0])
        horizontal_explanation_final = VGroup(horizontal_explanation_if_if, horizontal_explanation_if_nabla, horizontal_bullet, nabla_horizontal_connection)
        self.play(
            FadeOut(horizontal_explanation_a),
            FadeOut(horizontal_explanation_b),
            nabla_horizontal_connection.animate.next_to(horizontal_explanation_if_if, DOWN, buff=text_buff).shift([-1/2*get_len(horizontal_explanation_if_if) + 1/2*get_len(nabla_horizontal_connection), 0, 0])
        )

        # Gathering everything together:
        self.next_section()
        self.wait(1)

        self.play(
            diagonal_explanation_final.animate.move_to([
                self.camera.frame.get_center()[0] - 1/4*get_len(self.camera.frame),
                self.camera.frame.get_center()[1] + 1/8 * get_height(self.camera.frame), self.camera.frame.get_center()[2]
            ]),
            horizontal_explanation_final.animate.move_to([
                self.camera.frame.get_center()[0] + 1/4*get_len(self.camera.frame),
                self.camera.frame.get_center()[1] + 1/8 * get_height(self.camera.frame), self.camera.frame.get_center()[2]
            ]),
        )
        self.wait(1)
        self.play(horizontal_explanation_final.animate.next_to(diagonal_explanation_final, DOWN, buff=text_buff/2).shift([-1/2*get_len(diagonal_explanation_final) + 1/2*get_len(horizontal_explanation_final), 0, 0]))
        self.play(
            FadeOut(nabla_i),
            FadeOut(nabla_i_plus),
            FadeOut(nabla_i_bigger_rectangle),
            nabla_i_e.animate.scale(1/nabla_i_scale).next_to(diagonal_explanation_final, UP, buff=2*text_buff + get_height(nabla_simplified)).shift([-1/2*get_len(diagonal_explanation_final) + 1/2*(get_len(nabla_i_e)*1/nabla_i_scale) + get_len(diagonal_bullet), 0, 0]),
            nabla_simplified.animate.scale(1/nabla_i_scale).next_to(diagonal_explanation_final, UP, buff=text_buff).shift([-1/2*get_len(diagonal_explanation_final) + 1/2*(get_len(nabla_simplified)*1/nabla_i_scale) + get_len(diagonal_bullet), 0, 0]),
            FadeOut(diagonal_bullet),
            FadeOut(horizontal_bullet),
            FadeOut(horizontal_explanation_if_nabla[1]),
            FadeOut(diagonal_explanation_if_nabla[1]),
        )
        diagonal_explanation_final.remove(diagonal_bullet)
        horizontal_explanation_final.remove(horizontal_bullet)
        final_brace = BraceBetweenPoints(nabla_i_movement_group.get_critical_point(UL), nabla_i_movement_group.get_critical_point(DL) + [0, -1/2*text_buff - get_height(nabla_horizontal_connection), 0], direction=[-1, 0, 0])
        self.play(
            FadeOut(nabla_horizontal_start[0]),
            diagonal_explanation_if_if.animate.next_to(nabla_i_movement_group, RIGHT, buff=text_buff),
            diagonal_explanation_if_nabla[0].animate.next_to(nabla_i_movement_group, RIGHT, buff=2*text_buff + get_len(diagonal_explanation_if_if)),

            horizontal_explanation_if_if.animate.next_to(nabla_i_movement_group, RIGHT, buff=text_buff).shift([0, -get_height(diagonal_explanation_if_nabla[0])-1/2*text_buff, 0]),
            horizontal_explanation_if_nabla[0].animate.next_to(nabla_i_movement_group, RIGHT, buff=2*text_buff + get_len(diagonal_explanation_if_if)).shift([0, -get_height(diagonal_explanation_if_nabla[0])-1/2*text_buff, 0]),

            nabla_horizontal_movement_group.animate.next_to(nabla_i_movement_group, DOWN, buff=1/2*text_buff).shift([-1/2*get_len(nabla_i_movement_group) + 1/2*get_len(nabla_horizontal_movement_group), 0, 0]),
            Create(final_brace),
            nabla_i_start[0].animate.next_to(final_brace.get_tip(), LEFT, buff=text_buff/2)
        )
        self.play(
            nabla_simplified.animate.next_to(nabla_i_start[0], UP, buff=get_height(nabla_i_movement_group)+1/4*text_buff).shift([-1/2*get_len(nabla_i_start[0]) + 1/2*get_len(nabla_simplified), 0, 0]),
            nabla_i_e.animate.next_to(nabla_i_start[0], UP, buff=get_height(nabla_i_movement_group)+3/4*text_buff+get_height(nabla_simplified)).shift([-1/2*get_len(nabla_i_start[0]) + 1/2*get_len(nabla_i_e), 0, 0])
        )
        final_group = VGroup(
            nabla_i_e,
            nabla_simplified,
            nabla_i_start[0],
            final_brace,
            nabla_i_movement_group,
            nabla_horizontal_movement_group,
            diagonal_explanation_if_if,
            diagonal_explanation_if_nabla[0],
            horizontal_explanation_if_if,
            horizontal_explanation_if_nabla[0]
        )
        self.play(final_group.animate.move_to([
            final_group.get_center()[0],
            self.camera.frame.get_center()[1] + 1/4*get_height(self.camera.frame),
            final_group.get_center()[2]
        ]))



        self.wait(3)

class EightthScene(MovingCameraScene):
    def construct(self):
        text_size = 20

        triangle_octant_size = 3
        triangle_octant_stroke = 3

        triangle_octant_one_positions = [
            ORIGIN,
            [triangle_octant_size, 0, 0],
            [triangle_octant_size, triangle_octant_size,  0]
        ]
        triangle_octant_one = Polygon(*triangle_octant_one_positions, color=WHITE, stroke_width=triangle_octant_stroke)
        
        triangle_octant_two_positions = [
            ORIGIN,
            [triangle_octant_size, triangle_octant_size,  0],
            [0, triangle_octant_size, 0]
        ]
        triangle_octant_two = Polygon(*triangle_octant_two_positions, color=WHITE, stroke_width=triangle_octant_stroke)

        triangle_octant_three_positions = [
            ORIGIN,
            [0, triangle_octant_size, 0],
            [-triangle_octant_size, triangle_octant_size,  0]
        ]
        triangle_octant_three = Polygon(*triangle_octant_three_positions, color=WHITE, stroke_width=triangle_octant_stroke)

        triangle_octant_four_positions = [
            ORIGIN,
            [-triangle_octant_size, triangle_octant_size,  0],
            [-triangle_octant_size, 0, 0]
        ]
        triangle_octant_four = Polygon(*triangle_octant_four_positions, color=WHITE, stroke_width=triangle_octant_stroke)
        
        triangle_octant_five_positions = [
            ORIGIN,
            [-triangle_octant_size, 0, 0],
            [-triangle_octant_size, -triangle_octant_size,  0]
        ]
        triangle_octant_five = Polygon(*triangle_octant_five_positions, color=WHITE, stroke_width=triangle_octant_stroke)

        triangle_octant_six_positions = [
            ORIGIN,
            [-triangle_octant_size, -triangle_octant_size,  0],
            [0, -triangle_octant_size, 0]
        ]
        triangle_octant_six = Polygon(*triangle_octant_six_positions, color=WHITE, stroke_width=triangle_octant_stroke)

        triangle_octant_seven_positions = [
            ORIGIN,
            [0, -triangle_octant_size, 0],
            [triangle_octant_size, -triangle_octant_size,  0]
        ]
        triangle_octant_seven = Polygon(*triangle_octant_seven_positions, color=WHITE, stroke_width=triangle_octant_stroke)

        triangle_octant_eight_positions = [
            ORIGIN,
            [triangle_octant_size, -triangle_octant_size,  0],
            [triangle_octant_size, 0, 0]
        ]
        triangle_octant_eight = Polygon(*triangle_octant_eight_positions, color=WHITE, stroke_width=triangle_octant_stroke)

        triangles_octant = VGroup(
            triangle_octant_one,
            triangle_octant_two,
            triangle_octant_three,
            triangle_octant_four,
            triangle_octant_five,
            triangle_octant_six,
            triangle_octant_seven,
            triangle_octant_eight
        )

        triangle_octant_labels = Tex(
            r"$1$",
            r"$2$",
            r"$3$",
            r"$4$",
            r"$5$",
            r"$6$",
            r"$7$",
            r"$8$",
            font_size=text_size
        )

        octant_label_distance_from_origin = 0.7
        octant_label_starting_angle = PI/8
        octant_label_angle = octant_label_starting_angle
        for i in range(0, 8):
            triangle_octant_labels[i].move_to([
                octant_label_distance_from_origin * np.cos(octant_label_angle),
                octant_label_distance_from_origin * np.sin(octant_label_angle),
                triangle_octant_labels[i].get_center()[2]
            ])
            octant_label_angle += PI/4
        
        octant_arrow_length = 0.5
        octant_arrow_distance = 2.2
        text_buff = 0.1

        octant_base_arrow_group = VGroup(
            Arrow(start=ORIGIN, end=[octant_arrow_length, 0, 0], buff=0),
            Arrow(start=ORIGIN, end=[0, octant_arrow_length, 0], buff=0),
            Arrow(start=ORIGIN, end=[octant_arrow_length, octant_arrow_length, 0], buff=0),
            Tex(r"$a$", font_size=text_size).move_to([octant_arrow_length, - text_buff, 0]),
            Tex(r"$b$", font_size=text_size).move_to([-text_buff, octant_arrow_length, 0]),
            Tex(r"$m_1$", font_size=text_size).move_to([1/2*octant_arrow_length, -text_buff, 0]),
            Tex(r"$m_2$", font_size=text_size).move_to([octant_arrow_length/2 - text_buff, octant_arrow_length/2, 0])
        )

        octant_arrow_group = VGroup()
        octant_arrow_angle = PI/8

        for i in range(0, 8):
            # if i == 3:
            #     octant_arrow_group.add(octant_base_arrow_group.copy().rotate(PI/2*(i % 2 + int(i/2)), about_point=ORIGIN).move_to([
            #         octant_arrow_distance * np.cos(octant_arrow_angle),
            #         octant_arrow_distance * np.sin(octant_arrow_angle), 0
            #     ]))
            if i % 2 == 0:
                octant_arrow_group.add(octant_base_arrow_group.copy().rotate(PI/2*(i % 2 + int(i/2)), about_point=ORIGIN).move_to([
                    octant_arrow_distance * np.cos(octant_arrow_angle),
                    octant_arrow_distance * np.sin(octant_arrow_angle), 0
                ]))
            else:
                octant_arrow_group.add(octant_base_arrow_group.copy().flip().rotate(PI/2, about_point=ORIGIN).move_to([
                    octant_arrow_distance * np.cos(octant_arrow_angle),
                    octant_arrow_distance * np.sin(octant_arrow_angle), 0
                ]))
            octant_arrow_angle += PI/4


        ###############################ANIMATIONS###############################

        self.play(
            Create(triangles_octant),
            Write(triangle_octant_labels),
            Create(octant_arrow_group)
        )


        self.wait(3)


