from furniture_design.order import Order
from furniture_design.cabinets.Kitchen.kitchen import *
from furniture_design.cabinets.Dressing.dressing import *
from furniture_design.cabinets.elements.board import *
from furniture_design.cabinets.elements.accessory import *
from manufacturing.generate_files import generate_manufacturing_files
import os

order_data = {
    "client": "George Mihes",
    "Client Proficut": "Bogdan Urs",
    "Tel Proficut": "0740472185",
    "Transport": "Da",
    "Adresa": "Mosnita Veche, str. Borsa, Nr. 38",
    "h_bucatarie": 2450,
    "h_faianta_top": 1470,
    "h_faianta_base": 900,
    "depth_base": 600,
    "top_height": 700,
    "top_height_2": 0,
    "top_depth": 400,
    "top_depth_2": 0,
    "blat_height": 880,
    "cuptor_height": 600,
    "MsV_height_min": 820,
    "MsV_height_max": 900,
    "material_pal": "Alb W962ST2", #TODO confirm materials
    "material_pal_2": "Smoke Green K521 SU",
    "material_front": "A34R3", #TODO confirm materials
    "material_blat": "Stejar Halifax 600", #TODO confirm materials
    "material_pfl": "Alb", #TODO confirm materials
    "h_rate": 70,
    "h_proiect": 8,
    "discount": 100,
    "nr_electrocasnice": 5,
}

rules = {
    "thick_pal": 18,
    "thick_front": 18,
    "thick_blat": 38,
    "height_legs": 100,
    "general_width": 600,
    "width_blat": 600,
    "gap_spate": 50,
    "gap_fata": 50,
    "gap_front": 2,
    "cant_general": 1,
    "cant_pol": 2,
    "cant_separator": 1,
    "pol_depth": 20
}

blat_height = order_data["blat_height"]
base_height = order_data["blat_height"] - rules["thick_blat"] - rules["height_legs"]
base_depth = order_data["depth_base"] - rules["gap_spate"] - rules["gap_fata"]

gap_base_top = 700
top_height = order_data["h_bucatarie"] - 90 - order_data["blat_height"] - gap_base_top
top_depth = order_data["top_depth"]

gen_width = rules["general_width"]
thick_pal = rules["thick_pal"]

order = Order(order_data)

c1 = BaseBox("C1", base_height, gen_width, base_depth, rules)
c1.add_drawer_a_pal(100,20) #sertare cu cutii, nu tandembox
c1.add_drawer_a_pal(100, 200)
c1.add_drawer_a_pal(100,400)
c1.add_drawer_a_pal(100,600)
# c1.add_front([[40,100],[40,100],[20,100]],"drawer")
c1.remove_element("blat","C1.blat")
#c1.move_corp("z", rules["height_legs"]), c1.move_corp("y", - rules["gap_spate"])
order.append(c1)

c2 = BaseCorner("C2", base_height, 850, 850, rules, 350, 350, "right", False)
c2.remove_element("front", "C2_1")
c2.remove_element("front", "C2_2")
placa_1 = BoardPal("C2.colt1", base_height - thick_pal, 200, rules["thick_pal"], 2, 0,0,0)
placa_1.rotate("y"), placa_1.rotate("z"), placa_1.move("x", c2.width - placa_1.width - thick_pal)
placa_1.move("y", c2.depth - 200 - thick_pal), placa_1.move("z", thick_pal)
placa_2 = BoardPal("C2.colt2", base_height - thick_pal, 200, rules["thick_pal"], 0, 0,0,0)
placa_2.rotate("y"), placa_2.move("y", c2.depth - placa_2.width), placa_2.move("x", c2.width - placa_1.width), placa_2.move("z", thick_pal)
c2.append(placa_1)
c2.append(placa_2)
c2.move_corp("y", -350)
# c2.move_corp("z", rules["height_legs"]), c2.move_corp("y", - rules["gap_spate"])
order.append(c2)

c3 = BaseBox("C3", base_height, gen_width, base_depth, rules)
c3.add_drawer_a_pal(100, 20)
c3.get_item_by_type_label("pal","C3.leg1").move("z", -30)
c3.get_item_by_type_label("pal","C3.leg2").move("z", -30)
c3.add_sep_h(c3.width - 2 * thick_pal,0, c3.height - order_data["cuptor_height"]- 30, 1)
c3.get_item_by_type_label("pfl","C3.pfl").__setattr__("width",c3.height - 30 - 4)

c3.rotate_corp("z")
c3.move_corp("x", - c3.depth)
c3.move_corp("y", -350)

# c3.add_front([[20,100]],"drawer")
c3.remove_element("blat","C3.blat")
order.append(c3)

c4 = MsVBox("C4", base_height, 450, base_depth, rules)
#c4.add_front_lateral("right") #TODO de reverificat placa laterala
#c4.remove_element("front", "C4_1")
c4.rotate_corp("z")
c4.move_corp("x", -c3.width - c4.width)
c4.move_corp("y", -c3.width - 350)
order.append(c4)

c5 = SinkBox("C5", base_height, 1000, base_depth, rules) #TODO de verificat daca robinetii intra ok in corp. Daca nu ajustam din corpul de pe colt.
# c5.add_front([[100, 50],[100,50]],"door")
c5.remove_element("blat","C5.blat")
c5.rotate_corp("z")
c5.move_corp("x", - c3.width - c4.width - c5.depth)
c5.move_corp("y", -350 - c3.width - c4.width)
order.append(c5)

c6 = JollyBox("C6", base_height, 300, base_depth, rules)
c6.remove_element("blat","C6.blat")
c6.remove_element("front", "C6_1")
c6.rotate_corp("z")
c6.move_corp("x", - c3.width - c4.width - c5.width - c6.depth)
c6.move_corp("y", -350 -c3.width - c4.width - c5.width)
order.append(c6)

top_offset_z = blat_height + gap_base_top
top_offset_x = -c1.width - c2.width - c3.width - c4.width - c5.width - c6.width
top_offset_y = base_depth - top_depth + rules["gap_spate"]

s1 = TopBox("S1", top_height, gen_width, top_depth, rules)
s1.add_pol(2,2)
# s1.add_front([[100,50],[100,50]],"door")
s1.move_corp("z", top_offset_z)
s1.move_corp("x", top_offset_x)
s1.move_corp("y", top_offset_y)
order.append(s1)

s2 = TopBox("S2", top_height, 300, top_depth, rules)
s2.add_pol(2,2)
# s2.add_front([[100,100]],"door")
# s2.move_corp("x", -s1.width - c2.width), s2.move_corp("y", base_depth - top_depth), s2.move_corp("z", blat_height + gap_base_top)
s2.move_corp("z", top_offset_z)
s2.move_corp("x", top_offset_x)
s2.move_corp("y", top_offset_y)
order.append(s2)

s3 = TopCorner("S3", top_height, 600, 700, rules, 200, 300, "right", 2)
s3.remove_element("front", "S3_1")
s3.remove_element("front", "S3_2")
placa_t1 = BoardPal("S3.colt1", top_height - (2 * rules["thick_pal"]), 250, rules["thick_pal"], 2, 0,0,0)
placa_t1.rotate("y"), placa_t1.rotate("z"), placa_t1.move("x", s3.width - placa_t1.width - thick_pal)
placa_t1.move("y", s3.depth - 250 - thick_pal), placa_t1.move("z", thick_pal)
placa_t2 = BoardPal("S3.colt1", top_height - (2 * rules["thick_pal"]), 250, rules["thick_pal"], 0,0,0, 0)
placa_t2.rotate("y"), placa_t2.move("y", s3.depth - placa_t2.width), placa_t2.move("x", s3.width - placa_t1.width), placa_t2.move("z", thick_pal)
s3.append(placa_t1)
s3.append(placa_t2)
# s3.move_corp("x", -s1.width - c2.width), s3.move_corp("y", base_depth - top_depth - 300), s3.move_corp("z", blat_height + gap_base_top)
s3.move_corp("z", top_offset_z)
s3.move_corp("x", top_offset_x)
s3.move_corp("y", top_offset_y - 300)
order.append(s3)

s4 = TopBox("S4", top_height, 212, top_depth, rules)
s4.add_pol(3,2)
# s4.add_front([[100,100]],"door")

# s4.move_corp("x", -s1.width - s3.width - s2.width - c3.width - 352)
# s4.move_corp("z", blat_height + gap_base_top)
# s4.move_corp("y", -200)
s4.rotate_corp("z")
s4.move_corp("z", top_offset_z)
s4.move_corp("x", top_offset_x - s3.width + 200)
s4.move_corp("y", top_offset_y - 300)

order.append(s4)

s5 = TopBox("S5", top_height, gen_width, top_depth, rules)
s5.add_pol(2,2)
# s5.add_front([[100,50],[100,50]],"door")

# s5.move_corp("z", blat_height + gap_base_top)
# s5.move_corp("y", -s1.width - s3.width - s2.width - c3.width - 356 - s4.width - c5.width - c6.width)
s5.rotate_corp("z")
s5.move_corp("z", top_offset_z)
s5.move_corp("x", top_offset_x - s3.width - s4.width + 200)
s5.move_corp("y", top_offset_y - 300 - s4.width)

order.append(s5)

output_directory = "output"
os.makedirs(output_directory, exist_ok=True)
customer_output_directory = os.path.join(output_directory, str(os.path.basename(__file__)).replace(".py", "_output"))
os.makedirs(customer_output_directory, exist_ok=True)

generate_manufacturing_files(order, customer_output_directory)
