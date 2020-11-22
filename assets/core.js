class GlobalExplorer {
    constructor(api, onUpdate = () => {}) {
        this._api = api
        this._player = null
        this._content = {}
        this._game = null
        this._version = "unknown"
        this._onUpdate = onUpdate
    }

    get player() {
        return this._player
    }

    get content() {
        return this._content
    }

    get version() {
        return this._version
    }

    get game() {
        return this._game
    }

    async init() {
        await this._update()
    }

    async action(action) {
        await this._api.action(action)
        await this._update()
    }

    async _update() {
        [
            this._player, 
            this._content,
            this._game,
            this._version,
        ] = await Promise.all([
            this._api.player(),
            this._api.content(),
            this._api.game(),
            this._api.version(),
        ])
        this._onUpdate()
    }

    static async from_websocket(
        path,
        onUpdate = () => {}
    ) {
        class _Api {
            constructor(socket) {
                this._socket = socket
                console.log(socket)
                this._messages = {}
                this._counter = 0
                this._socket.onmessage = (event) => {
                    const rpc = JSON.parse(event.data)
                    if (this._messages[rpc._id]) {
                        this._messages[rpc._id](rpc.response, rpc.error)
                    }
                };
            }

            async init() {
                return this._rpc({type: "init"})
            }

            async player() {
                return this._rpc({type: "player"})
            }

            async content() {
                return this._rpc({type: "content"})
            }

            async game() {
                return this._rpc({type: "game"})
            }

            async version() {
                return this._rpc({type: "version"})
            }

            async action(action) {
                return this._rpc({
                    type: "action",
                    action: action
                })
            }

            async _rpc(data) {
                return await new Promise((resolve, reject) => {
                    const id = this._counter++
                    const stringData = JSON.stringify({
                        ...data,
                        _id: id,
                    })
                    this._socket.send(stringData)
                    const timeout = setTimeout(() => {
                        delete this._messages[id]
                        console.warn("Timeout: ", id, data)
                        reject("Timeout error")
                    }, 1000)
                    this._messages[id] = (data, error) => {
                        clearTimeout(timeout)
                        delete this._messages[id]
                        if(!error) {
                            resolve(data)
                        } else {
                            resolve(data)
                            console.warn("Server side error: ", error)
                        }
                    }
                    
                })
            }
        }
        const ws = new WebSocket(path)
        return new Promise((resolve, reject) => {
            ws.onopen = async () => {
                const api = new _Api(ws)
                await api.init()
                resolve(new GlobalExplorer(api, onUpdate))
            }
        })
    }
}