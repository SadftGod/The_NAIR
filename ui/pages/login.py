from nicegui import ui
from ui.client.login import grpc_login
def render():
    ui.image("/static/images/logo.svg").classes("logo_l")
    ui.element('div').classes("style_square squere_big")
    ui.element('div').classes("style_square squere_little")
    ui.element('div').classes("style_square2 squere_medium")

    with ui.element("div").classes("avatar_field"):
        ui.html('<div id="three_container" style="width: 100%; height: 100%; position: relative;"></div>')
    ui.add_body_html('''
        <script type="module">
            window.validateLoginInput = (value) => {
                const input = document.getElementById("login");
                const errorDiv = document.getElementById("login_error");
                let hasError = false;

                if (!value || typeof value !== "string") {
                    errorDiv.innerText = "Login must be a non-empty string";
                    hasError = true;
                } else {
                    const emailPattern = /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$/;
                    const isEmail = emailPattern.test(value);

                    if (isEmail) {
                        const domain = value.split("@")[1];
                        if (!domain.includes(".")) {
                            errorDiv.innerText = `Email domain '${domain}' is invalid`;
                            hasError = true;
                        }
                    } else {
                        if (value.length <= 2) {
                            errorDiv.innerText = "Nickname must be longer than 2 characters";
                            hasError = true;
                        } else if (!/^[A-Za-z0-9_]+$/.test(value)) {
                            errorDiv.innerText = "Nickname must contain only Latin letters, digits, or underscores";
                            hasError = true;
                        }
                    }
                }

                if (hasError) {
                    errorDiv.classList.add("shake");
                    input.classList.add("error_focus");
                    if (window.NAIR?.playError) {
                        window.NAIR.playError();
                    }
                } else {
                    errorDiv.innerText = "";
                    input.classList.remove("error_focus");
                }

                setTimeout(() => {
                    errorDiv.classList.remove("shake");
                }, 500);
            };

            window.addEventListener("DOMContentLoaded", () => {
                const input = document.getElementById("login");
                if (input) {
                    input.addEventListener("input", (e) => {
                        validateLoginInput(e.target.value);
                    });
                }
            });
        </script>

        <style>
        @keyframes shake {
        0%   { transform: translateX(0); }
        20%  { transform: translateX(-5px); }
        40%  { transform: translateX(5px); }
        60%  { transform: translateX(-5px); }
        80%  { transform: translateX(5px); }
        100% { transform: translateX(0); }
        }
        .shake {
        animation: shake 0.5s;
        }
        .error_focus {
        box-shadow: inset 0 0 0.1vw 0.2vw rgba(180, 0, 0, 1), 0.3vw 0.4vw 1.6vw 0 rgba(180, 0, 0, 0.6) !important;
        }
        .error_focus ~ .login_label {
        color: rgba(255, 80, 80, 1) !important;
        }
        </style>
        ''')

    ui.add_body_html('''
        <script type="module">
            function playErrorIfExists() {
                if (window.NAIR?.playError) {
                    window.NAIR.playError();
                }
            }

            window.validatePasswordInput = (value) => {
                const input = document.getElementById("password");
                const errorDiv = document.getElementById("password_error");
                let hasError = false;

                if (typeof value !== "string") {
                    errorDiv.innerText = "Password must be a string";
                    hasError = true;
                } else {
                    value = value.trim();
                    if (value.length < 8) {
                        errorDiv.innerText = "Password must be at least 8 characters long";
                        hasError = true;
                    } else if (!/[A-Za-z]/.test(value)) {
                        errorDiv.innerText = "Password must contain at least one letter";
                        hasError = true;
                    } else if (!/\\d/.test(value)) {
                        errorDiv.innerText = "Password must contain at least one digit";
                        hasError = true;
                    }
                }

                if (hasError) {
                    errorDiv.classList.add("shake");
                    input.classList.add("error_focus");
                    playErrorIfExists();
                } else {
                    errorDiv.innerText = "";
                    input.classList.remove("error_focus");
                }

                setTimeout(() => {
                    errorDiv.classList.remove("shake");
                }, 500);
            };

            window.addEventListener("DOMContentLoaded", () => {
                const input = document.getElementById("password");
                if (input) {
                    input.addEventListener("input", (e) => {
                        validatePasswordInput(e.target.value);
                    });
                }
            });
        </script>

        <style>
        @keyframes shake {
        0%   { transform: translateX(0); }
        20%  { transform: translateX(-5px); }
        40%  { transform: translateX(5px); }
        60%  { transform: translateX(-5px); }
        80%  { transform: translateX(5px); }
        100% { transform: translateX(0); }
        }
        .shake {
        animation: shake 0.5s;
        }
        .error_focus {
        box-shadow: inset 0 0 0.1vw 0.2vw rgba(180, 0, 0, 1), 0.3vw 0.4vw 1.6vw 0 rgba(180, 0, 0, 0.6) !important;
        }
        .error_focus ~ .login_label {
        color: rgba(255, 80, 80, 1) !important;
        }
        </style>
        ''')

    ui.add_body_html('''
        <script type="module">
            import * as THREE from 'https://esm.sh/three@0.148.0';
            import { GLTFLoader } from 'https://esm.sh/three@0.148.0/examples/jsm/loaders/GLTFLoader.js';

            let mixer, actions = {}, currentAction = null;

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
                    model.scale.set(4.5, 4.5, 4.5);
                    model.position.y = -5.2;
                    model.position.x = -0.5;
                    scene.add(model);

                    mixer = new THREE.AnimationMixer(model);

                    gltf.animations.forEach((clip) => {
                        const action = mixer.clipAction(clip);
                        action.setLoop(THREE.LoopOnce);
                        action.clampWhenFinished = true;
                        actions[clip.name] = action;
                    });

                    playAnimation('greet');
                    setTimeout(() => playAnimation('yawn'), 10000);
                });

                function playAnimation(name, onFinish = null) {
                    if (!actions[name]) {
                        console.warn('⛔ Animation not found:', name);
                        return;
                    }

                    if (currentAction) {
                        currentAction.stop();
                    }

                    const action = actions[name];
                    currentAction = action;
                    action.reset().play();

                    if (onFinish) {
                        mixer.addEventListener('finished', function listener(e) {
                            mixer.removeEventListener('finished', listener);
                            onFinish();
                        });
                    }
                }

                window.NAIR = {
                    play: (name, next = null) => playAnimation(name, next ? () => playAnimation(next) : null),
                    playSuccess: () => playAnimation('success'),
                    playError: () => playAnimation('error'),
                    playGreet: () => playAnimation('greet'),
                    playYawn: () => playAnimation('yawn'),
                };

                camera.position.z = 3;

                const clock = new THREE.Clock();
                function animate() {
                    requestAnimationFrame(animate);
                    const delta = clock.getDelta();
                    if (mixer) mixer.update(delta);
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

    async def on_login_click():
        login = await ui.run_javascript('document.getElementById("login").value')
        password = await ui.run_javascript('document.getElementById("password").value')
        token = grpc_login(login, password)
        if token:
            ui.notify(f"✔ Logged in with token", type='positive')
            await ui.run_javascript('window.NAIR?.playSuccess()')
            await ui.run_javascript(f'document.cookie = "the_nair_token={token}; path=/; max-age=86400;"')

            await ui.run_javascript('setTimeout(() => window.location.href = "/", 800)')
        else:
            ui.notify("✘ Login failed", type='negative')


    with ui.element('section').classes("login_form"):
        with ui.element("div").classes("form_label"):
            ui.label("/login")
        with ui.element("label").classes("remember_checkbox"):
            ui.element("input").props('type="checkbox"').classes("change_swiper")
            with ui.element("span").classes("swiper_label"):
                ui.element("div").classes("swimming_circle")
                ui.image("/static/images/profile.svg").classes("image_login_status login_icon")
                ui.image("/static/images/support.svg").classes("image_login_status message_icon")

        with ui.element("div").classes("input_con"):
            ui.element("input").props('id="login" name="login" placeholder="Enter your login"').classes("login_input") 
            with ui.element("label").props('for="login"').classes("login_label"):
                ui.label("login")
            with ui.element("div").props('id="login_error"').classes("error_label"):
                ui.label("")

        
        with ui.element("div").classes("input_con"):
            ui.element("input").props('id="password" name="password" placeholder="Enter your password"').classes("login_input")
            with ui.element("label").props('for="password"').classes("login_label"):
                ui.label("password")
            with ui.element("div").props('id="password_error"').classes("error_label"):
                ui.label("")


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
            with ui.element("div").classes("enter_login").on("click", on_login_click):
                ui.label("Enter")

