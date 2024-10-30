import omni.replicator.core as rep
#import omni.usd

with rep.new_layer():

    #stage = omni.usd.get_context().get_stage()
    #prim = stage.GetPrimAtPath("/Environment/defaultLight")
    #attribute = prim.GetAttribute("inputs:intensity")
    #attribute.Set(0)

    Case_PATH = '/home/rics/Documents/pc_cases/Assets/Parts/HP_600_G2_MD/case/case.usd'
    Case = rep.create.from_usd(Case_PATH)
    with Case:
        rep.modify.pose(
                scale=(100, 100, 100)
                )
        
    Chassis_PATH = '/home/rics/Documents/pc_cases/Assets/Parts/HP_600_G2_MD/chassis/chassis.usd'
    Chassis= rep.create.from_usd(Chassis_PATH)
    with Chassis:
        rep.modify.pose(
                scale=(100, 100, 100)
                )
        
    Fan_PATH = '/home/rics/Documents/pc_cases/Assets/Parts/HP_600_G2_MD/fan/fan.usd'
    Fan = rep.create.from_usd(Fan_PATH)
    with Fan:
        rep.modify.pose(
                scale=(100, 100, 100)
                )
            
    HDD_PATH = '/home/rics/Documents/pc_cases/Assets/Parts/HP_600_G2_MD/hdd/hdd.usd'
    HDD = rep.create.from_usd(HDD_PATH,semantics=[('class', 'HDD')])
    with HDD:
        rep.modify.pose(
                scale=(100, 100, 100)
                )
    
    Heat_Sink_PATH = '/home/rics/Documents/pc_cases/Assets/Parts/HP_600_G2_MD/heat_sink/heat_sink.usd'
    Heat_Sink = rep.create.from_usd(Heat_Sink_PATH)
    with Heat_Sink:
        rep.modify.pose(
                scale=(100, 100, 100)
                )

    Motherboard_PATH = '/home/rics/Documents/pc_cases/Assets/Parts/HP_600_G2_MD/mb/mb.usd'
    Motherboard = rep.create.from_usd(Motherboard_PATH, semantics=[('class', 'Motherboard')])
    with Motherboard:
        rep.modify.pose(
                scale=(100, 100, 100)
                )
    
    RAM_PATH = '/home/rics/Documents/pc_cases/Assets/Parts/HP_600_G2_MD/ram/ram.usd'
    RAM = rep.create.from_usd(RAM_PATH)
    with RAM:
        rep.modify.pose(
                scale=(100, 100, 100)
                )
    
    RAM_Slots_PATH = '/home/rics/Documents/pc_cases/Assets/Parts/HP_600_G2_MD/ram_slots/ram_slots.usd'
    RAM_Slots = rep.create.from_usd(RAM_Slots_PATH, semantics=[('class', 'RAM_Slots')])
    with RAM_Slots:
        rep.modify.pose(
                scale=(100, 100, 100)
                )
        
    ground_plane=rep.create.plane(position=(0, 0, 0), rotation=(0,0.0,0.0), scale=100, visible=True)
    camera = rep.create.camera(position=(0, 0, 100), rotation=(0, -90, 0))
    distance_light = rep.create.light( intensity=2500.0, light_type="distant")
    dome_light = rep.create.light( intensity=1000.0, light_type="dome")
    rep.settings.set_render_pathtraced(samples_per_pixel=64)
    render_product = rep.create.render_product(camera, (1080, 1080))

    def random_ground(plane):
        with plane:
            rep.randomizer.texture(textures=[
                '/home/rics/Documents/pc_cases/textures/metallic-surface-texture.jpg',
                '/home/rics/Documents/pc_cases/textures/natural-wooden-background.jpg',
                '/home/rics/Documents/pc_cases/textures/texture-background.jpg',
                '/home/rics/Documents/pc_cases/textures/wooden-flooring-textured-background-design.jpg',
                '/home/rics/Documents/pc_cases/textures/wood.jpg',
                '/home/rics/Documents/pc_cases/textures/wood_1.jpg',
                '/home/rics/Documents/pc_cases/textures/wood_2.jpg',
            ])
        return plane.node
    
    rep.randomizer.register(random_ground)

    def random_light_angle():
        with distance_light:
            rep.modify.pose(
                rotation=rep.distribution.uniform((-10,-10, -10), (10, 10, 10)))
        return distance_light.node
   
    # Setup randomization
    with rep.trigger.on_frame(num_frames=1500, rt_subframes=50):
        rep.randomizer.random_ground(ground_plane)
        rep.randomizer.random_light_angle()
        with camera:
            rep.modify.pose(position=rep.distribution.uniform((-5,-5, 70),(5, -5, 90)))

    # Initialize and attach writer
    writer = rep.WriterRegistry.get("BasicWriter")

    writer.initialize(output_dir="components_hp_600_g2_md", rgb=True, bounding_box_2d_tight=True)

    writer.attach([render_product])

    rep.orchestrator.preview()
    
