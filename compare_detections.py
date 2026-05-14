import re

# Parse final model results (100-epoch trained model)
final_text = """
image 1/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\13268413_1080_1920_30fps-1-_frame_000150_jpg.rf.5e0fc2dccce9a74e87f5b0543c6983c7.jpg: 640x640 2 persons, 37.2ms
image 2/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\13268413_1080_1920_30fps-1-_frame_000300-a_png.rf.b1e2c136943fc1456ccb913d58761b4d.jpg: 640x640 2 persons, 12.9ms
image 3/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\13268413_1080_1920_30fps-1-_frame_000300_jpg.rf.22e8817b8ef66db13af8f95608f5cc5b.jpg: 640x640 2 persons, 17.2ms
image 4/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\14321470_3840_2160_25fps_frame_000150-b_png.rf.b8ed3be0d66cfe70af4f09da58c4d7ec.jpg: 640x640 3 persons, 17.9ms
image 5/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\14321470_3840_2160_25fps_frame_000450_jpg.rf.50f3596c69f221d5c8d980f55b4da959.jpg: 640x640 3 persons, 14.1ms
image 6/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\14321470_3840_2160_25fps_frame_000750_jpg.rf.9c8f6825407de91d9c3c9fe70b02b04d.jpg: 640x640 9 persons, 16.7ms
image 7/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\14321470_3840_2160_25fps_frame_001200_jpg.rf.1b4b166c62e42dd75665349ce541a23d.jpg: 640x640 3 persons, 18.0ms
image 8/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\14321470_3840_2160_25fps_frame_001650_jpg.rf.b61070c2c66c41ab4c7dfb853d62c057.jpg: 640x640 6 persons, 14.2ms
image 9/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\14618434_2560_1440_30fps_frame_000000b_png.rf.d87682e16d6046ee7f19b5b86c6c1b4b.jpg: 640x640 1 person, 16.5ms
image 10/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\15341742_4096_2160_60fps_frame_000150_jpg.rf.57b3cfe913b1b6d512d87ce743cddfcf.jpg: 640x640 3 persons, 13.3ms
image 11/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\15341742_4096_2160_60fps_frame_000300_jpg.rf.e83e554c8fb03e6bf57e043ded340d2b.jpg: 640x640 1 person, 12.8ms
image 12/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\16161654-uhd_3840_2160_30fps_frame_000000_jpg.rf.3030b29cc16cd8734f7e0d6e6486ecdc.jpg: 640x640 1 person, 12.6ms
image 13/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\20188372-uhd_3840_2160_60fps_frame_000000-a_png.rf.8ba0dd739e761d4e2b4ce4ee33c9ca54.jpg: 640x640 1 person, 12.4ms
image 14/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\2k-Video-Beach-001-30fps_frame_000150_jpg.rf.4ec0f03b6006314af09d8bda4b8585ec.jpg: 640x640 43 persons, 13.1ms
image 15/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\2k-Video-Beach-008_30fps_frame_000150_jpg.rf.7d784afc27d60bedf8dbc59477a93b81.jpg: 640x640 61 persons, 12.7ms
image 16/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\2k-Video-Beach-010_30fps_frame_000300_jpg.rf.ec21f4fe1ad41e89d6d75a8430ac105c.jpg: 640x640 13 persons, 12.5ms
image 17/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\4k-Video-Beach-001_30fps_frame_000000_jpg.rf.7d6830cf46934725333fbe09c6e5dcff.jpg: 640x640 23 persons, 14.1ms
image 18/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\4k-Video-Beach-003_30fps_frame_000000-a_png.rf.00aac85e27aa8662d5d409f3023da129.jpg: 640x640 23 persons, 12.7ms
image 19/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\8858425-uhd_3840_2160_25fps_frame_000150-a_png.rf.3805e104774dcb0896e1650f035b65d9.jpg: 640x640 1 person, 12.6ms
image 20/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\8858425-uhd_3840_2160_25fps_frame_000300_jpg.rf.fa1bde1cc2e4ea7166db4352e9070cbf.jpg: 640x640 (no detections), 12.6ms
image 21/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\Video-Surf-001_frame_000600_jpg.rf.1bb2443a1069a4d596021e9b1456c09a.jpg: 640x640 2 persons, 13.0ms
image 22/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\pexels-ahsenilist-33263149_jpg.rf.2834c0838c379993717e5124675aa18f.jpg: 640x640 (no detections), 12.5ms
image 23/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\pexels-alesiakozik-7899659_jpg.rf.f93fb72c4b6b125f2680eb429d628eaa.jpg: 640x640 (no detections), 13.2ms
image 24/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\pexels-basiciggy-9250013_jpg.rf.d176ce42401c87b2ef920b7a5143aed3.jpg: 640x640 (no detections), 13.3ms
image 25/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\pexels-bohdan-relax-264149016-14588372_jpg.rf.831d71f44a2ee2560d5ffe62909f7d23.jpg: 640x640 (no detections), 12.9ms
image 26/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\pexels-diva-36496444_jpg.rf.e8ccfe58f4e09a27f0ffbd042f247dc7.jpg: 640x640 (no detections), 13.0ms
image 27/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\pexels-enginakyurt-9292871_jpg.rf.87db225c4395c679eb665196fae5e23b.jpg: 640x640 (no detections), 12.8ms
image 28/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\pexels-enrique72-12440392_jpg.rf.b83ca0be69fc25b8e150dacd2a59087a.jpg: 640x640 (no detections), 13.1ms
image 29/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\pexels-esteffani-gaio-1306421482-28184210_jpg.rf.5d27df64ceb4d3af9fb7e20ba0a13d7a.jpg: 640x640 (no detections), 12.8ms
image 30/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\pexels-eyupcan-timur-424989336-30942270_jpg.rf.58b97c80c72f672f6236e2b02b79a55c.jpg: 640x640 (no detections), 13.2ms
image 31/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\pexels-frank-cone-140140-17398574_jpg.rf.bb05a8de906b199ea0d2d589157a9feb.jpg: 640x640 (no detections), 13.1ms
image 32/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\pexels-gi-gi-1289764006-31742169_jpg.rf.a62d5fbd43a99672484407dec4847191.jpg: 640x640 (no detections), 12.6ms
image 33/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\pexels-griffinw-20120961_jpg.rf.8667efaa2cf8e318615fa547366d367b.jpg: 640x640 (no detections), 12.0ms
image 34/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\pexels-griffinw-3654863_jpg.rf.b4cc3830902de4065d8a7a83d68c0b34.jpg: 640x640 (no detections), 12.7ms
image 35/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\pexels-hellojoshwithers-15734263_jpg.rf.85c8d5182b3662a4c76e81c935adbe48.jpg: 640x640 (no detections), 12.6ms
image 36/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\pexels-iryna-kuchakova-105196800-9644423_jpg.rf.ff6479c71ebb579c9e38877450366387.jpg: 640x640 (no detections), 17.2ms
image 37/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\pexels-jonathanborba-33893274_jpg.rf.2fa6906fe0f8fb93a6aa11d7b2924fc2.jpg: 640x640 (no detections), 12.2ms
image 38/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\pexels-justin-eng-1711913075-27940635_jpg.rf.0cea1c4ed896844c7a1db0184fb07184.jpg: 640x640 (no detections), 13.1ms
image 39/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\pexels-karola-g-5202525_jpg.rf.f63f3af649b9ed7e3abe769c78f72d66.jpg: 640x640 (no detections), 12.4ms
image 40/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\pexels-lubna-13288641_jpg.rf.b2c026f6f850c5449efd18683a85618e.jpg: 640x640 (no detections), 12.4ms
image 41/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\pexels-magda-ehlers-pexels-7762128_jpg.rf.90c27ee23fd321457f10033a787efdbe.jpg: 640x640 (no detections), 12.3ms
image 42/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\pexels-magda-ehlers-pexels-7762260_jpg.rf.8792ed87bca1d0809bc13ea19c8abb08.jpg: 640x640 (no detections), 12.8ms
image 43/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\pexels-matreding-28588333-1-_jpg.rf.29ee85fc462d5098ae45f6d4f686a34a.jpg: 640x640 (no detections), 12.3ms
image 44/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\pexels-matreding-5331880_jpg.rf.8e3f515fbb74efdfd268448fe0648843.jpg: 640x640 2 persons, 12.2ms
image 45/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\pexels-neslihan-97164342-28700514-1-_jpg.rf.3aff483972adc2292ca3bb69d6b98392.jpg: 640x640 (no detections), 12.4ms
image 46/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\pexels-neslihan-97164342-28700541_jpg.rf.b372a41db76d818cfbd540c58c2615e1.jpg: 640x640 (no detections), 12.1ms
image 47/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\pexels-nui-malama-169330637-35374811_jpg.rf.92f3a539f76fda3a0f4e61e142e1196f.jpg: 640x640 (no detections), 12.5ms
image 48/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\pexels-nui-malama-169330637-36530539_jpg.rf.55fd385c7b86cd60e5d1e542059292dc.jpg: 640x640 (no detections), 12.3ms
image 49/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\pexels-oktay-koseoglu-42034955-14371297_jpg.rf.77959aa5abf708521a6b0eed7f31b798.jpg: 640x640 (no detections), 12.3ms
image 50/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\pexels-oussama-grabsi-2147703525-35100550_jpg.rf.11e46692ce189f5eff0db2cb1d8a9dad.jpg: 640x640 (no detections), 14.3ms
image 51/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\pexels-pelin-2937827-20732316_jpg.rf.47707d8cb90447166df32ed215724bd5.jpg: 640x640 (no detections), 12.6ms
image 52/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\pexels-plasticlines-17836476_jpg.rf.edeb8ef88c154e4cca2a4122b93a593a.jpg: 640x640 (no detections), 12.3ms
image 53/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\pexels-raulling-31995195_jpg.rf.1b40e092452715722711e4c4d9256ae4.jpg: 640x640 (no detections), 12.4ms
image 54/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\pexels-raybilcliff-27027651_jpg.rf.d978588de3c660f09ac2bbd4c7d39869.jpg: 640x640 (no detections), 12.3ms
image 55/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\pexels-roman-odintsov-6493450_jpg.rf.ba7dc15f445214a56b9a8e0d22d8e386.jpg: 640x640 (no detections), 12.3ms
image 56/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\pexels-shreyaan-17512569_jpg.rf.a04340dbdfb3746c0f9de65b030089cf.jpg: 640x640 (no detections), 13.3ms
image 57/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\pexels-shvets-production-7565607_jpg.rf.1eacb4f4e835d65af581fdb534b8b738.jpg: 640x640 (no detections), 12.5ms
image 58/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\pexels-stonesdonotdisappear-19564400_jpg.rf.3a0be15da41d9f24d00edab2c1e0c740.jpg: 640x640 (no detections), 12.4ms
image 59/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\pexels-suju-17853985_jpg.rf.c8b5d5c654f3fbe78ce393cea3f397f4.jpg: 640x640 1 person, 12.8ms
image 60/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\pexels-tatiana-137432171-10742174_jpg.rf.70d7d153ab5f2772cb5e26cfbf65dd1c.jpg: 640x640 (no detections), 12.9ms
image 61/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\pexels-thephotokai-33648185_jpg.rf.966e82e3f1fd906a7e2d95cdffbbc640.jpg: 640x640 (no detections), 12.7ms
image 62/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\pexels-trickshot-fotos-922614184-19968092_jpg.rf.4258fcb6ba100cf3c49a9c1e824828ab.jpg: 640x640 3 persons, 13.0ms
image 63/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\pexels-umar-al-farouq-578250965-20505732_jpg.rf.227f06eb55423239ce61d73fc29a2f45.jpg: 640x640 (no detections), 17.9ms
image 64/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\pexels-vera-silkina-85579813-9076557_jpg.rf.2b25227543a65742f6c06802ae9cd6ca.jpg: 640x640 (no detections), 16.3ms
image 65/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\pexels-zeynep-sude-emek-193601188-34962541_jpg.rf.16f687f706c55c334c58b5792a19402f.jpg: 640x640 (no detections), 14.4ms
"""

# Parse standard YOLO results
standard_text = """
image 1/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\13268413_1080_1920_30fps-1-_frame_000150_jpg.rf.5e0fc2dccce9a74e87f5b0543c6983c7.jpg: 640x640 (no detections), 17.4ms
image 2/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\13268413_1080_1920_30fps-1-_frame_000300-a_png.rf.b1e2c136943fc1456ccb913d58761b4d.jpg: 640x640 2 persons, 15.2ms
image 3/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\13268413_1080_1920_30fps-1-_frame_000300_jpg.rf.22e8817b8ef66db13af8f95608f5cc5b.jpg: 640x640 (no detections), 14.7ms
image 4/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\14321470_3840_2160_25fps_frame_000150-b_png.rf.b8ed3be0d66cfe70af4f09da58c4d7ec.jpg: 640x640 2 persons, 15.5ms
image 5/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\14321470_3840_2160_25fps_frame_000450_jpg.rf.50f3596c69f221d5c8d980f55b4da959.jpg: 640x640 3 persons, 16.2ms
image 6/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\14321470_3840_2160_25fps_frame_000750_jpg.rf.9c8f6825407de91d9c3c9fe70b02b04d.jpg: 640x640 8 persons, 17.1ms
image 7/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\14321470_3840_2160_25fps_frame_001200_jpg.rf.1b4b166c62e42dd75665349ce541a23d.jpg: 640x640 2 persons, 15.3ms
image 8/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\14321470_3840_2160_25fps_frame_001650_jpg.rf.b61070c2c66c41ab4c7dfb853d62c057.jpg: 640x640 5 persons, 16.1ms
image 9/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\14618434_2560_1440_30fps_frame_000000b_png.rf.d87682e16d6046ee7f19b5b86c6c1b4b.jpg: 640x640 (no detections), 16.8ms
image 10/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\15341742_4096_2160_60fps_frame_000150_jpg.rf.57b3cfe913b1b6d512d87ce743cddfcf.jpg: 640x640 (no detections), 17.0ms
image 11/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\15341742_4096_2160_60fps_frame_000300_jpg.rf.e83e554c8fb03e6bf57e043ded340d2b.jpg: 640x640 (no detections), 16.8ms
image 12/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\16161654-uhd_3840_2160_30fps_frame_000000_jpg.rf.3030b29cc16cd8734f7e0d6e6486ecdc.jpg: 640x640 1 person, 13.5ms
image 13/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\20188372-uhd_3840_2160_60fps_frame_000000-a_png.rf.8ba0dd739e761d4e2b4ce4ee33c9ca54.jpg: 640x640 1 person, 14.8ms
image 14/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\2k-Video-Beach-001-30fps_frame_000150_jpg.rf.4ec0f03b6006314af09d8bda4b8585ec.jpg: 640x640 3 persons, 2 birds, 17.6ms
image 15/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\2k-Video-Beach-008_30fps_frame_000150_jpg.rf.7d784afc27d60bedf8dbc59477a93b81.jpg: 640x640 7 persons, 7 birds, 14.4ms
image 16/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\2k-Video-Beach-010_30fps_frame_000300_jpg.rf.ec21f4fe1ad41e89d6d75a8430ac105c.jpg: 640x640 7 persons, 15.4ms
image 17/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\4k-Video-Beach-001_30fps_frame_000000_jpg.rf.7d6830cf46934725333fbe09c6e5dcff.jpg: 640x640 19 persons, 13.5ms
image 18/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\4k-Video-Beach-003_30fps_frame_000000-a_png.rf.00aac85e27aa8662d5d409f3023da129.jpg: 640x640 12 persons, 14.0ms
image 19/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\8858425-uhd_3840_2160_25fps_frame_000150-a_png.rf.3805e104774dcb0896e1650f035b65d9.jpg: 640x640 1 person, 15.8ms
image 20/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\8858425-uhd_3840_2160_25fps_frame_000300_jpg.rf.fa1bde1cc2e4ea7166db4352e9070cbf.jpg: 640x640 2 persons, 1 surfboard, 15.3ms
image 21/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\Video-Surf-001_frame_000600_jpg.rf.1bb2443a1069a4d596021e9b1456c09a.jpg: 640x640 (no detections), 15.0ms
image 22/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\pexels-ahsenilist-33263149_jpg.rf.2834c0838c379993717e5124675aa18f.jpg: 640x640 (no detections), 15.3ms
image 23/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\pexels-alesiakozik-7899659_jpg.rf.f93fb72c4b6b125f2680eb429d628eaa.jpg: 640x640 (no detections), 15.9ms
image 24/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\pexels-basiciggy-9250013_jpg.rf.d176ce42401c87b2ef920b7a5143aed3.jpg: 640x640 1 surfboard, 18.1ms
image 25/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\pexels-bohdan-relax-264149016-14588372_jpg.rf.831d71f44a2ee2560d5ffe62909f7d23.jpg: 640x640 (no detections), 14.7ms
image 26/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\pexels-diva-36496444_jpg.rf.e8ccfe58f4e09a27f0ffbd042f247dc7.jpg: 640x640 (no detections), 13.9ms
image 27/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\pexels-enginakyurt-9292871_jpg.rf.87db225c4395c679eb665196fae5e23b.jpg: 640x640 (no detections), 16.1ms
image 28/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\pexels-enrique72-12440392_jpg.rf.b83ca0be69fc25b8e150dacd2a59087a.jpg: 640x640 (no detections), 15.8ms
image 29/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\pexels-esteffani-gaio-1306421482-28184210_jpg.rf.5d27df64ceb4d3af9fb7e20ba0a13d7a.jpg: 640x640 (no detections), 15.7ms
image 30/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\pexels-eyupcan-timur-424989336-30942270_jpg.rf.58b97c80c72f672f6236e2b02b79a55c.jpg: 640x640 (no detections), 16.1ms
image 31/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\pexels-frank-cone-140140-17398574_jpg.rf.bb05a8de906b199ea0d2d589157a9feb.jpg: 640x640 (no detections), 15.0ms
image 32/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\pexels-gi-gi-1289764006-31742169_jpg.rf.a62d5fbd43a99672484407dec4847191.jpg: 640x640 (no detections), 14.6ms
image 33/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\pexels-griffinw-20120961_jpg.rf.8667efaa2cf8e318615fa547366d367b.jpg: 640x640 (no detections), 15.3ms
image 34/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\pexels-griffinw-3654863_jpg.rf.b4cc3830902de4065d8a7a83d68c0b34.jpg: 640x640 (no detections), 15.4ms
image 35/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\pexels-hellojoshwithers-15734263_jpg.rf.85c8d5182b3662a4c76e81c935adbe48.jpg: 640x640 (no detections), 15.5ms
image 36/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\pexels-iryna-kuchakova-105196800-9644423_jpg.rf.ff6479c71ebb579c9e38877450366387.jpg: 640x640 (no detections), 17.2ms
image 37/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\pexels-jonathanborba-33893274_jpg.rf.2fa6906fe0f8fb93a6aa11d7b2924fc2.jpg: 640x640 (no detections), 15.4ms
image 38/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\pexels-justin-eng-1711913075-27940635_jpg.rf.0cea1c4ed896844c7a1db0184fb07184.jpg: 640x640 (no detections), 15.5ms
image 39/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\pexels-karola-g-5202525_jpg.rf.f63f3af649b9ed7e3abe769c78f72d66.jpg: 640x640 (no detections), 15.3ms
image 40/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\pexels-lubna-13288641_jpg.rf.b2c026f6f850c5449efd18683a85618e.jpg: 640x640 (no detections), 15.2ms
image 41/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\pexels-magda-ehlers-pexels-7762128_jpg.rf.90c27ee23fd321457f10033a787efdbe.jpg: 640x640 (no detections), 15.7ms
image 42/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\pexels-magda-ehlers-pexels-7762260_jpg.rf.8792ed87bca1d0809bc13ea19c8abb08.jpg: 640x640 (no detections), 15.7ms
image 43/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\pexels-matreding-28588333-1-_jpg.rf.29ee85fc462d5098ae45f6d4f686a34a.jpg: 640x640 (no detections), 15.7ms
image 44/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\pexels-matreding-5331880_jpg.rf.8e3f515fbb74efdfd268448fe0648843.jpg: 640x640 (no detections), 15.8ms
image 45/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\pexels-neslihan-97164342-28700514-1-_jpg.rf.3aff483972adc2292ca3bb69d6b98392.jpg: 640x640 (no detections), 16.3ms
image 46/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\pexels-neslihan-97164342-28700541_jpg.rf.b372a41db76d818cfbd540c58c2615e1.jpg: 640x640 (no detections), 17.5ms
image 47/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\pexels-nui-malama-169330637-35374811_jpg.rf.92f3a539f76fda3a0f4e61e142e1196f.jpg: 640x640 (no detections), 15.8ms
image 48/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\pexels-nui-malama-169330637-36530539_jpg.rf.55fd385c7b86cd60e5d1e542059292dc.jpg: 640x640 (no detections), 16.4ms
image 49/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\pexels-oktay-koseoglu-42034955-14371297_jpg.rf.77959aa5abf708521a6b0eed7f31b798.jpg: 640x640 (no detections), 15.1ms
image 50/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\pexels-oussama-grabsi-2147703525-35100550_jpg.rf.11e46692ce189f5eff0db2cb1d8a9dad.jpg: 640x640 (no detections), 17.1ms
image 51/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\pexels-pelin-2937827-20732316_jpg.rf.47707d8cb90447166df32ed215724bd5.jpg: 640x640 (no detections), 15.9ms
image 52/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\pexels-plasticlines-17836476_jpg.rf.edeb8ef88c154e4cca2a4122b93a593a.jpg: 640x640 (no detections), 15.5ms
image 53/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\pexels-raulling-31995195_jpg.rf.1b40e092452715722711e4c4d9256ae4.jpg: 640x640 (no detections), 15.9ms
image 54/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\pexels-raybilcliff-27027651_jpg.rf.d978588de3c660f09ac2bbd4c7d39869.jpg: 640x640 (no detections), 17.3ms
image 55/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\pexels-roman-odintsov-6493450_jpg.rf.ba7dc15f445214a56b9a8e0d22d8e386.jpg: 640x640 (no detections), 16.0ms
image 56/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\pexels-shreyaan-17512569_jpg.rf.a04340dbdfb3746c0f9de65b030089cf.jpg: 640x640 (no detections), 17.6ms
image 57/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\pexels-shvets-production-7565607_jpg.rf.1eacb4f4e835d65af581fdb534b8b738.jpg: 640x640 (no detections), 16.4ms
image 58/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\pexels-stonesdonotdisappear-19564400_jpg.rf.3a0be15da41d9f24d00edab2c1e0c740.jpg: 640x640 (no detections), 15.8ms
image 59/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\pexels-suju-17853985_jpg.rf.c8b5d5c654f3fbe78ce393cea3f397f4.jpg: 640x640 (no detections), 16.1ms
image 60/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\pexels-tatiana-137432171-10742174_jpg.rf.70d7d153ab5f2772cb5e26cfbf65dd1c.jpg: 640x640 (no detections), 15.9ms
image 61/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\pexels-thephotokai-33648185_jpg.rf.966e82e3f1fd906a7e2d95cdffbbc640.jpg: 640x640 (no detections), 16.3ms
image 62/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\pexels-trickshot-fotos-922614184-19968092_jpg.rf.4258fcb6ba100cf3c49a9c1e824828ab.jpg: 640x640 3 persons, 16.0ms
image 63/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\pexels-umar-al-farouq-578250965-20505732_jpg.rf.227f06eb55423239ce61d73fc29a2f45.jpg: 640x640 (no detections), 17.9ms
image 64/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\pexels-vera-silkina-85579813-9076557_jpg.rf.2b25227543a65742f6c06802ae9cd6ca.jpg: 640x640 (no detections), 16.3ms
image 65/65 C:\\AUS\\0 - Repositories\\AI Surf Monitoring\\sds_yolo11\\..\\Training Data Yolo\\test\\images\\pexels-zeynep-sude-emek-193601188-34962541_jpg.rf.16f687f706c55c334c58b5792a19402f.jpg: 640x640 (no detections), 14.4ms
"""

def parse_detections(text):
    results = {}
    pattern = r'image \d+/\d+ .+\\(.+?\.jpg): \d+x\d+ (.+?), \d+\.\d+ms'
    
    for line in text.strip().split('\n'):
        match = re.search(pattern, line)
        if match:
            filename = match.group(1)
            detection_text = match.group(2)
            
            # Count persons only
            person_count = 0
            if '(no detections)' in detection_text:
                person_count = 0
            else:
                # Extract numbers before "person" or "persons"
                person_match = re.search(r'(\d+) persons?', detection_text)
                if person_match:
                    person_count = int(person_match.group(1))
            
            results[filename] = person_count
    
    return results

final_results = parse_detections(final_text)
standard_results = parse_detections(standard_text)

# Create comparison table
comparisons = []
for filename in final_results:
    final_count = final_results.get(filename, 0)
    standard_count = standard_results.get(filename, 0)
    differential = final_count - standard_count
    
    # Shorten filename for display
    short_name = filename[:50] + '...' if len(filename) > 50 else filename
    
    comparisons.append({
        'filename': short_name,
        'final': final_count,
        'standard': standard_count,
        'diff': differential
    })

# Sort by differential (highest to lowest)
comparisons.sort(key=lambda x: x['diff'], reverse=True)

# Print table
print(f"\n{'Image':<55} {'Final':<8} {'Standard':<10} {'Diff':>6}")
print("=" * 85)

for item in comparisons:
    print(f"{item['filename']:<55} {item['final']:<8} {item['standard']:<10} {item['diff']:>+6}")

print("\n" + "=" * 85)
print(f"Total detections - Final: {sum(c['final'] for c in comparisons)}, "
      f"Standard: {sum(c['standard'] for c in comparisons)}, "
      f"Diff: {sum(c['diff'] for c in comparisons):+}")
