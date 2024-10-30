import omni.replicator.core as rep

with rep.new_layer():

    Dell_3040_SFF_PATH = '/home/rics/Documents/pc_cases/Assets/Cases/Dell_3040_SFF/dell_3040_sff.usd'
    #rotation=(0, 0, 0),
    Dell_3020_SFF_PATH = '/home/rics/Documents/pc_cases/Assets/Cases/Dell_3020_SFF/dell_3020_sff.usd'
    #rotation=(0, 0, 0),
    Acer_Veriton_PATH = '/home/rics/Documents/pc_cases/Assets/Cases/Acer_Veriton_M4630G/acer_veriton.usd'
    #rotation=(0, 0, 0),
    HP_800_G1_SFF_PATH = '/home/rics/Documents/pc_cases/Assets/Cases/HP_800_G1_SFF/hp_800_g1_sff.usd'
    #rotation=(90, 0, -90),
    Dell_790_SFF_PATH = '/home/rics/Documents/pc_cases/Assets/Cases/Dell_Optiplex_790_SFF/dell_790_sff.usd'
    #rotation=(0, 0, 0),
    HP_8200_SFF_PATH = '/home/rics/Documents/pc_cases/Assets/Cases/HP_Elite_8200_SFF/hp_8200_sff.usd'
    #rotation=(0, 0, 0),
    HP_3200_CMT_PATH = '/home/rics/Documents/pc_cases/Assets/Cases/HP_Elite_3200_CMT/hp_3200_cmt.usd'
    #rotation=(0, 0, 0),
    HP_600_G2_PATH = '/home/rics/Documents/pc_cases/Assets/Cases/HP_600_G2_MD/hp_600_g2_md.usd'
    #rotation=(0, 0, -90),
    HP_800_G3_PATH = '/home/rics/Documents/pc_cases/Assets/Cases/HP_800_G3_MD/hp_800_g3_md.usd'
    #rotation=(0, 0, -90),
    HP_Z420_PATH = '/home/rics/Documents/pc_cases/Assets/Cases/HP_Z420/hp_z420.usd'
    #rotation=(0, 0, 0),

    PC = rep.create.from_usd(Acer_Veriton_PATH,semantics=[('class', 'PC')])
    with PC:
        rep.modify.pose(
                rotation=(0, 0, 0),
                scale=(100, 100, 100)
                )
        
    #distance_light = rep.create.light(rotation=(315,0,0), intensity=3000, light_type="distant")
    ground_plane=rep.create.plane(scale=100, visible=True)
    background_plane=rep.create.plane(position=(0, 50, 0), rotation=(90,0.0,0.0), scale=120, visible=True)
    camera = rep.create.camera(position=(0, -50, 5), rotation=(0, -5, -90))
    rep.settings.set_render_pathtraced(samples_per_pixel=64)
    render_product = rep.create.render_product(camera, (1080, 1080))
    
    def rotate_models():
        shapes = rep.get.prims(semantics=[('class', 'PC')])
        with shapes:
            rep.modify.pose(
                position=rep.distribution.uniform((-0.2, 0, 0), (0, 0, 0)),
                rotation=rep.distribution.uniform((0, 0, -30), (0, 0, 30)),
            )
        return shapes.node
    
    rep.randomizer.register(rotate_models)

    def random_background(plane):
        with plane:
            rep.randomizer.texture(textures=[
                    'omniverse://localhost/NVIDIA/Materials/vMaterials_2/Masonry/textures/bricks_grey_diff.jpg',
                    'omniverse://localhost/NVIDIA/Materials/vMaterials_2/Concrete/textures/concrete_wall_aged_diff.jpg',
                    'omniverse://localhost/NVIDIA/Materials/vMaterials_2/Concrete/textures/stone_diff.jpg',
                    'omniverse://localhost/NVIDIA/Materials/vMaterials_2/Concrete/textures/conrete_formed_diff.jpg',
                    ])
        return plane.node
    
    rep.randomizer.register(random_background)

    def random_ground(plane):
        with plane:
            rep.randomizer.texture(textures=[
                    'omniverse://localhost/NVIDIA/Materials/vMaterials_2/Concrete/textures/conrete_formed_diff.jpg',
                    'omniverse://localhost/NVIDIA/Materials/vMaterials_2/Concrete/textures/stone_diff.jpg',
                    'omniverse://localhost/NVIDIA/Materials/vMaterials_2/Concrete/textures/concrete_wall_aged_diff.jpg',
                    ])
        return plane.node
    
    rep.randomizer.register(random_ground)

    # Setup randomization
    with rep.trigger.on_frame(num_frames=750, rt_subframes=50):
        #rep.randomizer.rotate_models()
        rep.randomizer.random_ground(ground_plane)
        rep.randomizer.random_background(background_plane)
        with camera:
            rep.modify.pose(position=rep.distribution.uniform((-5, -50, 3), (5, -40, 10)), rotation=rep.distribution.uniform((-10, -8, -95), (0, 8, -85)))

    # Initialize and attach writer
    writer = rep.WriterRegistry.get("BasicWriter")

    writer.initialize(output_dir='pc', rgb=True, bounding_box_2d_tight=True)

    writer.attach([render_product])

    rep.orchestrator.preview()
    