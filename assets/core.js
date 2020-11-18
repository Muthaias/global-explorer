class GlobalExplorer {
    constructor(api, onUpdate = () => {}, log = () => {}) {
        this._api = api
        this._player = null
        this._content = {}
        this._game = null
        this._version = "unknown"
        this._onUpdate = onUpdate
        this._log = log
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
}