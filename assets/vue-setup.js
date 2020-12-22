async function setup() {
    const markdownConverter = new showdown.Converter()
    const transform = (markdown) => {
        return markdownConverter.makeHtml(markdown)
    }
    const app = new Vue({
        el: "#app",
        data: {
            content: {},
            viewContent: {},
            visible: false,
            player: {
                name: "John Stirling",
                account: {
                    card_issuer: "VISA",
                    card_number: "2222 2222 2222 2222"
                }
            },
            game: {
                time: "19:00"
            },
            showPlayer: false,
            contentTransform: transform,
            onAction(a) {}
        },
        watch: {
            viewContent(value, oldValue) {
                const element = this.$refs.content
                if (
                    JSON.stringify(value) === JSON.stringify(oldValue)
                    || !element
                ) return

                if (this.visible) {
                    const onTransitionEnd = (event) => {
                        if (event.target !== element) return;

                        element.removeEventListener("transitionend", onTransitionEnd);
                        this.content = value
                        this.visible = true
                    };
                    this.visible = false
                    element.addEventListener("transitionend", onTransitionEnd);
                } else {
                    this.content = value
                    this.visible = true
                }
            }
        }
    })
    const urlParams = new URLSearchParams(window.location.search)
    const savedSessionId = urlParams.get('session_id') || window.localStorage.getItem("global_explorer_session")
    const core = await GlobalExplorer.from_websocket(
        `ws://${window.location.hostname}:5000/`,
        () => {
            console.log(core.version)
            console.log(core.player)
            console.log(core.content)
            console.log(core.game)
            app.game = core.game || {time: "- - -"}
            app.player = core.player || {
                name: "John Doe",
                account: {
                    card_issuer: "NOOP",
                    card_number: "---- ---- ---- ----"
                }
            }
            app.showPlayer = !!core.player
            app.viewContent = core.content
        },
        savedSessionId
    );
    app.onAction = (action, value) => {
        console.log(action, value)
        core.action(action, value)
    }
    core.init().then(() => {
        const sessionId = core.api.sessionId
        if (sessionId) {
            window.localStorage.setItem("global_explorer_session", sessionId)
        }
    })
}