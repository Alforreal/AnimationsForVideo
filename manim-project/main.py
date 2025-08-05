import time
from manim import *
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

        d1 = Dot(plane.c2p(d1_coord[0], d1_coord[1]), radius= 0.07, color=WHITE)

        d2 = Dot(plane.c2p(d2_coord[0], d2_coord[1]), radius= 0.07,color=WHITE)

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
            plane = NumberPlane(x_range=(0, 5, 1), y_range=(0, 3, 1))
            upper_line = Line(start=plane.c2p(0, 3), end=plane.c2p(5, 3), stroke_width= 2, color=WHITE)
            right_line = Line(start=plane.c2p(5, 3), end=plane.c2p(5,0), stroke_width= 2, color=WHITE)
            box = VGroup(plane, upper_line, right_line)
            box.set_z_index(1)

            #Square
            square = Square(color = BLUE, side_length= 1, stroke_width = 1.7)
            square.move_to(plane.c2p(0.5, 0.5))
            square.set_z_index(1)

            #Dot
            dot = Dot(plane.c2p(0, 0), radius= 0.04, color=RED)
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


            #Move Camera
            self.camera.frame.move_to(square) 
            self.wait(2)

            #D1D2
            d1_coord = [0, 0, 0]
            d2_coord = [5, 3, 0]
            d1 = Dot(plane.c2p(d1_coord[0], d1_coord[1]), radius= 0.07, color=WHITE)

            d2 = Dot(plane.c2p(d2_coord[0], d2_coord[1]), radius= 0.07, color=WHITE)

            d1_text = Text("D1", font_size=21).next_to(d1, DOWN * 0.7)
            d2_text = Text("D2", font_size=21).next_to(d2, UP * 0.5)

            x1y1_text = Text("(x1y1)", font_size=21).next_to(d1, DOWN * 0.7)
            x2y2_text = Text("(x2y2)", font_size=21).next_to(d2, UP * 0.3)


            d1d2_line= Line(start=d1.get_center(), end=d2.get_center(), color=WHITE)
            line_stuff = VGroup(d1, d2, d1d2_line, d1_text, d2_text)
            d1d2_names = VGroup(d1_text, d2_text)
            xy_group = VGroup(x1y1_text, x2y2_text)

            line_stuff.set_z_index(3)
            d1d2_names.set_z_index(3)
            xy_group.set_z_index(3)

            #Change_of_coordinates
            d1_new_coord_text = Text("(0, 0)", font_size=21).next_to(d1, DOWN * 0.6)
            d2_new_coord_text1 = Text("(x2-x1, y2-y1)", font_size=21).next_to(d2, UP * 0.3)
            d2_new_coord_text2 = Text("(Δa, Δb)", font_size=21).next_to(d2, UP * 0.3)

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
            self.play(self.camera.frame.animate.scale(2).move_to(ORIGIN), Unwrite(all_text_in_sqare),run_time=2)
            self.play(Create(box), run_time = 4)

            #D1D2 Animation
            self.play(Create(d1), Create(d2), run_time=1)
            self.wait(2)
            self.play(Create(d1d2_line), run_time=2)
            self.wait(2)
            self.play(Write(d1d2_names), run_time=1)

            self.play(d1_text.animate.shift(LEFT * 0.333), d2_text.animate.shift(LEFT * 0.275), run_time=2)
            self.play(Write(x1y1_text.shift(RIGHT * 0.3)), Write(x2y2_text.shift(RIGHT * 0.4)), run_time=1)
            self.wait(1.5)

            #Animation_Change_of_coordinates
            self.play(Unwrite(x1y1_text), run_time=1)
            self.wait(0.2)
            self.play(Write(d1_new_coord_text.shift(RIGHT * 0.3)), run_time=1)
            #self.play(Transform(x1y1_text, d1_new_coord_text.shift(RIGHT * 0.3)), run_time=1)
            self.play(Unwrite(x2y2_text), run_time=1)
            self.wait(0.2)
            self.play(Write(d2_new_coord_text1.shift(RIGHT * 0.9)), run_time=1)
            #self.play(Transform(x2y2_text, d2_new_coord_text1.shift(RIGHT * 0.9)), run_time=1)
            self.wait(1.5)
            #self.play(Transform(d2_new_coord_text1, d2_new_coord_text2.shift(RIGHT * 0.5)), run_time=1)
            self.play(Unwrite(d2_new_coord_text1), run_time=1)
            self.wait(0.2)
            self.play(Write(d2_new_coord_text2.shift(RIGHT * 0.5)))

            self.wait(3)



