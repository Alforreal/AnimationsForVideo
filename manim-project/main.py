import time
from manim import *
import numpy as np

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
            # p_name = Tex(r"$\boldsymbol{P (a_1, b_1)}$", font_size = 11).move_to(plane.c2p(0.8, 1.2)) // For later use

            p_stuff = VGroup(p_dot, p_name)
            p_stuff.set_z_index(4)

            # R point
            r_dot = Dot(plane.c2p(2, 1), radius= 0.04, color=GREEN)
            r_name = Tex(r"$\boldsymbol{R}$", font_size = 11).move_to(plane.c2p(2.1, 0.9))
            # r_name = Tex(r"$\boldsymbol{R (a_1+1, b_1)}$", font_size = 11).move_to(plane.c2p(2.2, 0.8)) // For later use

            r_stuff = VGroup(r_dot, r_name)
            r_stuff.set_z_index(4)

            # Q point
            q_dot = Dot(plane.c2p(2, 2), radius= 0.04, color=GREEN)
            q_name = Tex(r"$\boldsymbol{Q}$", font_size = 11).move_to(plane.c2p(2.1, 2.1))
            # q_name = Tex(r"$\boldsymbol{Q (a_1+1, b_1 + 1)}$", font_size = 11).move_to(plane.c2p(2.2, 2.2)) // For later use


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
            if_r_greater_q_if = Tex(r"$\boldsymbol{if}$", font_size=11).next_to(rq_difference_text, DOWN, buff=0.05)
            if_r_greater_q_rq = Tex(r"$\boldsymbol{r-q}$", font_size=11).next_to(if_r_greater_q_if, RIGHT, buff=0.05)
            if_r_greater_q_sign = Tex(r"$\boldsymbol{>}$", font_size=11).next_to(if_r_greater_q_rq, RIGHT, buff=0.05)
            if_r_greater_q_move = Tex(r"$\boldsymbol{0\rightarrow move\;diagonally}$", font_size=11).next_to(if_r_greater_q_sign, RIGHT, buff=0.05)

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
            if_r_less_q_move = Tex(r"$\boldsymbol{0\rightarrow move\;horizontally}$", font_size=11).next_to(if_r_less_q_sign, RIGHT, buff=0.05)
            
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

            fraction_offset = 0.05

            r_fraction_text = Tex(r"$\boldsymbol{r}$", font_size=11)
            rs_fraction_text = Tex(r"$\boldsymbol{RS}$", font_size=11)

            r_rs_fraction_line = Line(
                start=[equals_text.get_left()[0] - (rs_fraction_text.get_right()[0] - rs_fraction_text.get_left()[0]) - fraction_offset, equals_text.get_center()[1], equals_text.get_center()[2]],
                end=[equals_text.get_left()[0] - fraction_offset, equals_text.get_center()[1], equals_text.get_center()[2]],
                color=WHITE,
                stroke_width=0.5
            )

            r_fraction_text.move_to([
                r_rs_fraction_line.get_center()[0],
                r_rs_fraction_line.get_center()[1] + (r_fraction_text.get_top()[1] - r_fraction_text.get_bottom()[1])/2 + fraction_offset/2,
                r_rs_fraction_line.get_center()[2]])
            rs_fraction_text.move_to([
                r_rs_fraction_line.get_center()[0],
                r_rs_fraction_line.get_center()[1] - (rs_fraction_text.get_top()[1] - rs_fraction_text.get_bottom()[1])/2 - fraction_offset/2,
                r_rs_fraction_line.get_center()[2]
            ])

            r_rs_group = VGroup(r_rs_fraction_line, r_fraction_text, rs_fraction_text)
            r_rs_group.set_z_index(3)

            # q/QS:
            q_fraction_text = Tex(r"$\boldsymbol{q}$", font_size=11)
            qs_fraction_text = Tex(r"$\boldsymbol{QS}$", font_size=11)

            q_qs_fraction_line = Line(
                start=[equals_text.get_right()[0] + fraction_offset, equals_text.get_center()[1], equals_text.get_center()[2]],
                end=[equals_text.get_right()[0] + (qs_fraction_text.get_right()[0] - qs_fraction_text.get_left()[0]) + fraction_offset, equals_text.get_center()[1], equals_text.get_center()[2]],
                color=WHITE,
                stroke_width=0.5
            )

            q_fraction_text.move_to([
                q_qs_fraction_line.get_center()[0],
                q_qs_fraction_line.get_center()[1] + (q_fraction_text.get_top()[1] - q_fraction_text.get_bottom()[1])/2 + fraction_offset/2,
                q_qs_fraction_line.get_center()[2]
            ])
            qs_fraction_text.move_to([
                q_qs_fraction_line.get_center()[0],
                q_qs_fraction_line.get_center()[1] - (qs_fraction_text.get_top()[1] - qs_fraction_text.get_bottom()[1])/2 - fraction_offset/2,
                q_qs_fraction_line.get_center()[2]
            ])

            q_qs_group = VGroup(q_fraction_text, qs_fraction_text, q_qs_fraction_line)

            # r*QS = q*RS

            r_qs_multiplication = Tex(r"$\times$", font_size=11)
            r_qs_multiplication.move_to([
                equals_text.get_left()[0] - (qs_fraction_text.get_right()[0] - qs_fraction_text.get_left()[0]) - fraction_offset - (r_qs_multiplication.get_right()[0] - r_qs_multiplication.get_left()[0])/2,
                equals_text.get_center()[1], equals_text.get_center()[2]
            ])
            
            q_rs_multiplication = Tex(r"$\times$", font_size=11)
            q_rs_multiplication.move_to([
                equals_text.get_right()[0] + (q_fraction_text.get_right()[0] - q_fraction_text.get_left()[0]) + fraction_offset + (q_rs_multiplication.get_right()[0] - q_rs_multiplication.get_left()[0])/2,
                equals_text.get_center()[1], equals_text.get_center()[2]
            ])

            # r = q*RS/QS
            q_rs_group = VGroup(q_fraction_text, q_rs_multiplication, rs_fraction_text)
            q_rs_fraction_line = Line(
                start=[equals_text.get_right()[0] + fraction_offset/2, equals_text.get_center()[1], equals_text.get_center()[2]],
                end=[
                    equals_text.get_right()[0] + 1.5*fraction_offset + (rs_fraction_text.get_right()[0]-rs_fraction_text.get_left()[0]) + (q_rs_multiplication.get_right()[0]-q_rs_multiplication.get_left()[0]) + (q_fraction_text.get_right()[0]-q_fraction_text.get_left()[0]),
                    equals_text.get_center()[1], equals_text.get_center()[2]
                ],
                color=WHITE,
                stroke_width=0.5
            )

            # r/q = RS/QS
            rs_qs_fraction_line = Line(
                start=[equals_text.get_right()[0] + fraction_offset, equals_text.get_center()[1], equals_text.get_center()[2]],
                end=[equals_text.get_right()[0] + (rs_fraction_text.get_right()[0] - rs_fraction_text.get_left()[0]) + fraction_offset, equals_text.get_center()[1], equals_text.get_center()[2]],
                color=WHITE,
                stroke_width=0.5
            )
            r_q_fraction_line = Line(
                start=[equals_text.get_left()[0] - fraction_offset - (q_fraction_text.get_right()[0] - q_fraction_text.get_left()[0]), equals_text.get_center()[1], equals_text.get_center()[2]],
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
                end=[equals_text.get_right()[0] + (q_prime_text.get_right()[0] - q_prime_text.get_left()[0]) + fraction_offset, equals_text.get_center()[1], equals_text.get_center()[2]],
                color=WHITE,
                stroke_width=0.5
            )

            r_prime_text.move_to([
                r_prime_q_fraction_line.get_center()[0],
                r_prime_q_fraction_line.get_top()[1] + fraction_offset + (r_prime_text.get_top()[1] - r_prime_text.get_bottom()[1])/2,
                r_prime_text.get_center()[2]
            ])
            q_prime_text.move_to([
                r_prime_q_fraction_line.get_center()[0],
                r_prime_q_fraction_line.get_bottom()[1] - (fraction_offset - 0.02)  - (q_prime_text.get_top()[1] - q_prime_text.get_bottom()[1])/2,
                r_prime_text.get_center()[2]
            ])

            r_prime_q_group = VGroup(r_prime_text, r_prime_q_fraction_line, q_prime_text)

            #                                                                       ANIMATIONS
            # self.next_section(skip_animations=True)
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

            # self.next_section(skip_animations=True)

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

            # self.next_section(skip_animations=True)
            
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
            # self.next_section(skip_animations=True)
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
            self.play(
                rq_difference_label.animate.move_to([
                    rq_difference_label.get_center()[0],
                    rq_difference_label.get_center()[1] - 0.01, # Nudge for aesthetic reasons, without it r-q is a not in center
                    rq_difference_label.get_center()[2]
                ])
            )
            
            # Transitioning to Scene 4:
            self.play(
                Unwrite(r_len_text),
                Unwrite(q_len_text),
                Unwrite(if_r_greater_q),
                Unwrite(if_r_less_q),
                Unwrite(curly_brace_if_r),
                Uncreate(text_rectangle),
                rq_nabla_temp_group.animate.move_to(rq_nabla_coords),
                Create(rq_nabla_rectangle)
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
            self.next_section()

            self.play(Write(angle_label_group))
            self.wait(1)
            shift_value = RIGHT * 1
            self.play(
                self.camera.frame.animate.shift(shift_value),
                rq_nabla_group.animate.shift(shift_value),
                ReplacementTransform(angle_label_group, alpha_is_beta)
            )
            self.wait(1)
            self.play(
                beta_text.animate(run_time=0.7, rate_func=smooth).move_to([
                    beta_text.get_center()[0] + (beta_sine_sine.get_right()[0] - beta_sine_sine.get_left()[0]),
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
                    r_qs_multiplication.get_left()[0] - (r_fraction_text.get_right()[0] - r_fraction_text.get_left()[0])/2 - fraction_offset/2,
                    equals_text.get_center()[1], r_fraction_text.get_center()[2]
                ]),
                q_fraction_text.animate.move_to([
                    equals_text.get_right()[0] + (q_fraction_text.get_right()[0] - q_fraction_text.get_left()[0])/2 + fraction_offset/2,
                    equals_text.get_center()[1], q_fraction_text.get_center()[2]
                ]),
                rs_fraction_text.animate.move_to([
                    q_rs_multiplication.get_right()[0] + (rs_fraction_text.get_right()[0] - rs_fraction_text.get_left()[0])/2 + fraction_offset/2,
                    equals_text.get_center()[1], rs_fraction_text.get_center()[2]
                ]),
                qs_fraction_text.animate.move_to([
                    equals_text.get_left()[0] - (qs_fraction_text.get_right()[0] - qs_fraction_text.get_left()[0])/2 - fraction_offset/2,
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
                    q_rs_fraction_line.get_top()[1] + (rs_fraction_text.get_top()[1] - rs_fraction_text.get_bottom()[1])/2 + fraction_offset/2,
                    q_rs_group.get_center()[2]
                ]),
                Create(q_rs_fraction_line),
                qs_fraction_text.animate.move_to([
                    q_rs_fraction_line.get_center()[0],
                    q_rs_fraction_line.get_bottom()[1] - (qs_fraction_text.get_top()[1] - qs_fraction_text.get_bottom()[1])/2 - fraction_offset/2,
                    qs_fraction_text.get_center()[2]
                ]),
                r_fraction_text.animate.move_to([
                    equals_text.get_left()[0] - (r_fraction_text.get_right()[0] - r_fraction_text.get_left()[0]) - fraction_offset/2,
                    r_fraction_text.get_center()[1], r_fraction_text.get_center()[2]
                ])
            )
            self.wait(0.5)
            self.play(
                r_fraction_text.animate.move_to([
                    r_q_fraction_line.get_center()[0],
                    r_q_fraction_line.get_top()[1] + (r_fraction_text.get_top()[1] - r_fraction_text.get_bottom()[1])/2 + fraction_offset/2,
                    r_fraction_text.get_center()[2]
                ]),
                Create(r_q_fraction_line),
                FadeOut(q_rs_multiplication),
                q_fraction_text.animate.move_to([
                    r_q_fraction_line.get_center()[0],
                    r_q_fraction_line.get_bottom()[1] - (q_fraction_text.get_top()[1] - q_fraction_text.get_bottom()[1])/2 - fraction_offset/2,
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
                    r_q_fraction_line.get_end()[0] - (r_prime_q_fraction_line.get_right()[0] - r_prime_q_fraction_line.get_left()[0]),
                    equals_text.get_center()[1],
                    equals_text.get_center()[2]
                ], r_q_fraction_line.get_end()
                ),
                q_fraction_text.animate.move_to([
                    r_q_fraction_line.get_end()[0] - (r_prime_q_fraction_line.get_right()[0] - r_prime_q_fraction_line.get_left()[0])/2,
                    q_prime_text.get_bottom()[1] + (q_fraction_text.get_top()[1] - q_fraction_text.get_bottom()[1])/2,
                    q_fraction_text.get_center()[2]
                ]),
                r_fraction_text.animate.move_to([
                    r_q_fraction_line.get_end()[0] - (r_prime_q_fraction_line.get_right()[0] - r_prime_q_fraction_line.get_left()[0])/2,
                    r_prime_text.get_bottom()[1] + (r_fraction_text.get_top()[1] - r_fraction_text.get_bottom()[1])/2,
                    r_fraction_text.get_center()[2]
                ])
            )

            self.wait(3)

            
            

        def interpolate_y_on_line(self, line, x_value, plane):
            start = line.get_start()
            end = line.get_end()
            start_coords = plane.p2c(start)
            end_coords = plane.p2c(end)
            if end_coords[0] - start_coords[0] == 0:
                return start_coords[1]
            t = (x_value - start_coords[0]) / (end_coords[0] - start_coords[0])
            return (1 - t) * start_coords[1] + t * end_coords[1]



