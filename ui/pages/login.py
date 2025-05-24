from nicegui import ui

def render():
    ui.image("/static/images/logo.svg").classes("logo_l")
    ui.element('div').classes("style_square squere_big")
    ui.element('div').classes("style_square squere_little")
    ui.element('div').classes("style_square2 squere_medium")

    with ui.element("div").classes("avatar_field"):
        ui.html('<div id="three_container" style="width: 100%; height: 100%; position: relative;"></div>')

    ui.add_body_html('''
        <script type="module">
            import * as THREE from 'https://esm.sh/three@0.148.0';
            import { GLTFLoader } from 'https://esm.sh/three@0.148.0/examples/jsm/loaders/GLTFLoader.js';

            window.addEventListener('DOMContentLoaded', () => {
                const container = document.getElementById('three_container');
                if (!container) {
                    console.error('⛔ #three_container not found');
                    return;
                }

                const scene = new THREE.Scene();
                const camera = new THREE.PerspectiveCamera(75, container.clientWidth / container.clientHeight, 0.1, 1000);
                const renderer = new THREE.WebGLRenderer({alpha: true});
                renderer.outputEncoding = THREE.sRGBEncoding;
                renderer.setSize(container.clientWidth, container.clientHeight);
                container.appendChild(renderer.domElement);

                const light = new THREE.AmbientLight(0xffffff, 1);
                scene.add(light);

                let model;
                const loader = new GLTFLoader();
                loader.load('/static/models/baddie_8.glb', function(gltf) {
                    model = gltf.scene;
                    model.scale.set(2.5, 2.5, 2.5);  // увеличим масштаб
                    model.position.y = -2.2;
                    scene.add(model);
                });

                camera.position.z = 3;

                function animate() {
                    requestAnimationFrame(animate);
                    if (model) {
                        model.rotation.y += 0.01;
                    }
                    renderer.render(scene, camera);
                }

                animate();

                window.addEventListener('resize', () => {
                    camera.aspect = container.clientWidth / container.clientHeight;
                    camera.updateProjectionMatrix();
                    renderer.setSize(container.clientWidth, container.clientHeight);
                });
            });
        </script>
        ''')





    with ui.element('section').classes("login_form"):
        with ui.element("div").classes("form_label"):
            ui.label("/login")
        with ui.element("label").classes("remember_checkbox"):
            ui.element("input").props('type="checkbox"').classes("change_swiper")
            with ui.element("span").classes("swiper_label"):
                ui.element("div").classes("swimming_circle")
                ui.image("/static/images/profile.svg").classes("image_login_status login_icon")
                ui.image("/static/images/support.svg").classes("image_login_status message_icon")

        with ui.element("div").classes("input_container_login"):
            with ui.element("div").classes("input_con"):
                ui.element("input").props('id="login" name="login" placeholder="Enter your login"').classes("login_input")
                with ui.element("label").props('for="login"').classes("login_label"):
                    ui.label("login")

            with ui.element("div").classes("input_con"):
                ui.element("input").props('id="password" name="password" placeholder="Enter your password"').classes("login_input")
                with ui.element("label").props('for="password"').classes("login_label"):
                    ui.label("password")

            with ui.element("label").classes("remember_checkbox"):
                ui.element("input").props('type="checkbox"').classes("checkbox_input")
                with ui.element("span").classes("checkbox_label"):
                    ui.label("remember me")

        with ui.element("div").classes("bottom_hint"):
            with ui.element("div").classes("hint"):
                with ui.element("div").classes("i_circle"):
                    ui.label("i")
                with ui.element("div").classes("support_text"):
                    ui.label("If you forgot your password, the only way to get back into the admin panel is to contact another administrator.")
            with ui.element("div").classes("enter_login"):
                ui.label("Enter")
