import time
from manim import *


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
            p_name = Tex(r"$\boldsymbol{P (a_1, b_1)}$", font_size = 11).move_to(plane.c2p(0.8, 1.2))

            p_stuff = VGroup(p_dot, p_name)
            p_stuff.set_z_index(4)

            # R point
            r_dot = Dot(plane.c2p(2, 1), radius= 0.04, color=GREEN)
            r_name = Tex(r"$\boldsymbol{R (a_1+1, b_1)}$", font_size = 11).move_to(plane.c2p(2.2, 0.8))

            r_stuff = VGroup(r_dot, r_name)
            r_stuff.set_z_index(4)

            # Q point
            q_dot = Dot(plane.c2p(2, 2), radius= 0.04, color=GREEN)
            q_name = Tex(r"$\boldsymbol{Q (a_1+1, b_1 + 1)}$", font_size = 11).move_to(plane.c2p(2.2, 2.2))

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

            s_name = Tex(r"$\boldsymbol{S (a_1 + 1, c)}$", font_size = 11)

            s_name.add_updater(lambda s: s.next_to(s_dot.get_center(), RIGHT, buff = 0.09))

            s_stuff = VGroup(s_dot, s_name)
            s_stuff.set_z_index(4)

            # R or Q?
            line_to_r = DashedLine(start = p_dot.get_center(), end = r_dot.get_center(), color = WHITE, dash_length = 0.1, dashed_ratio = 0.5, stroke_width = 1)
            line_to_q = DashedLine(start = p_dot.get_center(), end = q_dot.get_center(), color = WHITE, dash_length = 0.1, dashed_ratio = 0.5, stroke_width = 1)
            dashed_rq = VGroup(line_to_q, line_to_r)
            dashed_rq.set_z_index(3)

            #Triangles 

            # projection_point_r = d1d2_line.get_projection(r_dot.get_center())
            # projection_point_q = d1d2_line.get_projection(q_dot.get_center())

            projection_r = always_redraw(lambda: Line(start = r_dot.get_center(), end = d1d2_line.get_projection(r_dot.get_center()), color = ORANGE, stroke_width = 1))

            # projection_r.add_updater(lambda line: line.put_start_and_end_on(
            #     r_dot.get_center(), d1d2_line.get_projection(r_dot.get_center())
            # ))

            projection_q = always_redraw(lambda: Line(start = q_dot.get_center(), end = d1d2_line.get_projection(q_dot.get_center()), color = ORANGE, stroke_width = 1))
            # projection_q.add_updater(lambda line: line.put_start_and_end_on(
            #     q_dot.get_center(), d1d2_line.get_projection(q_dot.get_center())
            # ))

            line_QR = Line(start = q_dot.get_center(), end = r_dot.get_center(), color = ORANGE, stroke_width = 1.7)

            little_r_name = Tex(r"$\boldsymbol{r}$", font_size = 10).next_to(projection_r.get_center(), DOWN+LEFT, buff=0.01 )
            little_r_name.add_updater(lambda name: name.next_to(projection_r.get_center(), DOWN+LEFT, buff=0.01 ))

            little_q_name = Tex(r"$\boldsymbol{q}$", font_size = 10).next_to(projection_q.get_center(), UP+RIGHT, buff=0.01 )
            little_q_name.add_updater(lambda name: name.next_to(projection_q.get_center(), DOWN+LEFT, buff=0.01 ))

            

            # r_part_from_original = Line(start = projection_point_r, end = s_dot.get_center(), color = ORANGE)
            # q_part_from_original = Line(start = projection_point_q, end = s_dot.get_center(), color = ORANGE)
            # parts = VGroup(r_part_from_original, q_part_from_original, line_QR)
            # parts.set_z_index(3)

            projections = VGroup(projection_r, projection_q)
            projections.set_z_index(2)

            right_angle_r = always_redraw(lambda: RightAngle(
            d1d2_line,            
            projection_r,   
            length=0.07, 
            stroke_width = 1,          
            quadrant=(1, -1),      
            color=ORANGE
            ))

            right_angle_q = always_redraw(lambda: RightAngle(
            d1d2_line,            
            projection_q,   
            length=0.07, 
            stroke_width = 1,          
            quadrant=(-1, -1),      
            color=ORANGE
            ))


            #Calculate projection valeus
            r_label = Tex(r"\textbf{r = }", font_size=11)
            r_value = DecimalNumber(0, num_decimal_places=2, font_size=11)

            r_len_text = VGroup(r_label, r_value).arrange(RIGHT, buff=0.05)
            r_len_text.move_to(plane.c2p(3.8, 1.7), aligned_edge=RIGHT)

            r_value.add_updater(lambda r: r.set_value(projection_r.get_length()))


            q_label = Tex(r"\textbf{q = }", font_size=11)
            q_value = DecimalNumber(0, num_decimal_places=2, font_size=11)

            q_len_text = VGroup(q_label, q_value).arrange(RIGHT, buff=0.05)
            q_len_text.next_to(r_len_text, DOWN, buff = 0.1)

            q_value.add_updater(lambda q: q.set_value(projection_q.get_length()))
 
            #                                                                       ANIMATIONS

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

            #                                                                  Third Scene                                                                                    #

            self.play(self.camera.frame.animate.move_to(plane.c2p(2, 1.5)).scale(0.45), run_time=2)
            self.wait(1.5)

            #P
            self.play(Create(p_dot), Write(p_name))

            self.wait(1.5)

            #R and Q
            self.play(Create(r_dot), Write(r_name), Create(q_dot), Write(q_name))
            self.wait(1.5)

            #S
            self.play(Create(s_dot), Write(s_name))

            #R or Q? 

            self.play(Create(line_to_r), Create(line_to_q))
            self.wait(1.5)

            self.play(Uncreate(line_to_r), Uncreate(line_to_q))
            self.wait(1.5)
            self.play(Create(projections))
            self.wait(1)
            self.play(Write(little_q_name), Write(little_r_name))

            self.play(Create(right_angle_r), Create(right_angle_q))
            self.play(Write(r_len_text), Write(q_len_text))
            self.wait(1)

            self.play(d2_after_traverse.animate.move_to(plane.c2p(5, 3.3)), run_time=3)
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



